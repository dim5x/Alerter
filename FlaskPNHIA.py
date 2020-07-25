from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.static_folder = r'templates\static'


# Форматы для тестирования:
# test_mac1 = 'F4:97:C2:34:67:90'
# test_mac2 = 'F4-97-C2-89-78-67'
# test_mac3 = 'F497C2897867'
def check_mac(s):
    if len(s) > 12:
        half_mac = ''.join((i for i in s[:8] if i.isalnum())).upper()
    else:
        half_mac = s[:6]
    with open('oui_min+.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            if half_mac in line:
                l = line.split()
                return ' '.join(l[1:])


# Главная страница.
# Вариант с файловым представлением сислога.
# @app.route('/', methods=['POST', 'GET'])
# def hello_world():
#     name_syslog_file = 'sys.log'
#     global allow_mac
#     global disallow_mac
#     try:
#         with open(name_syslog_file, 'r') as f, \
#                 open('allow_mac.txt', 'r') as am, \
#                 open('disallow_mac.txt', 'r') as dm:
#             data = reversed(f.readlines())
#             allow_mac = am.readlines()
#             disallow_mac = dm.readlines()
#         return render_template('index.html', data=data, allow_mac=allow_mac, disallow_mac=disallow_mac)
#     except FileNotFoundError:
#         return render_template('FileNotFoundError.html')

# Главная страница.
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    global data
    global allow_mac
    global disallow_mac
    conn = sqlite3.connect('destination.db')
    cursor = conn.cursor()

    data = list(cursor.execute('''SELECT event_time, 
                                        priority,                                    
                                        from_host,
                                        ip,
                                        process,
                                        syslog_tag,
                                        message
                                        FROM syslog'''))
    allow_mac = list(cursor.execute('SELECT mac,company,author,description,started_at FROM wellknown_mac'))
    disallow_mac = list(cursor.execute('SELECT mac, company FROM unknown_mac'))
    return render_template('index.html', data=reversed(data), allow_mac=allow_mac, disallow_mac=disallow_mac)


# # Заглушка страницы добавления.
# @app.route('/add_allow_mac.html', methods=['POST', 'GET'])
# def add_allow_mac():
#     global allow_mac
#     if request.method == 'POST':
#         if request.form['button'] == 'Добавить':
#             with open('allow_mac.txt', 'a') as f:
#                 mac = request.form['field']
#                 f.write(mac + '\n')
#             return redirect('/')
#     return render_template('add_allow_mac.html', allow_mac=allow_mac)

# Заглушка страницы добавления.
@app.route('/add_allow_mac.html', methods=['POST', 'GET'])
def add_allow_mac():
    if request.method == 'POST':
        if request.form['button'] == 'Добавить':
            db = sqlite3.connect('destination.db')
            cur = db.cursor()
            mac = request.form['field']
            author = request.form['author']
            description = request.form['description']
            company = check_mac(mac)
            cur.execute('INSERT INTO wellknown_mac (mac,company,author,description) VALUES (?,?,?,?)',
                        (mac, company, author, description))
            db.commit()
            return redirect('/')
    return render_template('add_allow_mac.html', allow_mac=allow_mac)


# # Заглушка страницы добавления
# @app.route('/add_disallow_mac.html', methods=['POST', 'GET'])
# def add_disallow_mac():
#     global allow_mac
#     if request.method == 'POST':
#         if request.form['button'] == 'Добавить':
#             with open('disallow_mac.txt', 'a') as f:
#                 mac = request.form['field']
#                 f.write(mac + '\n')
#             return redirect('/')
#     return render_template('add_disallow_mac.html', disallow_mac=disallow_mac)

# Заглушка страницы добавления.
@app.route('/add_disallow_mac.html', methods=['POST', 'GET'])
def add_disallow_mac():
    if request.method == 'POST':
        if request.form['button'] == 'Добавить':
            mac = request.form['field']
            company = check_mac(mac)
            db = sqlite3.connect('destination.db')
            cur = db.cursor()
            cur.execute('INSERT INTO unknown_mac (mac,company) VALUES (?,?)', (mac, company))
            db.commit()
            return redirect('/')
    return render_template('add_disallow_mac.html', disallow_mac=disallow_mac)


@app.route('/test')
def txt():
    return render_template('test.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
