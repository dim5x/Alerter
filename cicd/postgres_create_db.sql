 /*Таблица с событиями*/
create table syslog(
    id integer primary key,
    priority integer,
    device_time timestamp,
    receivedat timestamp with time zone default current_timestamp,
    from_host varchar(200),
    process varchar(50),
    syslog_tag varchar(50),
    message varchar(400),
    mac varchar(17)
    );
	
/*Таблица с mac-адресами*/
create table mac_addresses(
	mac varchar(17),
	device varchar(70),
	description varchar(400),
	wellknown int,
	wellknown_author varchar(400),
	wellknown_started_at timestamp
	);