import psycopg2
import sqlite3
import os

import management


class db_connection:
    def __init__(self):
        self.rdbms, self.db_connection_string = management.get_settings(["rdbms","db_connection_string"])
        #self.db_connection_string = management.get_option("db_connection_string")

    def open(self):
        if self.rdbms == "sqlite":
            self.connection = sqlite3.connect(self.db_connection_string)
        elif self.rdbms == "postgresql":
            self.connection = psycopg2.connect(self.db_connection_string)

    def close(self):
        self.connection.close()

    def test_connection(self):
        if self.rdbms == "sqlite":
            if os.path.exists(self.db_connection_string):
                return 0
            else:
                return 1
        return 0

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, query):
        self.connection.row_factory = self.dict_factory
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_non_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True

    def execute_scalar(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        return result


def get_value(data):
    if data is None:
        value = 'null'
    elif not data.isdigit():
        value = '\'' + data.replace('\'', '\'\'') + '\''
    else:
        value = data
    return value


def insert_data(data, table, conn='not_created'):
    columns, values = '', ''
    for key in data:
        if columns == '':
            columns += key
            values += get_value(data[key])
        else:
            columns = columns + ', ' + key
            values = values + ', ' + get_value(data[key])

    query = 'insert into ' + table + '(' + columns + ') values(' + values + ')'

    connection = conn
    if connection == 'not_created':
        db = db_connection()
        db.open()

    db.execute_non_query(query)

    if connection == 'not_created':
        db.close()


def login_exists(login):
    query = 'select count(1) _count from [admin] where [login] = %(login)s' % {'login': login}
    db = db_connection()
    db.open()
    result = (int(db.execute_scalar(query)) > 0)
    db.close()
    return result


def get_events(all_events=True, only_unknown_mac=False, started_at='', ended_at=''):
    if started_at == '':
        started_at = 'datetime(\'now\',\'-2 hour\', \'localtime\')'
    if ended_at == '':
        ended_at = 'datetime(\'now\', \'localtime\')'

    query = '''select 
			device_time,
			priority,
			from_host,
			process,
			syslog_tag,
			message
		from
			syslog
		where
			device_time > %(started_at)s
			and
			device_time < %(ended_at)s
		 ''' % {'started_at': started_at, 'ended_at': ended_at}
    if not all_events:
        query = query + ' and (syslog_tag like \'%link-up%\' or syslog_tag like \'%LINK_DOWN%\')'

    db = db_connection()
    db.open()
    result = db.execute(query)
    db.close()

    return result


def get_wellknown_mac():
    query = '''select 
					mac_addresses.mac mac,
					mac_owners.manufacturer manufacturer
				from 
					mac_addresses 
					left join
					mac_owners
					on
					upper(substr(replace(mac_addresses.mac,':',''),1,6)) = mac_owners.mac
				where 
					wellknown = 1
				'''

    db = db_connection()
    db.open()
    result = db.execute(query)
    db.close()

    return result


def get_unknown_mac():
    query = '''select 
					mac_addresses.mac mac,
					mac_owners.manufacturer manufacturer
				from 
					mac_addresses 
					left join
					mac_owners
					on
					upper(substr(replace(mac_addresses.mac,':',''),1,6)) = mac_owners.mac
				where 
					wellknown = 0 
					or 
					wellknown is null
				'''

    db = db_connection()
    db.open()
    result = db.execute(query)
    db.close()

    return result


def set_mac_to_wellknown(mac, login, description):
    query = '''update
						mac_addresses
					set
						wellknown = 1,
						wellknown_author = '%(login)s',
						description = '%(description)s',
						wellknown_started_at = datetime('now','localtime')
					where
						mac = '%(mac)s'
					''' % {'login': login, 'mac': mac, 'description': description}

    db = db_connection()
    db.open()
    db.execute_non_query(query)
    db.close()
