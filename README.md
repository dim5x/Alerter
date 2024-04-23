[![Openned issues](https://badgen.net/github/open-issues/dim5x/PyNetHomeInvaderAlerter)]()
[![Closed issues](https://badgen.net/github/closed-issues/dim5x/PyNetHomeInvaderAlerter)]()
[![Lines of code](https://badgen.net/codeclimate/loc/dim5x/PyNetHomeInvaderAlerter)]()
[![Commits](https://badgen.net/github/commits/dim5x/PyNetHomeInvaderAlerter)]()
[![License: Unlicense](https://img.shields.io/badge/Fuck%20license-Unlicense-brightgreen)](LICENSE)
[![Last commit](https://badgen.net/github/last-commit/dim5x/PyNetHomeInvaderAlerter)]()

<!--[![Actions Status](https://github.com/dim5x/PyNetHomeInvaderAlerter/workflows/Publish-on-Docker-Hub/badge.svg)](https://github.com/dim5x/PyNetHomeInvaderAlerter/actions)-->
[![Actions Status](https://github.com/dim5x/PyNetHomeInvaderAlerter/workflows/Run-tests-on-Push/badge.svg)](https://github.com/dim5x/PyNetHomeInvaderAlerter/actions)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/4bb2e27ce5df492495a6e6d479bdc86f)](https://www.codacy.com/manual/dim5x/PyNetHomeInvaderAlerter/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dim5x/PyNetHomeInvaderAlerter&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/2e0f5a54936d9ff63335/maintainability)](https://codeclimate.com/github/dim5x/PyNetHomeInvaderAlerter/maintainability)<!--[![codecov](https://codecov.io/gh/dim5x/PyNetHomeInvaderAlerter/branch/master/graph/badge.svg)](https://codecov.io/gh/dim5x/PyNetHomeInvaderAlerter)-->

[![Docker size](https://badgen.net/docker/size/dim5x/alerter)]() - Alerter.

[![Docker size](https://badgen.net/docker/size/dim5x/flask)]() - Web_view.

<!--[![Docker size](https://badgen.net/codacy/coverage/9bafb2021af6488aba69eff6dd1dc173)]()-->

# Alerter
<ol>
<li><h2>Запуск скрипта alerter.py.</h2></li>
<ul>
<li><b>Что делает:</b> собирает с роутера информацию, à la SYSLOG-сервер. <del>Хранит в текстовом логе.</del> Хранит в БД.</li>
<li><b>Настройка:</b> в роутере прописать IP-адрес SYSLOG сервера.</li>
<li><b>Примечание:</b> роутер и ПК с которого запущен скрипт должны быть в одной сети.</li>
</ul>
  
<li><h2>Запуск скрипта web_view.py.</h2></li>
<ul>
<li><b>Что делает:</b> отображает информацию из <s>текстового лога</s> БД. Позволяет залогиниться \ разлогиниться. Добавить \ удалить мак.</li>
<li><b>Формат:</b> <s>< IP-адрес источника > < Дата > < Событие ></s></li>
<li> [Дата] [Приоритет] [Откуда] [IP] [Процесс] [Тэг] [Сообщение] </li> 
</ul>

<li><h2>Папка cicd.</h2></li>
<b>Что содержит:</b>
<ul>
<li> Файлы *.sql - для создания таблиц. 
<li> Dockerfile и зависимости для Docker. 
<li> Юнит-тесты и утилиту для тестирования syslog-сервера.</li> 
</ul>

<li><h2>Папка static.</h2></li>
<b>Что содержит:</b>
<ul>
<li> требуху для html-страниц: jquery, bootstrap, DataTables, фавикон и 404.</li> 
</ul>

<li><h2>Папка templates.</h2></li>
<b>Что содержит:</b>
<ul>
<li> собрание html-страниц для отображения информации.</li>
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
