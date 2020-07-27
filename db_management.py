import sqlite3
import management

def get_connection(db='default'):
    if db == 'default':
        return management.get_option(db_name)
		
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
	if int(cursor.execute('select count(1) _count from admin where login = \'' + login '\'')) > 0:
		return true
	else
		return false
