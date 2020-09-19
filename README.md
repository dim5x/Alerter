[![Release](https://badgen.net/github/release/dim5x/PyNetHomeInvaderAlerter)]()
[![Lines of code](https://badgen.net/codeclimate/loc/dim5x/PyNetHomeInvaderAlerter)]()
[![Openned issues](https://badgen.net/github/open-issues/dim5x/PyNetHomeInvaderAlerter)]()
[![Closed issues](https://badgen.net/github/closed-issues/dim5x/PyNetHomeInvaderAlerter)]()
[![Commits](https://badgen.net/github/commits/dim5x/PyNetHomeInvaderAlerter)]()
[![License: Unlicense](https://img.shields.io/badge/Fuck%20license-Unlicense-brightgreen)](LICENSE)
[![Last commit](https://badgen.net/github/last-commit/dim5x/PyNetHomeInvaderAlerter)]()

[![Actions Status](https://github.com/dim5x/PyNetHomeInvaderAlerter/workflows/Run-tests-on-any-Push-event/badge.svg)](https://github.com/dim5x/PyNetHomeInvaderAlerter/actions)
[![Actions Status](https://github.com/dim5x/PyNetHomeInvaderAlerter/workflows/Publish-on-Docker-Hub/badge.svg)](https://github.com/dim5x/PyNetHomeInvaderAlerter/actions)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1711f11a97b84790b35dfc77a91f0893)](https://app.codacy.com/manual/dim5x/PyNetHomeInvaderAlerter?utm_source=github.com&utm_medium=referral&utm_content=dim5x/PyNetHomeInvaderAlerter&utm_campaign=Badge_Grade_Dashboard)
[![Maintainability](https://api.codeclimate.com/v1/badges/4cf97e39fba425223a49/maintainability)](https://codeclimate.com/github/dim5x/PyNetHomeInvaderAlerter/maintainability)
[![codecov](https://codecov.io/gh/dim5x/PyNetHomeInvaderAlerter/branch/master/graph/badge.svg)](https://codecov.io/gh/dim5x/PyNetHomeInvaderAlerter)

Alerter.py: [![Docker size](https://badgen.net/docker/size/dim5x/alerter)]()

Web_view: [![Docker size](https://badgen.net/docker/size/dim5x/flask)]()

<!--[![Docker size](https://badgen.net/codacy/coverage/9bafb2021af6488aba69eff6dd1dc173)]()-->


# PyNetHomeInvaderAlerter
<ol>
<li><h2>Запуск скрипта PyNetHomeInvaderAlerter.py.</h2></li>
<ul>
<li><b>Что делает:</b> собирает с роутера информацию, а-ля SYSLOG сервер. <del>Хранит в текстовом логе.</del> Хранит в БД.</li>
<li><b>Настройка:</b> в роутере прописать IP-адрес SYSLOG сервера.</li>
<li><b>Примечание:</b> роутер и комп с которого запущен скрипт должны быть в одной сети.</li>
</ul>
  
<li><h2>Запуск скрипта FlaskPNHIA.py.</h2></li>
<ul>
<li><b>Что делает:</b> отображает информацию из <s>текстового лога</s> БД. Позволяет залогиниться\разлогиниться. Добавить мак.</li>
<li><b>Формат:</b> <s>< IP-адрес источника > < Дата > < Событие ></s></li>
<li> [Дата] [Приоритет] [Откуда] [IP] [Процесс] [Тэг] [Сообщение] </li> 
</ul>

<li><h2>Файл xxxx-xx-xx.log </h2></li>
<ul>
<li><b>Что содержит:</b> тестовая информация для отображения.</li>
</ul>

<li><h2>Папка cicd.</h2></li>
<ul>
<li><b>Что содержит:</b> *.sql - для создания таблиц. Докерфайлы и зависимости для Docker. 
Юнит-тесты и утилиту для тестирования сислог сервера.</li> 
</ul>

<li><h2>Папка static.</h2></li>
<ul>
<li><b>Что содержит:</b> требуху для html-страниц: jquery-3.5.1, bootstrap, DataTables, фавикон и 404.</li> 
</ul>

<li><h2>Папка templates.</h2></li>
<ul>
<li><b>Что содержит:</b> собрание html-страниц для отображения информации.</li>
</ul>

<li><h2>Скриншот:</h2></li>
<img src="https://github.com/dim5x/PyNetHomeInvaderAlerter/raw/master/archive/Screenshot7.PNG" alt="альтернативный текст">  
</ol>

<h2>Настройка postgresql:</h2><br>
<tt><b>NB:</b> База данных, учетные данные должны соответствовать указанным в настройках *.config.<br>
</tt>
<ol>
  <li><b>Установка (для linux).</b><br>
https://www.postgresql.org/download/linux/ubuntu/</li>
  <li><b>Настройка базы данных:</b>
<ul>
<li>Логинимся под системным пользователем:<br>

```sh
su - postgres
```

</li>
<li>Запускаем утилиту:<br>

```sh
psql
```

</li>
<li>Создаем пользователя для сервиса:<br>

```SQL
create user alerter with password 'alerter';
```

</li>
<li>Создаем базу данных:<br>

```SQL
create database alerter_destination;
```

</li>
<li>Предоставляем пользователю права на базу данных:<br>

```SQL
grant all privileges on database alerter_destination to alerter;
```

</li>
</ul>

  <li><b>Настройка подключений:</b><br>
Прослушаваемый интерфейс:<br/>
<pre>vi /etc/postgresql/10/main/postgresql.conf
listen_addresses = '*'</pre>
Предоставляем доступ, например, для всех пользователей во всей локальной сети:<br>
<pre>vi /etc/postgresql/10/main/pg_hba.conf
host	all	all	0.0.0.0/0	md5</pre></li>
</ol>
