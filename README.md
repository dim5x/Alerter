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

Alerter — это инструмент для мониторинга и оповещения о сетевых событиях в локальной сети на основе входящих syslog-сообщений. Подходит для использования дома или в небольших офисах.

## 🚀 Возможности:

* Прием и хранение syslog-сообщений от сетевых устройств (например, роутеров).
* Веб-интерфейс для просмотра логов.
* Фильтрация по MAC-адресам, источникам и другим параметрам.
* Управление списком доверенных MAC-адресов.
* Авторизация пользователей.
* Развертывание через Docker.

## 🗂️ Структура проекта:

```
Alerter/
├── alerter.py           # SYSLOG-сервер
├── web_view.py          # Веб-интерфейс
├── static/              # Статические файлы (JS, CSS)
├── templates/           # HTML-шаблоны
├── cicd/                # Docker, CI/CD, тесты
├── global.config        # Глобальные настройки
└── options.ini          # Настройки веб-интерфейса
```

## 📦 Установка:

### 1. Клонируйте репозиторий:

```bash
git clone https://github.com/dim5x/Alerter.git
cd Alerter
```

### 2. Установите зависимости:

Для запуска вручную требуется Python 3.9+ и PostgreSQL. Установите зависимости:

```bash
pip install -r requirements.txt
```

### 3. Настройте базу данных PostgreSQL:
**NB**: База данных, учетные данные должны соответствовать указанным в настройках *.config.


Установка (для linux):
https://www.postgresql.org/download/linux/ubuntu/

Настройка базы данных:

3.1. Логинимся под системным пользователем:
```sh
 su - postgres
```

3.2. Запускаем утилиту:
```sh
psql
```

3.3. Создаём пользователя для сервиса:
```SQL
create user alerter with password 'alerter';
```

3.4. Создаём базу данных:
```SQL
create database alerter_destination;
```

3.5. Предоставляем пользователю права на базу данных:
```SQL
grant all privileges on database alerter_destination to alerter;
```

### 4. Настройте параметры подключения:
Прослушиваемый интерфейс:
```vi /etc/postgresql/10/main/postgresql.conf
listen_addresses = '*'
```
Предоставляем доступ, например, для всех пользователей во всей локальной сети:
```vi /etc/postgresql/10/main/pg_hba.conf
host	all	all	0.0.0.0/0	md5
```

### 5. Запустите сервер логов:
```bash
python3 alerter.py
```
* **Настройка:** в роутере прописать IP-адрес SYSLOG сервера.
* **Примечание:** роутер и ПК с которого запущен скрипт должны быть в одной сети.


### 6. Запустите веб-интерфейс:
```bash
python3 web_view.py
```

### 📦 Развертывание через Docker:
В каталоге `cicd` находятся Dockerfile и инструкции. Пример запуска:
```bash
cd cicd
docker-compose up --build
```

## 🌐 Веб-интерфейс:
Интерфейс доступен по адресу: [http://localhost:5000](http://localhost:5000)

Возможности:

* Просмотр логов в реальном времени
* Фильтрация по времени, источнику, MAC-адресу
* Управление белыми списками MAC-адресов

Скриншот:
<img src="https://github.com/dim5x/PyNetHomeInvaderAlerter/raw/master/archive/Screenshot7.PNG" alt="альтернативный текст">  

## 🧪 Тестирование:

В папке `cicd` есть инструменты и скрипты для тестирования, включая симуляцию syslog-сообщений.



## 🧑‍💻 Автор:

* Автор: [dim5x](https://github.com/dim5x)
* Соавтор : [Baron-Munchhausen](https://github.com/Baron-Munchhausen)
* Лицензия: Fuck license.

---

**Alerter** — ваш первый шаг к прозрачному мониторингу.
