import sqlite3

""" Табличка c именем syslog и полями: 
                            id
                            priority = приоритет
                            device_time = время с железки
                            process = источник события
                            event_time = время события
                            ip = IP-адрес 
                            from_host = (доменное имя?) | переименовать в device_name? 
                            syslog_tag = тег события
                            message = сообщение о событии
                            mac_allow = разрешенные маки
                            mac_disallow = неразрешенные маки
                            rez = резерв
                            """
db = sqlite3.connect('destination.db')  # создаём коннект с базой
cursor = db.cursor()  # создаём курсор

# SQL- запрос на создание:
cursor.execute('''CREATE TABLE IF NOT EXISTS syslog (id INTEGER PRIMARY KEY,
                        priority integer,
                        device_time DATETIME, 
                        event_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','localtime')),
                        from_host varchar(200),
                        ip varchar(15),
                        process text,
                        syslog_tag varchar(50),
                        message varchar(400),                        
                        rez text)''')

# Табличка для маков:
cursor.execute('''CREATE TABLE IF NOT EXISTS unknown_mac (id INTEGER PRIMARY KEY,
                        mac varchar(17),
                        started at DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','localtime')),
                        company text)''')

cursor.execute('INSERT INTO unknown_mac (mac, company) VALUES (?,?)', ('23:34:56:32:23:45', 'apple'))

cursor.execute('''CREATE TABLE IF NOT EXISTS wellknown_mac  (id INTEGER PRIMARY KEY,
                        mac varchar(17),
                        company text,
                        description text,                        
                        started_at DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','localtime')),
                        ended_at DATETIME,
                        author varchar(20))''')
cursor.execute('INSERT INTO wellknown_mac (mac, company,description,author) VALUES (?,?,?,?)',
               ('23:34:56:32:23:45', 'apple', 'Зу-зу-зу', 'Василий'))

db.commit()
db.close()
