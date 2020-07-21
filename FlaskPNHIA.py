from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.static_folder = r'templates\static'


# Главная страница.
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    name_syslog_file = 'sys.log'
    global allow_mac
    global disallow_mac
    try:
        with open(name_syslog_file, 'r') as f, \
                open('allow_mac.txt', 'r') as am, \
                open('disallow_mac.txt', 'r') as dm:
            data = reversed(f.readlines())
            allow_mac = am.readlines()
            disallow_mac = dm.readlines()
        return render_template('index.html', data=data, allow_mac=allow_mac, disallow_mac=disallow_mac)
    except FileNotFoundError:
        return render_template('FileNotFoundError.html')


# Заглушка страницы добавления.
@app.route('/add_allow_mac.html', methods=['POST', 'GET'])
def add_allow_mac():
    global allow_mac
    if request.method == 'POST':
        if request.form['button'] == 'Добавить':
            with open('allow_mac.txt', 'a') as f:
                mac = request.form['field']
                f.write(mac + '\n')
            return redirect('/')
    return render_template('add_allow_mac.html', allow_mac=allow_mac)


# Заглушка страницы добавления.
@app.route('/add_disallow_mac.html', methods=['POST', 'GET'])
def add_disallow_mac():
    global allow_mac
    if request.method == 'POST':
        if request.form['button'] == 'Добавить':
            with open('disallow_mac.txt', 'a') as f:
                mac = request.form['field']
                f.write(mac + '\n')
            return redirect('/')
    return render_template('add_disallow_mac.html', disallow_mac=disallow_mac)


# @app.route('/allow_mac.txt')
# def txt():
#     return render_template('allow_mac.txt')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
