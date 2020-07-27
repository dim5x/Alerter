from flask import Flask, render_template, request, redirect, session
# from flask_login import LoginManager
import sqlite3
import hashlib
import management
import db_management

app = Flask(__name__)
app.static_folder = r'templates\static'  # определяем static папку для Flask, где лежат css и прочее.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # для работы session

global data
global allow_mac
global disallow_mac
login = ''


def check_mac(s):
    """ Return company name of the MAC
    Форматы для тестирования:
        test_mac1 = 'F4:97:C2:34:67:90'
        test_mac2 = 'F4-97-C2-89-78-67'
        test_mac3 = 'F497C2897867
    """
    if len(s) > 12:
        half_mac = ''.join((i for i in s[:8] if i.isalnum())).upper()
    else:
        half_mac = s[:6]
    with open('oui_min+.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            if half_mac in line:
                lo = line.split()
                return ' '.join(lo[1:])


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
@app.route('/alerter', methods=['POST', 'GET'])
def hello_world():
    if login in session:
        global data
        global allow_mac
        global disallow_mac
        #conn = sqlite3.connect('destination.db')
        #cursor = conn.cursor()

       # data = list(cursor.execute('''SELECT device_time, 
       #                                     priority,                                    
       #                                     from_host,
       #                                     process,
       #                                     syslog_tag,
       #                                     message
       #                                     FROM syslog'''))
        # data = db_management.get_events(link,start,end)
        data = db_management.get_events()
       # allow_mac = list(cursor.execute('SELECT mac FROM mac_addresses where wellknown = 1'))
        allow_mac = db_management.get_wellknown_mac()
       # disallow_mac = list(cursor.execute('SELECT mac FROM mac_addresses where wellknown = 0 or wellknown is null'))
        disallow_mac = db_management.get_unknown_mac()
       
        return render_template('alerter.html', data=reversed(data), allow_mac=allow_mac, disallow_mac=disallow_mac,
                               login=login)
    return 'You are not logged in'


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
    if login in session:
        if request.method == 'POST':
            if request.form['button'] == 'Добавить':
                db = sqlite3.connect('destination.db')
                cur = db.cursor()
                mac = request.form['field']
                # author = request.form['author']
                author = login
                description = request.form['description']
                company = check_mac(mac)
                cur.execute('INSERT INTO wellknown_mac (mac,company,author,description) VALUES (?,?,?,?)',
                            (mac, company, author, description))
                db.commit()
                return redirect('/alerter')
    else:
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
    if login in session:
        if request.method == 'POST':
            if request.form['button'] == 'Добавить':
                mac = request.form['field']
                company = check_mac(mac)
                db = sqlite3.connect('destination.db')
                cur = db.cursor()
                cur.execute('INSERT INTO unknown_mac (mac,company) VALUES (?,?)', (mac, company))
                db.commit()
                return redirect('/alerter')
    else:
        return redirect('/')
    return render_template('add_disallow_mac.html', disallow_mac=disallow_mac)


@app.route('/test')
def txt():
    return render_template('test.html', data=data)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    message = ''
    if request.method == 'POST':
        #j = []
        #db = sqlite3.connect('destination.db')
        #cur = db.cursor()
        name = request.form.get('name')
        surname = request.form.get('surname')
        wanted_login = request.form.get('wanted_login')
        email = request.form.get('wanted_login')
        #l = list(cur.execute('SELECT login FROM admin'))
        #print(l)
        #for i in l:
        #    j.append(str(i)[2:-3])
        #print(j)
        #if wanted_login not in j:
        if not db_management.login_exists(wanted_login):
            return '''
        <h2 style="text-align: center">Отослано. Ждите и усё будет!</h2>
        '''
        else:
            message = 'Логин занят.'
            render_template('registration.html', message=message)
    return render_template('registration.html', message=message)


@app.route('/', methods=['POST', 'GET'])
def login_admin():
    message = ''
    session.clear()
    global login
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        password_hash = hashlib.sha3_384(bytes(password, encoding='UTF-8')).hexdigest()

        db = sqlite3.connect('destination.db')
        cur = db.cursor()
        hash_in_base = list(cur.execute('SELECT hash FROM admin WHERE login=?', (login,)))
        if password_hash == (str(hash_in_base)[3:-4]):
            session[login] = login
            return redirect('/alerter')
        else:
            message = 'Fail.'
            return render_template('index.html', message=message)
    return render_template('index.html', message=message)


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('FileNotFoundError.html'), 404


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect('/')
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''


if __name__ == '__main__':
    flask_host = management.get_option('flask_host')
    print(flask_host)
    #
    app.run(debug=True, use_reloader=True,host=flask_host)
