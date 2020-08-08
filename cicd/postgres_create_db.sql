 /*Таблица с событиями*/
create table syslog(
    priority integer,
    device_time timestamp,
    receivedat timestamp default current_timestamp,
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
	wellknown_started_at timestamp
	);
	
/*Текущее состояние*/
create table current_state(
	mac varchar(17),
	state integer,
	started_at timestamp,
	from_host varchar(200),
	port varchar(30)
	);

/* Учетные записи*/
create table admin(
	login varchar(20),
    hash varchar(96),
    date_time timestamp default current_timestamp
    );
	
/* Производители */

create table mac_owners(
	mac varchar(6),
	manufacturer varchar(200)
);

/*Функция для триггера на insert в syslog*/

create or replace function public.syslog_insert()
	returns trigger
	language plpgsql
as $function$

	declare
		new_port varchar(17);
	begin
		if TG_OP = 'INSERT' THEN
		
			new_port = substring(NEW.message from '%#"([a-z]{2}-([0-9]{1,}))(/([0-9]){1,}){1,}#"%' for '#');
		
			/* Добавим новый mac-адрес */
		
			/*
			Если данный mac-адрес отсутсвуюет
					- в базе инвентаризации
					- и среди известных mac-адресов
				 необходимо внести его в таблицу
			*/
			/* if (select count(1) from wellknown_mac where mac = new_mac) + (select count(1) from items_devicenetworkcards where mac = new_mac) = 0 then*/
			
			if length(new.mac) > 0 then
				if (select count(1) from mac_addresses where mac = new.mac) = 0 then
 					insert into mac_addresses(mac)
 					select 
 						upper(new.mac);
				end if;
			end if;
			
			if (position('link-up' in new.syslog_tag) > 0 or position(' associated -' in new.message) > 0) and length(new.mac) > 0 then
				
				/* Обновим таблицу текущих состояний */
		
				if (select count(1) from current_state where mac = new.mac) = 0 then
					insert into current_state(mac, state, started_at, from_host, port)
					select
						new.mac,
						1,
						current_timestamp,
						new.from_host,
						new_port;
				else
					update current_state
				set
						state = 1,
						started_at = current_timestamp,
						from_host = new.from_host,
						port = new_port
					where
						mac = new.mac;
				end if;
			
				return new;
			
			end if;
			
			if position('SNMP_TRAP_LINK_DOWN' in new.syslog_tag) > 0 then
			
				update current_state
				set
					state = 0,
					started_at = current_timestamp
				where
					port = new_port
					and
					from_host = new.from_host;
			
				return new;
	
			end if;
		
			if position('disassociated -' in new.message) > 0 or position('Disassoc' in new.message) > 0 then
			
				update current_state
				set
					state = 0,
					started_at = current_timestamp
				where
					mac = new.mac;
			
				return new;
	
			end if;
		
			return new;
		
		end if;
	end;

$function$
;


create trigger syslog_insert after
insert
on
public.syslog for each row execute procedure syslog_insert();