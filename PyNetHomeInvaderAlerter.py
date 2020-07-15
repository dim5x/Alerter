import datetime
import socketserver
from flask import Flask, render_template, request, redirect, g

# HOST, PORT = 'x.x.x.x', 514
HOST, PORT = '192.168.0.3', 514

app = Flask(__name__)


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        today = datetime.datetime.today()
        name_syslog_file = today.strftime('%Y-%m-%d') + '.log'
        with open(name_syslog_file, 'a') as f:
            f.write(self.client_address[0] + '\t' + today.strftime('%Y-%m-%d %H:%M:%S') + '\t' + str(data) + '\n')
            if 'kernel' in str(data):
                print(data)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    today = datetime.datetime.today()
    name_syslog_file = today.strftime('%Y-%m-%d') + '.log'
    with open(name_syslog_file, 'r') as f:
        s = f.read()
    return render_template('index.html', data=s)


if __name__ == '__main__':
    app.run(debug=False)
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)

    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('Crtl+C Pressed. Shutting down.')
