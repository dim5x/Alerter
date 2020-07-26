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
		datetime('now', 'localtime'),
		new.from_host,
		(select text_value from variables where name = 'port') port
	from
		variables 
	where
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
		started_at = datetime('now','localtime'),
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
