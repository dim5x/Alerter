import socketserver
import sqlite3
import re
import datetime

# Под виндой с 514-ым портом могут быть проблемы, нужно повышение привилегий.
# Заменить тем, что выше 1023-его.
# HOST, PORT = 'x.x.x.x', 514
#HOST, PORT = '192.168.0.102', 5140
# my_branch test
HOST, PORT = '172.27.0.165', 514

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

class MyUDPServer(socketserver.UDPServer):
    def __init__(self, server_address, RequestHandlerClass, db, bind_and_activate=True):
        socketserver.UDPServer.__init__(self, server_address, RequestHandlerClass)
        self.db = db
    def server_close(self):
        socketserver.UDPServer.server_close()
        db.close()


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        cursor = self.server.db.cursor()  # создаём курсор

        # Вот так работает на моих данных:
        # address = self.client_address[0]
        # src, *event = data[19:35], data[35:]
        # cursor.execute("INSERT INTO syslog (address,source,event) VALUES (?,?,?)", (address, src, str(event)))
       
        # Вот так должно заработать на твоих данных:
        event = re.search('(<\d{,3}>)(\w{,3}\s+\d{,2}\s+\d{,2}:\d{,2}:\d{2,2})\s+(\S{1,})\s+(\S{1,})\s+(.+)', str(data[:]))
        priority = event.group(1).replace('<','').replace('>','')
        timestamp = datetime.datetime.strptime(str(datetime.datetime.now().year) + ' ' + event.group(2), '%Y %b %d %H:%M:%S')
        receivedat = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        fromhost = event.group(3)
        syslogtag = event.group(4)
        message = event.group(5)
        cursor.execute("INSERT INTO systemevents (priority,receivedat,fromhost,syslogtag,message) VALUES (?,?,?,?,?)", (priority,receivedat,fromhost,syslogtag,message))

        db.commit()
        # for debug
        '''
        with open('sys.log', 'a') as f:
            f.write(str(data[:]) + '\n')
            f.write(priority + '\t' + receivedat  + '\t' + fromhost + '\t' + syslogtag + '\t' + message + '\n')
        '''

if __name__ == '__main__':
    try:
        db = sqlite3.connect('destination_test.db')
        server = MyUDPServer((HOST, PORT), SyslogUDPHandler, db)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('Ctrl+C Pressed. Shutting down.')
