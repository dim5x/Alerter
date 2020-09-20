 /*Таблица с событиями*/
create table syslog(
    priority integer,
    device_time datetime,
    receivedat datetime not null default (datetime('now','localtime')),
    from_host varchar(200),
    process varchar(50),
    syslog_tag varchar(50),
    message varchar(400),
    mac varchar(17)
    );

/*Таблица с mac-адресами*/
create table mac_addresses(
	mac varchar(17),
	description varchar(400),
	wellknown int,
	wellknown_author varchar(400),
	wellknown_started_at datetime
	);

/*Текущее состояние*/
create table current_state(
	mac varchar(17),
	state integer,
	started_at datetime,
	from_host varchar(200),
	port varchar(30)
	);

/* Учетные записи*/
create table admin(
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
	mac varchar(6),
	manufacturer varchar(100)
);

/* При возникновении новых событий*/
create trigger syslog_insert after insert on syslog
when instr(new.syslog_tag, 'link-up') > 0 or instr(new.syslog_tag, 'LINK_DOWN') > 0 or instr(new.message, 'assoc') > 0
begin
	delete from variables;

	insert into variables(name, integer_value, text_value) 
	select
		'new_mac',
		0,
		case
			when instr(NEW.message, 'MAC') > 0 then
				substr(NEW.message, instr(NEW.message, 'MAC')+4, 17)
			when 
				instr(new.message, 'associated -') > 0 then
				substr(NEW.message, instr(NEW.message, 'associated -')+13, 17)
			else
				null
		end _value;

	insert into mac_addresses(mac)
	select 
		new_data.mac 
	from 
		(
		select
			new.mac mac
		) new_data 
		left join
		(
		select 
			mac
		from
			mac_addresses
		) mac_addresses
		on new_data.mac = mac_addresses.mac 
	where
		new_data.mac is not null
		and 
		mac_addresses.mac is null
	;

	insert into variables(name, text_value)
	select
		'port',
		case
			when instr(message, 'MAC') > 0 then
				substr(
					substr(message, instr(message, 'IFNAME')+7, length(message)-instr(message, 'IFNAME')),
					1,
					instr(substr(message, instr(message, 'IFNAME')+7, length(message)-instr(message, 'IFNAME')), 'MAC') - 2
					)
			when instr(message, 'MAC') = 0 and instr(message, 'IFNAME') > 0 then
				substr(
					substr(message, instr(message, 'IFNAME')+7, length(message)-instr(message, 'IFNAME')),
					1,
					case
						when instr(substr(message, instr(message, 'IFNAME')+7, length(message)-instr(message, 'IFNAME')), ' ') > 0
						 then instr(substr(message, instr(message, 'IFNAME')+7, length(message)-instr(message, 'IFNAME')), ' ')
						else length(substr(message, instr(message, 'IFNAME')+7, length(message)-instr(message, 'IFNAME')))
					end
					)
			else null
		end _value
	from
		(
		select
			upper(new.message) message
		) message_data
		;	
	
	
	
	insert into current_state(mac,state,started_at,from_host,port)
	select
		new_data.mac,
		1,
		datetime(current_timestamp, 'localtime'),
		new.from_host,
		(select text_value from variables where name = 'port') port
	from 
		(
		select
			new.mac mac
		) new_data 
		left join
		(
		select 
			mac
		from
			current_state
		) current_state
		on new_data.mac = current_state.mac 
	where
		new_data.mac is not null
		and 
		current_state.mac is null
		and 
		(
		instr(new.syslog_tag, 'link-up') > 0 
	 	or 
		instr(new.message, ' associated -') > 0
		);
	
	
	update current_state 
	set
		state = 1,
		started_at = datetime('now', 'localtime'),
		from_host = new.from_host,
		port = (select text_value from variables where name = 'port')
	where 
		mac = new.mac
		and
		(
		instr(new.syslog_tag, 'link-up') > 0
		or
		instr(NEW.message, ' associated -') > 0
		);
	
	
	update current_state 
	set
		state = 0,
		started_at = new.receivedat
	where
		(
		instr(new.syslog_tag, 'LINK_DOWN') > 0
		and 
		port = (select text_value from variables where name = 'port')
		and
		from_host = new.from_host
		)
		or
		(
		(instr(NEW.message, 'disassociated -') > 0 or instr(NEW.message, 'Disassoc') > 0)
		and
		mac = new.mac
		);
end;
