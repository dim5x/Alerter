import socketserver
import sqlite3
import re

# Под виндой с 514-ым портом могут быть проблемы, нужно повышение привилегий.
# Заменить тем, что выше 1023-его.
# HOST, PORT = 'x.x.x.x', 514
HOST, PORT = '192.168.0.102', 5140
# my_branch test
# HOST, PORT = '172.27.0.165', 514

db = sqlite3.connect('destination.db')  # создаём коннект с базой
cursor = db.cursor()  # создаём курсор


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())

        pattern = r'(<\d{,3}>)(\w{,3}\s+\d{,2}\s+\d{,2}:\d{,2}:\d{2,2})\s+(\S{1,})\s+(\S{1,})\s+(.+)'
        event = re.search(pattern, data)
        priority = event.group(1).replace('<', '').replace('>', '')
        fromhost = event.group(3)
        syslogtag = event.group(4)
        message = event.group(5)

        cursor.execute("INSERT INTO syslog (priority,fromhost,syslogtag,message) VALUES (?,?,?,?)",
                       (priority, fromhost, syslogtag, message))

        db.commit()

        print(data)  # отправка сообщений от sysloga в консоль для отладки.


if __name__ == '__main__':
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        db.close()
        print('Ctrl+C Pressed. Shutting down.')
