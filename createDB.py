import sqlite3

""" Создал табличку c именем syslog и полями: 
                            id
                            priority = приоритет
                            event_time = время события
                            fromhost = IP-адресс (доменное имя) 
                            syslogtag = источник события
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
                        event_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','localtime')),
                        fromhost varchar(200),
                        syslogtag varchar(50),
                        message varchar(400),
                        mac_allow varchar(17),
                        mac_disallow varchar(17),
                        rez text)''')
db.commit()
db.close()
