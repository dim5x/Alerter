import psycopg2
import sqlite3
import os

import management


#   Класс представляет собой абстракцию для работы с базой данных.
#
#   Желательно с классом работать изнутри этого модуля. Целевая схема следующая:
#
#       создается функция, которая будет вызываться извне, def function
#       внутри функции определяется запрос к БД
#     
#       db = db_connection()    // создается экземпляр класса
#       db.open()               // открывается подклчюение
#       result = db.execute...  // выполняется запрос
#       db.close()              // закрывается подключение
#
#   Методы класса
#       
#       open                создать подключение к БД
#       close               закрыть подключение
#       execute             выполняет запрос и возвращает результат в виде списка словарей
#       execute_scalar      выполняет запрос и возвращает результат в виде одного значения
#                           нужно использовать в запросах типа "select count(x) from" или "select top 1 x from" 
#       execute_non_query   необходимо использовать для запросов, которые изменяют данные "insert", "update"
#
#   Атрибуты класса (извне не используются)
#
#       rdbms               тип БД
#       connection_string   строка подключения
#       connection          текущее подключение


class db_connection:
    def __init__(self):
        self.rdbms, self.db_connection_string = management.get_settings(["rdbms", "db_connection_string"])
        # self.db_connection_string = management.get_option("db_connection_string")

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


#
#   Функции для работы извне
#

#   Вставка словаря в соответствующую таблицу
#
#   data    словарь
#   table   имя таблицы
#   conn    подключение
#
#   Если подключение не передается в качестве параметра, то создается подключение по умолчанию, которое закрывается после выполнения

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


#   Проверка существования логина
#
#   login       проверяемый логин

def login_exists(login):
    query = 'select count(1) _count from [admin] where [login] = %(login)s' % {'login': login}
    db = db_connection()
    db.open()
    result = (int(db.execute_scalar(query)) > 0)
    db.close()
    return result


#   Выборка событий из syslog'а
#
#   all_events          получать только c тэгами link-up и LINK_DOWN
#   only_unknown_mac    получить события только с неизвестными mac'ами
#   started_at          начало диапазона
#   ended_at            конец диапазона
#
#   По умолчанию в выборку попадают все события за последний два часа

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
            case
                when mac_addresses.mac is null then ''
                when mac_addresses.wellknown = 1 then 'wellknown'
                when mac_addresses.mac is not null and (mac_addresses.wellknown is null or mac_addresses.wellknown = 0) then 'unknown'
            end mac_type,
			message
		from
			syslog
            left join
            mac_addresses
            on syslog.mac = mac_addresses.mac
		where
			device_time > %(started_at)s
			and
			device_time < %(ended_at)s
		 ''' % {'started_at': started_at, 'ended_at': ended_at}
    if all_events == False:
        query = query + ' and (syslog_tag like \'%link-up%\' or syslog_tag like \'%LINK_DOWN%\')'

    db = db_connection()
    db.open()
    result = db.execute(query)
    db.close()

    return result


#   Выборка всех доверенных mac-адресов

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


#   Выборка всех недоверенных mac-адресов

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


#   Установка признака "доверенный" для mac-адреса

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


#   Удаление признака "доверенный" для mac-адреса

def set_mac_to_unknown(mac, login):
    query = '''update
						mac_addresses
					set
						wellknown = 0,
						wellknown_author = '%(login)s',
						description = '',
						wellknown_started_at = datetime('now','localtime')
					where
						mac = '%(mac)s'
					''' % {'login': login, 'mac': mac}

    db = db_connection()
    db.open()
    db.execute_non_query(query)
    db.close()


#   Аутентификация

def flask_logon(login, hash):
    query = '''
                select
                    count(1) _count
                from
                    admin
                where
                    login = '%(login)s'
                    and
                    hash = '%(hash)s'
            ''' % {'login': login, 'hash': hash}

    db = db_connection()
    db.open()
    result = (int(db.execute_scalar(query)) > 0)
    db.close()
    return result
