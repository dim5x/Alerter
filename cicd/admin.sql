create table admin(
	id integer primary key,
	login varchar(20),
    hash varchar(96),
    date_time datetime not null default (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
    );