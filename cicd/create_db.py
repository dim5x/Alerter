import os
import sqlite3

def get_query(script_file):
    with open(script_file) as file:
        query = file.read().replace('\n', ' ')
    return query


if os.path.exists('/destination.db'):
    os.remove('../destination.db')

db = sqlite3.connect('../destination.db')
cursor = db.cursor()


# Таблица событий
cursor.execute(get_query('syslog.sql'))
# Таблица с mac-адресами
cursor.execute(get_query('mac_addresses.sql'))
# Таблица с текущим состоянием
cursor.execute(get_query('current_state.sql'))
# Таблица с переменными
cursor.execute(get_query('variables.sql'))
# Триггер при появлении новых событий
cursor.execute(get_query('trigger_syslog_insert.sql'))
# Только для тестирования
cursor.execute(
    "INSERT INTO mac_addresses (mac, wellknown, wellknown_author, wellknown_started_at) "
    "VALUES (?,?,?,?)", ('84:85:06:21:d5:5a', 1, 'dim5x' , '2020-07-26 00:01:02'))

cursor.execute(
    "INSERT INTO mac_addresses (mac, wellknown, wellknown_author, wellknown_started_at) "
    "VALUES (?,?,?,?)", ('84:85:06:21:D5:5A', 1, 'dim5x' , '2020-07-26 00:01:02'))

cursor.execute(
    "INSERT INTO mac_addresses (mac) "
    "VALUES (?)", ('00:25:06:11:d5:00',))
cursor.execute(
    "INSERT INTO mac_addresses (mac) "
    "VALUES (?)", ('08:75:57:11:11:11',))


db.commit()
db.close()

