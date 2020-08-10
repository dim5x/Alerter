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

<li><h2>Папка templates.</h2></li>
<ul>
<li><b>Что содержит:</b> собрание html-страниц для отображения информации.</li>
</ul>

<li><h2>Скриншот:</h2></li>
<img src="https://github.com/dim5x/PyNetHomeInvaderAlerter/raw/master/Screenshot.PNG" alt="альтернативный текст">  
</ol>

<h2>Настройка postgresql:</h2><br>
<tt><b>NB:</b> База данных, учетные данные должны соответствовать указанным в настройках *.config.<br>
</tt>
<ol>
  <li><b>Установка (для linux).</b><br>
https://www.postgresql.org/download/linux/ubuntu/</li>
  <li><b>Настройка базы данных:</b>
<ul>
<li>Логинимся под системным пользователем:<br></li>

```
su - postgres
```
<li>Запускаем утилиту:<br></li>

```
psql
```
<li>Создаем пользователя для сервиса:<br></li>

```SQL
create user alerter with password 'alerter';
```

<li>Создаем базу данных:<br></li>

```SQL
create database alerter_destination;
```

<li>Предоставляем пользователю права на базу данных:<br></li>

```SQL
grant all privileges on database alerter_destination to alerter;
```

</ul>

  <li><b>Настройка подключений:</b><br>
Прослушаваемый интерфейс:<br/>
<pre>vi /etc/postgresql/10/main/postgresql.conf
listen_addresses = '*'</pre>
Предоставляем доступ, например, для всех пользователей во всей локальной сети:<br>
<pre>vi /etc/postgresql/10/main/pg_hba.conf
host	all	all	0.0.0.0/0	md5</pre></li>
</ol>