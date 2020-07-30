import socketserver
import sqlite3
import re
import os
from datetime import datetime
import db_management
import subprocess
import sys
import management

# Под виндой с 514-ым портом могут быть проблемы, нужно повышение привилегий.
# Заменить тем, что выше 1023-его.
# HOST, PORT = 'x.x.x.x', 514

# КМК должно быть типа такого:
# HOST, PORT, db_name = management.get_option()
# Соответственно, management.get_option() - выдаёт список или картеж из трёх элементов:
# типа: (127.0.0.1, 515 (сразу в формате int) и третий параметр с БД.)

HOST, PORT = management.get_option('alerter_host'), int(management.get_option('alerter_port'))
db_name = management.get_option('db_connection_string')

# заменить на TestConnection
if not os.path.exists(db_name):
    print('Нужна база!')
    try:
        subprocess.Popen([sys.executable, 'cicd/create_db.py'])
        print('База создана!')
        db = db_management.db_connection()
    except:
        print('Что-то пошло не так!')
else:
    db = db_management.db_connection()

db.open()


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())

        # Parse
        event = re.search(
            r'(?P<priority><\d{,3}>)(?P<date>\w{,3}\s+\d{,2}\s+\d{,2}:\d{,2}:\d{2,2})(?P<from_host>\s+[^:]+){0,'
            r'1}\s+(?P<process>\S+:)(?P<syslog_tag>\s+\S+:){0,1}\s+(?P<message>.+)', data)

        priority = event.group('priority').strip('><')
        device_time = datetime.strptime(str(datetime.now().year) + ' ' + event.group('date'), '%Y %b %d %H:%M:%S')

        if isinstance(event.group('from_host'), str):
            from_host = event.group('from_host')
        else:
            from_host = self.client_address[0]
        process = event.group('process')
        syslog_tag = event.group('syslog_tag')
        message = event.group('message')

        data_dic = {'priority': priority, 'device_time': device_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'from_host': from_host, 'process': process, 'syslog_tag': syslog_tag, 'message': message}
        db_management.insert_data(data_dic, 'syslog')

        print(data)  # отправка сообщений от sysloga в консоль для отладки.


if __name__ == '__main__':
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        print('Start server on: {}. Listening port: {}'.format(HOST, PORT))
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        db.close()
        print('Ctrl+C Pressed. Shutting down.')
