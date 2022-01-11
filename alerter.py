# This Python file uses the following encoding: utf-8
"""Модуль для обработки сообщений от сетевых железок."""

# Под Windows с 514-ым портом могут быть проблемы, нужно повышение привилегий.
# Можно заменить порт на тот, что выше 1023-его. На клиенте прописать аналогичный.
# HOST, PORT = 'x.x.x.x': str, 514: int

from configparser import ConfigParser
from datetime import datetime
import re
from rich.console import Console
import socketserver

import db_management


console = Console()
# from memory_profiler import memory_usage
TEMPLATE1 = '┌────┬────────────────────┬─────────────┬──────────────┬──────────────────────┐'
TEMPLATE2 = '│{:^4}│{:^19} │ {:^11} │ {:^12} │ {:^20} │'
TEMPLATE3 = '│{: <77}│'

config = ConfigParser()
config.read('options.ini')
# HOST, PORT = 'localhost', 5140
HOST, PORT = config['ALERTER']['host'], config['ALERTER']['port']

db = db_management.DatabaseConnection()
CONNECTION_RESULT = db.test_connection()

match CONNECTION_RESULT:
    case 'BASE EXISTS':
        print('База существует.')
    case 'BASE NOT EXISTS':
        db.create_db()
        print('База создана!')
    case ERROR:
        print(f'Что-то пошло не так! {ERROR}')

db.open()


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    """Класс Syslog сервера."""

    def handle(self):
        """Обработчик событий сислога."""
        data = bytes.decode(self.request[0].strip())

        # Parse
        event = re.search(
            r'(?P<priority><\d{,3}>)'
            r'(?P<date>\w{,3}\s+\d{,2}\s+\d{,2}:\d{,2}:\d{2})'
            r'(?P<from_host>\s+[^:]+)?\s+'
            r'((?P<process>\S+):)?'
            r'((?P<syslog_tag>\s+\S+):)? '
            r'(?P<message>.+)',
            data)

        device_time = datetime.strptime(str(datetime.now().year) + ' ' + event.group('date'), '%Y %b %d %H:%M:%S')

        if isinstance(event.group('from_host'), str):
            from_host = event.group('from_host')
        else:
            from_host = self.client_address[0]

        mac_re = re.search('(?P<mac>[0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5})', event.group('message'))
        if mac_re:
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

        if row['process'] == 'kernel':
            if db.rdbms == 'sqlite':
                db_management.insert_data(row, 'syslog')
            elif db.rdbms == 'postgresql':
                db_management.new_syslog_event(row, db)

        # print(data)  # отправка сообщений от sysloga в консоль для отладки.
        console.print(TEMPLATE1)
        console.print(TEMPLATE2.format(row['priority'] or '-',
                                       row['from_host'] or '-',
                                       row['process'] or '-',
                                       row['syslog_tag'] or '-',
                                       row['mac'] or '-'))
        console.print(TEMPLATE3.format(row['message'][:77] or '-'))


if __name__ == '__main__':
    try:
        server = socketserver.UDPServer((HOST, int(PORT)), SyslogUDPHandler)
        console.print(f'Start server on: {HOST}. Listening port: {PORT}')
        console.print(TEMPLATE1, style='bold magenta')
        console.print(TEMPLATE2.format('PR', 'FROM_HOST', 'PROCESS', 'SYSLOG_TAG', 'MAC'),
                      style='bold magenta')
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit) as error:
        print(error)
        if 'WinError 10048' in str(error):
            print('Что делать?: Остановите другой экземпляр скрипта, использующий сокет.')
        else:
            print("""Причина: вероятнее всего вы в разных подсетях с роутером, с которого принимаете события.
Что делать?: смените IP-адрес на адрес из подсети роутера и перезапустите alerter.py.""")
    except KeyboardInterrupt:
        db.close()
        print('Ctrl+C Pressed. Shutting down.')
