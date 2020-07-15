import datetime
import socketserver

# HOST, PORT = 'x.x.x.x', 514
HOST, PORT = '192.168.0.3', 514


# HOST, PORT = 'localhost', 514


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        today = datetime.datetime.today()
        name_syslog_file = today.strftime('%Y-%m-%d') + '.log'
        with open(name_syslog_file, 'a') as f:
            if 'kernel: wlan0' in str(data):
                f.write('IP: ' + self.client_address[0] + '\t' + today.strftime('%Y-%m-%d %H:%M:%S') + '\t' + str(
                    data[19:]) + '\n')
                print(data)


if __name__ == '__main__':
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('Crtl+C Pressed. Shutting down.')
