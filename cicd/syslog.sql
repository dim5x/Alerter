create table syslog(
	id integer primary key,
    priority integer,
    device_time datetime,
    receivedat datetime not null default current_timestamp,
    from_host varchar(200),
    process varchar(50),
    syslog_tag varchar(50),
    message varchar(400)
    );
