"""
Под виндой с 514-ым портом могут быть проблемы, нужно повышение привилегий.
Заменить тем, что выше 1023-его.
HOST, PORT = 'x.x.x.x', 514
"""
# from memory_profiler import memory_usage
import socketserver
import re
from datetime import datetime

import db_management
import management

HOST, PORT = management.get_settings(['alerter_host', 'alerter_port'])

db = db_management.db_connection()
CONNECTION_RESULT = db.test_connection()

TEMPLATE = '{:2} |{:^16} | {:^9} | {:^10} | {:^17} | {}'

if CONNECTION_RESULT == 1:
    try:
        db.create_db()
        print('База создана!')
    except Exception as error:
        print('Что-то пошло не так!', error)
elif CONNECTION_RESULT == 2:
    print('Что-то пошло не так!')

db.open()


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    """Класс Syslog сервера"""

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

        mac_re = re.search('(?P<mac>[0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5})', event.group('message'))
        if mac_re is not None:
            mac = mac_re.group('mac').upper()
        else:
            mac = None

        row = {'priority': event.group('priority').strip('><'),
               'device_time': device_time.strftime('%Y-%m-%d %H:%M:%S'),
               'from_host': from_host,
               'process': event.group('process'),
               'syslog_tag': event.group('syslog_tag'),
               'message': event.group('message'),
               'mac': mac}

        if db.rdbms == 'sqlite':
            db_management.insert_data(row, 'syslog')
        elif db.rdbms == 'postgresql':
            db_management.new_syslog_event(row, db)

        print(data)  # отправка сообщений от sysloga в консоль для отладки.
        #print(TEMPLATE.format(row['priority'], row['from_host'], row['process'],
        #                      row['syslog_tag'], row['mac'] or 'None', row['message']))


if __name__ == '__main__':
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        print('Start server on: {}. Listening port: {}'.format(HOST, PORT))
        print(TEMPLATE.format('pr', 'from_host', 'process', 'syslog_tag', 'mac', 'message'))
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise Exception
    except KeyboardInterrupt:
        db.close()
        print('Ctrl+C Pressed. Shutting down.')
