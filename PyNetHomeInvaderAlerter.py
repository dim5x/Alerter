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

""" Запись syslog'a в таблицу: 
        priority
	devicereportedtime
        receivedat
        fromhost
        process
        syslogtag
        message
"""

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

        # for debug
        '''
        with open('sys.log', 'a') as f:
            f.write(data+ '\n')
        '''

        # Parse
        event = re.search('(?P<priority><\d{,3}>)(?P<date>\w{,3}\s+\d{,2}\s+\d{,2}:\d{,2}:\d{2,2})(?P<fromhost>\s+[^:]+){0,1}\s+(?P<process>\S+:)(?P<syslogtag>\s+\S+:){0,1}\s+(?P<message>.+)', data)
        priority = event.group('priority').replace('<','').replace('>','')
        timestamp = datetime.datetime.strptime(str(datetime.datetime.now().year) + ' ' + event.group('date'), '%Y %b %d %H:%M:%S')
        devicereportedtime = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        fromhost = event.group('fromhost')
        process = event.group('process')
        syslogtag = event.group('syslogtag')
        message = event.group('message')
        cursor.execute("INSERT INTO syslog (priority,devicereportedtime,fromhost,process,syslogtag,message) VALUES (?,?,?,?,?,?)", (priority,devicereportedtime,fromhost,process,syslogtag,message))

        db.commit()
        

if __name__ == '__main__':
    try:
        db = sqlite3.connect('destination.db')
        server = MyUDPServer((HOST, PORT), SyslogUDPHandler, db)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('Ctrl+C Pressed. Shutting down.')
