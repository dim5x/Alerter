 /*Таблица с событиями*/
create table syslog(
    id integer primary key,
    priority integer,
    device_time datetime,
    receivedat datetime not null default (datetime('now','localtime')),
    from_host varchar(200),
    process varchar(50),
    syslog_tag varchar(50),
    message varchar(400)
    );

/*Таблица с mac-адресами*/
create table mac_addresses(
	mac varchar(30),
	device varchar(400),
	description varchar(400),
	wellknown int,
	wellknown_author varchar(400),
	wellknown_started_at datetime
	);

/*Текущее состояние*/
create table current_state(
	mac varchar(30),
	state integer,
	started_at datetime,
	from_host varchar(200),
	port varchar(30)
	);

/* Учетные записи*/
create table admin(
	id integer primary key,
	login varchar(20),
    hash varchar(96),
    date_time datetime not null default (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
    );

/* Переменные*/	
create table variables(
	name varchar(30),
	integer_value integer,
	text_value varchar(30)
	);
	
/* Производители */

create table mac_owners(
	mac varchar(30),
	manufacturer varchar(200)
)

/* При возникновении новых событий*/
create trigger syslog_insert after insert on syslog
when instr(new.syslog_tag, 'link-up') > 0 or instr(new.syslog_tag, 'LINK_DOWN') > 0
begin
	delete from variables;
	insert into variables(name, integer_value, text_value) 
	select
		'new_mac',
		0,
		case
			when instr(NEW.message, 'MAC') > 0 then
				substr(NEW.message, instr(NEW.message, 'MAC')+4, 17)
			else
				null
		end _value;

	insert into mac_addresses(mac)
	select
		text_value mac
	from 
		variables 
	where 
		text_value is not null
		and
		name = 'new_mac'
		and 
		text_value not in
						(
						select 
							mac
						from
							mac_addresses);
							
	insert into variables(name, text_value)
	select
		'port',
		case
			when instr(NEW.message, 'MAC') > 0 then
				substr(
					substr(NEW.message, instr(NEW.message, 'IFNAME')+7, length(NEW.message)-instr(NEW.message, 'IFNAME')),
					1,
					instr(substr(NEW.message, instr(NEW.message, 'IFNAME')+7, length(NEW.message)-instr(NEW.message, 'IFNAME')), 'MAC') - 2
					)
			else
				substr(
					substr(NEW.message, instr(NEW.message, 'IFNAME')+7, length(NEW.message)-instr(NEW.message, 'IFNAME')),
					1,
					ifnull(
						instr(substr(NEW.message, instr(NEW.message, 'IFNAME')+7, length(NEW.message)-instr(NEW.message, 'IFNAME')), ' '),
						length(substr(NEW.message, instr(NEW.message, 'IFNAME')+7, length(NEW.message)-instr(NEW.message, 'IFNAME')))
						)
					)
		end _value;	
	
	insert into current_state(mac,state,started_at,from_host,port)
	select
		text_value,
		1,
		datetime(current_timestamp, 'localtime'),
		new.from_host,
		(select text_value from variables where name = 'port') port
	from
		variables 
	where
		text_value is not null
		and
		name = 'new_mac'
		and 
		text_value not in
						(
						select 
							mac
						from
							current_state);
	
	
	update current_state 
	set
		state = 1,
		started_at = datetime('now', 'localtime'),
		from_host = new.from_host,
		port = (select text_value from variables where name = 'port')
	where 
		mac = (
				select 
					text_value 
				from 
					variables 
				where 
					name = 'new_mac'
					and
					text_value in (
									select 
										mac 
									from 
										current_state
									)
				)
		and
		instr(new.syslog_tag, 'link-up') > 0;
		
	update current_state 
	set
		state = 0,
		started_at = new.receivedat
	where
		instr(new.syslog_tag, 'LINK_DOWN') > 0
		and 
		port = (select text_value from variables where name = 'port')
		and
		from_host = new.from_host;	
end;

/* Данные для отладки */
insert into admin (login, hash) values ('admin','36d841bb32fc5ef1a5704652097584ee789f4d2e745fa283516320163dba0d699b5a502de4f33321155dc5715e0c1e4d');
