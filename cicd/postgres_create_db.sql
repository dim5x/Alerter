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
	id integer primary key,
	login varchar(20),
    hash varchar(96),
    date_time timestamp with time zone default current_timestamp
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
	manufacturer varchar(70)
);