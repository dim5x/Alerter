from flask import Flask, render_template
import datetime

# Тестовые МАК адреса для отображения:
allow_mac = ['84:85:06:21:d5:5a']
disallow_mac = ['00:25:06:11:d5:00', '08:75:56:11:11:11']

app = Flask(__name__)


# Главная страница.
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    today = datetime.datetime.today()
    name_syslog_file = today.strftime('%Y-%m-%d') + '.log'
    with open(name_syslog_file, 'r') as f:
        s = reversed(f.readlines())
    return render_template('index.html', data=s, allow_mac=allow_mac, disallow_mac=disallow_mac)


# Заглушка страницы добавления.
@app.route('/add_allow_mac', methods=['POST', 'GET'])
def add_allow_mac():
    return render_template('add_allow_mac.html', allow_mac=allow_mac)


# Заглушка страницы добавления.
@app.route('/add_disallowMAC', methods=['POST', 'GET'])
def add_disallow_mac():
    return render_template('add_disallow_mac.html', disallow_mac=disallow_mac)


if __name__ == '__main__':
    app.run()
