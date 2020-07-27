import os
import sqlite3


def get_query(script_file):
    with open(script_file, 'r') as file:
        query = file.read().replace('\n', ' ')
    return query


if os.path.exists('/destination.db'):
     os.remove('../destination.db')

db = sqlite3.connect('../destination.db')
cursor = db.cursor()

# Создание базы данных
cursor.executescript(get_query('create_db.sql'))

# Заполнение таблицы mac_owners
with open('macs.txt') as file:
    lines = file.read().splitlines()

query = 'insert into mac_owners(mac, manufacturer) values (\')'

for line in lines:
    mac, owner = line.split('     ')
	query = query + mac + '\', \'' + owner + '\','
	
query = query[0:-1] + ')'

cursor.execute(query)
	
        

db.commit()
db.close()
