from flask import Flask, render_template, request, redirect, g
import datetime

allowMAC=['']
disallowMAC=['']

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    today = datetime.datetime.today()
    name_syslog_file = today.strftime('%Y-%m-%d') + '.log'
    with open(name_syslog_file, 'r') as f:
        s = f.readlines()
    return render_template('index.html', data=s, allowMAC=allowMAC, disallowMAC=disallowMAC)


if __name__ == '__main__':
    app.run()
