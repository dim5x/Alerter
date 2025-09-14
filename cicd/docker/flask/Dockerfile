# Берем нужный базовый образ
FROM python:3.10-slim
# Копируем все файлы из текущей директории в /app контейнера
COPY /static/ /app/alerter/static/
COPY /templates/ /app/alerter/templates/
COPY ["*.py", "options.ini", "./cicd/docker/flask/requirements_flask.txt", "/app/alerter/"]

# Устанавливаем все зависимости
RUN pip install -r /app/alerter/requirements_flask.txt --no-cache-dir

# Устанавливаем приложение (Подробнее смотри Distutils)
WORKDIR /app/alerter

CMD ["python", "/app/alerter/web_view.py"]

# Говорим контейнеру какой порт слушай
EXPOSE 5000

