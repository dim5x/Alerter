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

# Таблица событий
#cursor.execute(get_query('syslog.sql'))
# Таблица с логин/паролем.
#cursor.execute(get_query('admin.sql'))
# # Таблица с mac-адресами
#cursor.execute(get_query('mac_addresses.sql'))
# # Таблица с текущим состоянием
#cursor.execute(get_query('current_state.sql'))
# # Таблица с переменными
#cursor.execute(get_query('variables.sql'))
# # Триггер при появлении новых событий
#cursor.execute(get_query('trigger_syslog_insert.sql'))
# Добавление админской учётки
cursor.execute(get_query('create_db.sql'))

db.commit()
db.close()
