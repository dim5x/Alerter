# This Python file uses the following encoding: utf-8
"""Модуль для работы с БД."""
import os
import sqlite3
import psycopg2
import psycopg2.extras

import management


class DatabaseConnection:
    """ Класс представляет собой абстракцию для работы с базой данных.

    Желательно с классом работать изнутри этого модуля. Целевая схема следующая:

        создается функция, которая будет вызываться извне, def function
        внутри функции определяется запрос к БД

        db = db_connection()    // создается экземпляр класса
        db.open()               // открывается подклчюение
        result = db.execute...  // выполняется запрос
        db.close()              // закрывается подключение

    Методы класса:

        open                создать подключение к БД.
        close               закрыть подключение.
        execute             выполняет запрос и возвращает результат в виде списка словарей.
        execute_scalar      выполняет запрос и возвращает результат в виде одного значения,
                            нужно использовать в запросах типа "select count(x) from" или
                            "select top 1 x from".
        execute_non_query   необходимо использовать для запросов, которые изменяют данные,
                            такие как:   "insert", "update".
        execute_script      выполняет скрипт из *.sql-файла.
        test_connection     проверить возможность подключения:
                            0 - всё в порядке;
                            1 - подключение есть, отсутствует структура, можно вызвать метод create_db;
                            2 - что-то непонятное, нужно искать причины.

    Атрибуты класса (извне не используются):

        rdbms               тип БД.
        connection_string   строка подключения.
        connection          текущее подключение.
        """

    def __init__(self):
        self.rdbms, self.db_connection_string, self.debug = management.get_settings(
            ["rdbms", "db_connection_string", "debug"])

    def create_db(self):
        """Создание структуры базы данных:"""
        self.open()

        if self.rdbms == "sqlite":
            self.execute_script("cicd/db/sqlite_create_db.sql")
        elif self.rdbms == "postgresql":
            self.execute_script("cicd/db/postgres_create_db.sql")

        # Заполнение таблицы mac_owners

        with open('cicd/db/macs.txt', encoding="utf-8") as file:
            lines = file.read().splitlines()
        query = 'insert into mac_owners(mac, manufacturer) values '
        for line in lines:
            mac, owner = line[0:6].replace('\'', '\'\''), line[11:].replace('\'', '\'\'')
            query += '(\'' + mac + '\', \'' + owner + '\'),'
        query = query[0:-1] + ';'
        self.execute_non_query(query)

        # Тестовые наборы данных для отладки

        if self.debug:
            self.execute_script("cicd/db/debug_data.sql")

        self.close()

    def open(self):
        """Открытие."""
        if self.rdbms == "sqlite":
            self.connection = sqlite3.connect(self.db_connection_string)
        elif self.rdbms == "postgresql":
            self.connection = psycopg2.connect(self.db_connection_string)

    def close(self):
        """Закрытие."""
        self.connection.close()

    def test_connection(self):
        """Проверка соединения."""
        if self.rdbms == "sqlite":
            if os.path.exists(self.db_connection_string):
                return 0
            else:
                return 1
        elif self.rdbms == "postgresql":
            # проверка доступности базы данных
            try:
                self.open()
                # проверка наличия структуры в базе данных
                query = "select count(table_name) _count from information_schema.tables WHERE table_schema='public'"
                table_count = self.execute_scalar(query)
                if table_count == 0:
                    self.close()
                    return 1
                else:
                    self.close()
                    return 0
            except:
                return 2
        return 2

    def dict_factory(self, cursor, row):
        dick = {}
        for idx, col in enumerate(cursor.description):
            dick[col[0]] = row[idx]
        return dick

    def execute(self, query):
        """Выполняет запрос и возвращает результат в виде списка словарей."""
        if self.rdbms == 'sqlite':
            self.connection.row_factory = self.dict_factory
            cursor = self.connection.cursor()
        elif self.rdbms == 'postgresql':
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_non_query(self, query):
        """Необходимо использовать для запросов, которые изменяют данные "insert", "update"."""
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True

    def execute_scalar(self, query):
        """Выполняет запрос и возвращает результат в виде одного значения.

        Нужно использовать в запросах типа "select count(x) from" или "select top 1 x from".
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def execute_script(self, path):
        """Выполняет скрипт из *.sql-файла."""
        cursor = self.connection.cursor()
        with open(path, 'r') as file:
            query = file.read().replace('\n', ' ').replace('\t', '')
        if self.rdbms == 'sqlite':
            cursor.executescript(query)
        elif self.rdbms == 'postgresql':
            cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True


def get_value(data):
    if data is None:
        value = 'null'
    elif not data.isdigit():
        value = '\'' + data.replace('\'', '\'\'') + '\''
    else:
        value = data
    return value


""" Функции для работы извне

  Вставка словаря в соответствующую таблицу:

  data    словарь
  table   имя таблицы
  conn    подключение

  Если подключение не передаётся в качестве параметра, то создается подключение по умолчанию,
  которое закрывается после выполнения. 
  """


def insert_data(data, table, conn='not_created'):
    """Добавляем данные в базу."""
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
        db = DatabaseConnection()
        db.open()

    db.execute_non_query(query)

    if connection == 'not_created':
        db.close()


def new_syslog_event(event, db):
    cursor = db.connection.cursor()
    cursor.callproc('new_syslog_event', [event['priority'], event['device_time'],
                                         event['from_host'], event['process'], event['syslog_tag'],
                                         event['message'], event['mac']])
    db.connection.commit()
    cursor.close()


def login_exists(login):
    """ Проверка существования логина:

        login       проверяемый логин
    """
    query = 'select count(1) _count from [admin] where [login] = %(login)s' % {'login': login}
    db = DatabaseConnection()
    db.open()
    result = (int(db.execute_scalar(query)) > 0)
    db.close()
    return result


def get_events(all_events=True, only_unknown_mac=False, started_at='', ended_at='', mac=''):
    """ Выборка событий из syslog'а:

   all_events          получать только c тэгами link-up и LINK_DOWN.
   only_unknown_mac    получить события только с неизвестными mac'ами.
   started_at          начало диапазона.
   ended_at            конец диапазона.

   По умолчанию в выборку попадают все события за последний два часа.
    """
    db = DatabaseConnection()
    query = ''

    if db.rdbms == 'sqlite':
        if started_at == '':
            started_at = 'datetime(\'now\',\'-2000 hour\', \'localtime\')'
        if ended_at == '':
            ended_at = 'datetime(\'now\', \'localtime\')'
    elif db.rdbms == 'postgresql':
        if started_at == '':
            started_at = 'current_timestamp + interval \'-2000 hour\''
        if ended_at == '':
            ended_at = 'current_timestamp'

    if db.rdbms == 'sqlite':
        query = '''select
            receivedat, '''
    elif db.rdbms == 'postgresql':
        query = '''select
            receivedat::timestamp(0) receivedat,'''

    query += '''priority,
            from_host,
            process,
            syslog_tag,
            case
                when mac_addresses.mac is null then ''
                when mac_addresses.wellknown = 1 then 'wellknown'
                when mac_addresses.mac is not null and (mac_addresses.wellknown is null or mac_addresses.wellknown = 0) then 'unknown'
            end mac_type,
            message,
            syslog.mac
        from
            syslog
            left join
            mac_addresses
            on upper(syslog.mac) = upper(mac_addresses.mac)
        where
            receivedat > %(started_at)s
            and
            receivedat < %(ended_at)s
        ''' % {'started_at': started_at, 'ended_at': ended_at}
    if not all_events:
        query += ' and (syslog_tag like \'%link-up%\' or syslog_tag like \'%LINK_DOWN%\')'
    if mac != '':
        query += 'and syslog.mac = %(mac)s' % {'mac': mac}

    query += ''' order by receivedat desc limit 500'''

    db.open()
    result = db.execute(query)
    db.close()
    # print(query)
    return result


def get_current_state(only_unknown=False):
    """  Выборка текущих подключений к сетевому оборудованию:

      from_host
      port
      mac
      mac_type
      manufacturer
      up_time

      Фильтр:
          only_unknown    только "недоверенные" mac-адресы.
    """

    query = '''select
                from_host,
                port,
                current_state.mac mac,
                case
                    when mac_addresses.mac is null then ''
                    when mac_addresses.wellknown = 1 then 'wellknown'
                    when mac_addresses.mac is not null and (mac_addresses.wellknown is null or mac_addresses.wellknown = 0) then 'unknown'
                end mac_type,
                manufacturer,
                started_at up_time
            from
                current_state
                join
                mac_addresses 
                on
                upper(current_state.mac) = upper(mac_addresses.mac)
                left join
                mac_owners
                on
                upper(substr(replace(mac_addresses.mac,':',''),1,6)) = mac_owners.mac
            where
                state = 1
                '''
    if only_unknown:
        query += " and mac_addresses.mac is not null and " \
                 "(mac_addresses.wellknown is null or mac_addresses.wellknown = 0) "

    query += "order by from_host, port"

    db = DatabaseConnection()
    db.open()
    result = db.execute(query)
    db.close()

    return result


def get_mac(status):
    """Выборка всех mac-адресов по критерию.

    В зависимости от переданного параметра:
    status = 'wellknown' - выборка доверенных маков.
    status = 'unknown'   - выборка недоверенных маков.
    """
    query_for_wellknown = '''select
                    mac_addresses.mac mac,
                    mac_addresses.wellknown_author wellknown_author,
                    mac_addresses.description description,
                    mac_addresses.wellknown_started_at wellknown_started_at,
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

    query_for_unknown = '''select
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
    db = DatabaseConnection()
    db.open()
    if status == 'wellknown':
        result = db.execute(query_for_wellknown)
    elif status == 'unknown':
        result = db.execute(query_for_unknown)
    db.close()

    return result


def set_mac_to_wellknown(mac, login, description):
    """Установка признака "доверенный" для mac-адреса."""
    db = DatabaseConnection()

    query = '''update
                        mac_addresses
                    set
                        wellknown = 1,
                        wellknown_author = '%(login)s',
                        description = '%(description)s',
            ''' % {'login': login, 'description': description}
    if db.rdbms == 'sqlite':
        query += '''wellknown_started_at = datetime('now','localtime')'''
    elif db.rdbms == 'postgresql':
        query += '''wellknown_started_at = current_timestamp'''

    query += ''' where
                        mac = '%(mac)s'
                ''' % {'mac': mac}

    db.open()
    db.execute_non_query(query)
    db.close()


def set_mac_to_unknown(mac, login):
    """Удаление признака "доверенный" для mac-адреса."""
    db = DatabaseConnection()

    query = '''update
                        mac_addresses
                    set
                        wellknown = 0,
                        wellknown_author = '%(login)s',
                        description = '',
            ''' % {'login': login}
    if db.rdbms == 'sqlite':
        query += '''wellknown_started_at = datetime('now','localtime')'''
    elif db.rdbms == 'postgresql':
        query += '''wellknown_started_at = current_timestamp'''

    query += ''' where
                        mac = '%(mac)s'
                    ''' % {'mac': mac}

    db.open()
    db.execute_non_query(query)
    db.close()


def flask_logon(login, hash_sha384):
    """Аутентификация."""
    query = '''
                select
                    count(1) _count
                from
                    admin
                where
                    login = '%(login)s'
                    and
                    hash = '%(hash)s'
            ''' % {'login': login, 'hash': hash_sha384}

    db = DatabaseConnection()
    db.open()
    result = (int(db.execute_scalar(query)) > 0)
    db.close()
    return result
