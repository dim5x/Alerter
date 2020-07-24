-- Таблица с событиями
drop table if exists syslog;

create table syslog(
	id integer primary key,
    priority integer,
    devicereportedtime datetime,
    receivedat datetime not null default current_timestamp,
    fromhost varchar(200),
    process varchar(50),
    syslogtag varchar(50),
    message varchar(400)
    );
    
-- Доверенные mac-адресы
drop table if exists wellknown_mac;
   
create table wellknown_mac(
	mac varchar(30),
	description varchar(400),
	started_at datetime,
	ended_at datetime,
	author varchar(400)
	);

-- Неизвестные mac-адресы
drop table if exists unknown_mac;

create table unknown_mac(
	mac varchar(30),
	started_at datetime,
	company varchar(400)
	);

-- Текущее состояние
drop table if exists current_state;

create table current_state(
	mac varchar(30),
	state integer,
	started_at datetime,
	fromhost varchar(200),
	port varchar(30)
	);

-- Переменные
drop table if exists variables;

create table variables(
	name varchar(30),
	integer_value integer,
	text_value varchar(30)
	);

-- При возникновении новых событий
drop trigger if exists syslog_insert;

create trigger syslog_insert after insert on syslog
when instr(new.syslogtag, 'link-up') > 0 or instr(new.syslogtag, 'LINK_DOWN') > 0
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
		--NEW.message REGEXP '%#"([0-9a-f]{2}:){5}[0-9a-f]{2}#"%');	
	insert into unknown_mac(mac, started_at)
	select
		new_data.mac,
		datetime(current_timestamp, 'localtime')
	from 
		(
		select
			text_value mac
		from
			variables
		where 
			name = 'new_mac'
		) new_data
		left join
		(
		select
			mac 
		from 
			wellknown_mac 
		where 
			ended_at is null		
		union		
		select 
			mac
		from 
			unknown_mac
		) well_mac
		on
		new_data.mac = well_mac.mac
	where 
		well_mac.mac is null
		and 
		new_data.mac is not null;	
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
	insert into current_state(mac,state,started_at,fromhost,port)
	select
		new_data.mac,
		1,
		datetime(current_timestamp, 'localtime'),
		new.fromhost,
		(select text_value from variables where name = 'port') port
	from 
		(
		select
			text_value mac
		from
			variables
		where 
			name = 'new_mac'
		) new_data
		left join
		(
		select
			mac 
		from 
			current_state 
		) cs
		on new_data.mac = cs.mac
	where
		 cs.mac is null
		and 
		new_data.mac is not null;	
	update current_state 
	set
		state = 1,
		started_at = new.receivedat,
		fromhost = new.fromhost,
		port = (select text_value from variables where name = 'port')
	where 
		mac = (
				select --top 1
					new_data.mac
				from 
					(
					select
						text_value mac
					from 
						variables
					where 
						name = 'new_mac'
					) new_data
					join
					(
					select
						mac
					from
						current_state
					) cs
					on
					new_data.mac = cs.mac
				limit 1
				)
		and 
		instr(new.syslogtag, 'link-up') > 0;	
	update current_state 
	set
		state = 0,
		started_at = new.receivedat
	where
		instr(new.syslogtag, 'LINK_DOWN') > 0
		and 
		port = (select text_value from variables where name = 'port')
		and
		fromhost = new.fromhost;	
end;

-------------------------------------------
-- Данные для отладки
insert into syslog 
select
	null,
	null,
	'2020-01-01',
	'2020-01-01',
	't',
	'LINK_DOWN.slax:',
	'IFNAME ge-5/0/41.0 MAC d8:9d:67:64:f6:d8'
	
insert into syslog 
select
	null,
	null,
	'2020-01-01',
	'2020-01-01',
	't',
	'link-up.slax:',
	'IFNAME ge-5/0/41.0 MAC d8:9d:67:64:f6:d8'
	
select * from unknown_mac

delete from unknown_mac

select * from current_state 

delete from current_state