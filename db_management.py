import sqlite3
import management

def get_connection(db='default'):
    if db == 'default':
        return management.get_option('db_name')
		
def get_value(data):
    if data is None:
        value = 'null'
    elif not data.isdigit():
        value = '\'' + data.replace('\'', '\'\'') + '\''
    else:
        value = data
    return value

def insert_data(data, table, cursor='not_created'):
    columns, values = '',''
    for key in data:
        if columns == '':
            columns += key
            values += get_value(data[key])
        else:
            columns = columns + ', ' + key
            values = values + ', ' + get_value(data[key])
            
    query = 'insert into ' + table + '(' + columns + ') values(' + values +')'
    
    connection = cursor
    if connection == 'not_created':
        db = sqlite3.connect('destination.db')
        cursor = db.cursor()
        
    cursor.execute(query)
    
    if connection == 'not_created':
        db.commit()
        db.close()
		
def login_exists(login):
    db = sqlite3.connect(get_connection())
    cursor = db.cursor()
    cursor.execute('select count(1) _count from [admin] where [login] = \'' + login + '\'');
    if int(cursor.fetchone()[0]) > 0:
        return True
    else:
        return False

def get_events(all_events=True, started_at='', ended_at=''):
    db = sqlite3.connect(get_connection())
    cursor = db.cursor()
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
		 ''' %  {'started_at':started_at, 'ended_at':ended_at}
    if not all_events:
        query = query + ' and (syslog_tag like \'%link-up%\' or syslog_tag like \'%LINK_DOWN%\')'
		
    result = list(cursor.execute(query))

    db.close()
	
    return result

def get_wellknown_mac():
    db = sqlite3.connect(get_connection())
    cursor = db.cursor()
	
    result = list(cursor.execute('select mac from mac_addresses where wellknown = 1'))
	
    db.close()
	
    return result
	
def get_unknown_mac():
    db = sqlite3.connect(get_connection())
    cursor = db.cursor()
	
    result = list(cursor.execute('''select 
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
				'''))
    db.close()
	
    return result
