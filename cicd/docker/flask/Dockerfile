# Берем нужный базовый образ
FROM python:3.10-slim

WORKDIR /app/alerter

# Копируем зависимости сначала (для кэширования)
COPY cicd/docker/flask/requirements_flask.txt .

# Устанавливаем зависимости
RUN pip install -r requirements_flask.txt --no-cache-dir

# Копируем код приложения
COPY /static/ /app/alerter/static/
COPY /templates/ /app/alerter/templates/
COPY web_view.py options.ini ./

# Говорим контейнеру какой порт слушать
EXPOSE 5000

CMD ["python", "/app/alerter/web_view.py"]
