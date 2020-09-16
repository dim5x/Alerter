# This Python file uses the following encoding: utf-8
"""Модуль для отображения текущего состояния, лога, управления маками."""
import hashlib
from flask import Flask, render_template, request, redirect, session
import management
import db_management

app = Flask(__name__)
# app.static_folder = r'static'  # определяем static папку для Flask, где лежат css и прочее.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # для работы session

data: list = []
state: list = []
allow_mac: list = []
disallow_mac: list = []
login: str = ''


# Страница логина.
@app.route('/', methods=['POST', 'GET'])
def login_admin():
    """Обрабатывает логин в систему. Считывает с формы логин/пароль (index.html).
    Проверяет в базе наличие хэша пароля. В случае успеха делает редирект на основную страницу.
    Помечает успешный залогин в кукисе session[login] = login.
    В противном случае - пишет Fail и отображает страницу ввода пароля снова."""
    message_for_user = ''
    session.clear()
    global login
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        password_hash = hashlib.sha3_384(bytes(password, encoding='UTF-8')).hexdigest()

        if db_management.flask_logon(login, password_hash):
            session[login] = login
            return redirect('/alerter')
        else:
            message_for_user = 'Fail.'
            return render_template('index.html', message=message_for_user)
    return render_template('index.html', message=message_for_user)


# Главная страница.
@app.route('/alerter', methods=['POST', 'GET'])
def hello_world():
    """ Отображает информацию из БД, в том случае, если осуществлен удачный логин. """
    if login in session:
        global data
        global state
        global allow_mac
        global disallow_mac

        data = db_management.get_events()
        state = db_management.get_current_state()

        allow_mac = db_management.get_wellknown_mac()
        disallow_mac = db_management.get_unknown_mac()

        return render_template('alerter.html', data=data, state=state, allow_mac=allow_mac,
                               disallow_mac=disallow_mac, login=login)
    return """
    <style> * {background: black; text-align:center; color: white;} a {color:blue;}</style>
    <h2>You are not <a href="/">logged in.</a></h2>
    """


# Заглушка страницы добавления хороших маков.
@app.route('/add_allow_mac.html', methods=['POST', 'GET'])
def add_allow_mac():
    """Добавляет мак в доверенные, в том случае, если успешен залогин.
    В качестве автора - проставляется тот, кто залогинился в систему."""
    editing_mac = request.args.get('editing_mac', '')
    if login in session:
        if request.method == 'POST':
            if request.form['button'] == 'Добавить':
                mac = request.form['field']
                description = request.form['description']
                db_management.set_mac_to_wellknown(mac, login, description)
                return redirect('/alerter')
    else:
        return redirect('/')
    return render_template('add_allow_mac.html', allow_mac=allow_mac, editing_mac=editing_mac)


# Заглушка страницы добавления плохих маков.
@app.route('/add_disallow_mac.html', methods=['POST', 'GET'])
def add_disallow_mac():
    """Добавляет плохие маки, если успешен залогин.
     Функционал сомнителен - ибо всё то же делается автоматически в БД.
    Вероятно, будет удалено/изменено просто на просмотр списка."""
    editing_mac = request.args.get('editing_mac', '')
    if login in session:
        if request.method == 'POST':
            if request.form['button'] == 'Добавить':
                mac = request.form['field']
                db_management.set_mac_to_unknown(mac, login)
                return redirect('/alerter')
    else:
        return redirect('/')
    return render_template('add_disallow_mac.html', disallow_mac=disallow_mac,
                           editing_mac=editing_mac)


# Страница регистрации нового пользователя.
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    """Осуществляет ригистрацию нового пользователя в системе.
    Фунционал работы с почтой не дописан. Под вопросом."""
    message = ''
    if request.method == 'POST':
        # name = request.form.get('name')
        # surname = request.form.get('surname')
        wanted_login = request.form.get('wanted_login')
        # email = request.form.get('wanted_login')
        if not db_management.login_exists(wanted_login):
            return '''
        <h2 style="text-align: center">Отослано. Ждите и усё будет!</h2>
        '''
        else:
            message = 'Логин занят.'
            return render_template('registration.html', message=message)
    return render_template('registration.html', message=message)


@app.route('/test')
def txt():
    """Для тестов."""

    data = db_management.get_events()
    return render_template('test.html', data=data)


@app.route('/test1')
def txt1():
    """Для тестов."""

    data = db_management.get_events()
    return render_template('test1.html', data=data)


@app.route('/test2')
def txt2():
    """Для тестов."""
    # data = ''
    data = db_management.get_events()
    return render_template('test2.html', data=data)


@app.route('/unit_test')
def unit_test():
    """Для юнит-теста."""
    return 'Hello World!'


# Страница 404.
@app.errorhandler(404)
def page_not_found(error):
    """Отображает страницу ошибки в случае перехода на несуществующую страницу."""
    return render_template('404.html', error=error), 404


if __name__ == '__main__':
    flask_host, flask_use_reloader = management.get_settings(['flask_host', 'flask_use_reloader'])
    app.run(debug=True, use_reloader=flask_use_reloader, host=flask_host)
