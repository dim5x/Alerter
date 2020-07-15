from flask import Flask, render_template
import datetime

# Тестовые МАК адреса для отображения:
allowMAC = ['84:85:06:21:d5:5a']
disallowMAC = ['00:25:06:11:d5:00', '08:75:56:11:11:11']

app = Flask(__name__)


# Главная страница.
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    today = datetime.datetime.today()
    name_syslog_file = today.strftime('%Y-%m-%d') + '.log'
    with open(name_syslog_file, 'r') as f:
        s = reversed(f.readlines())
    return render_template('index.html', data=s, allowMAC=allowMAC, disallowMAC=disallowMAC)


# Заглушка страницы добавления.
@app.route('/add_allowMAC', methods=['POST', 'GET'])
def add_allowMAC():
    return render_template('add_allowMAC.html', allowMAC=allowMAC)


# Заглушка страницы добавления.
@app.route('/add_disallowMAC', methods=['POST', 'GET'])
def add_disallowMAC():
    return render_template('add_disallowMAC.html', disallowMAC=disallowMAC)


if __name__ == '__main__':
    app.run()
