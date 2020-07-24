import sqlite3

""" Табличка c именем syslog и полями: 
                            id
                            priority = приоритет
                            devicereportedtime = время с железки
                            process = источник события
                            event_time = время события
                            ip = IP-адрес 
                            fromhost = (доменное имя?) | переименовать в device_name? 
                            syslogtag = тег события
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
                        devicereportedtime DATETIME, 
                        event_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','localtime')),
                        fromhost varchar(200),
                        ip varchar(15),
                        process text,
                        syslogtag varchar(50),
                        message varchar(400),                        
                        rez text)''')

# Табличка для маков:
cursor.execute('''CREATE TABLE IF NOT EXISTS mac (id INTEGER PRIMARY KEY,
                        event_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','localtime')),
                        allow_mac varchar(17),
                        disallow_mac varchar(17))''')
cursor.execute('INSERT INTO mac (allow_mac, disallow_mac) VALUES (?,?)', ('23:34:56:32:23:45', '00:00:56:32:23:77'))

db.commit()
db.close()
