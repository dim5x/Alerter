import socketserver
import re
import subprocess
import sys
from datetime import datetime

import db_management
import management

# Под виндой с 514-ым портом могут быть проблемы, нужно повышение привилегий.
# Заменить тем, что выше 1023-его.
# HOST, PORT = 'x.x.x.x', 514

HOST, PORT = management.get_settings(['alerter_host', 'alerter_port'])

db = db_management.db_connection()

if db.test_connection() == 1:
    try:
        db.create_db()
        print('База создана!')
    except:
        print('Что-то пошло не так!')

db.open()


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())

        # Parse
        event = re.search(
            r'(?P<priority><\d{,3}>)(?P<date>\w{,3}\s+\d{,2}\s+\d{,2}:\d{,2}:\d{2,2})(?P<from_host>\s+[^:]+){,1}\s+'
            r'((?P<process>\S+):){,1}((?P<syslog_tag>\s+\S+):){,1} (?P<message>.+)', data)

        device_time = datetime.strptime(str(datetime.now().year) + ' ' + event.group('date'), '%Y %b %d %H:%M:%S')

        if isinstance(event.group('from_host'), str):
            from_host = event.group('from_host')
        else:
            from_host = self.client_address[0]

        mac_re = re.search('(?P<mac>([0-9a-fA-F]{2}([:-]|$)){6}$|([0-9a-fA-F]{4}([.]|$)){3})', event.group('message'))
        if mac_re is not None:
            mac = mac_re.group('mac')
        else:
            mac = None

        row = {'priority': event.group('priority').strip('><'),
               'device_time': device_time.strftime('%Y-%m-%d %H:%M:%S'),
               'from_host': from_host,
               'process': event.group('process'),
               'syslog_tag': event.group('syslog_tag'),
               'message': event.group('message'),
               'mac': mac}

        db_management.insert_data(row, 'syslog')

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
