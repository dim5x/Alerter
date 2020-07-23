import socketserver
import sqlite3

# Под виндой с 514-ым портом могут быть проблемы, нужно повышение привилегий.
# Заменить тем, что выше 1023-его.
# HOST, PORT = 'x.x.x.x', 514
HOST, PORT = '192.168.0.102', 5140
# my_branch test
# HOST, PORT = '172.27.0.165', 514

""" Создал табличку c именем syslog и полями: 
                            address = IP-адресс (доменное имя) 
                            source = источник события
                            event = сообщение о событии
                            event_time = время события"""

# c.execute('''CREATE TABLE syslog (id INTEGER PRIMARY KEY,
#                             address varchar(50),
#                             source varchar(20),
#                             event text,
#                             event_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) )''')


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        db = sqlite3.connect('destination_test.db')  # создаём коннект с базой
        cursor = db.cursor()  # создаём курсор

        # Вот так работает на моих данных:
        address = self.client_address[0]
        src, *event = data[19:35], data[35:]
        cursor.execute("INSERT INTO syslog (address,source,event) VALUES (?,?,?)", (address, src, str(event)))

        # Вот так должно заработать на твоих данных:
        # address, src, *event = data.split()
        # cursor.execute("INSERT INTO syslog (address,source,event) VALUES (?,?,?)", (address, src, str(event)))

        db.commit()
        db.close()
        # print(data) # отправка сообщений от sysloga в консоль для отладки.


if __name__ == '__main__':
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('Ctrl+C Pressed. Shutting down.')
