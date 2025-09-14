# Берем нужный базовый образ
FROM python:3.10-slim

WORKDIR /app/alerter

# Копируем зависимости сначала (для кэширования)
COPY cicd/docker/alerter/requirements_alerter.txt .

# Устанавливаем все зависимости
RUN pip install -r /app/alerter/requirements_alerter.txt --no-cache-dir

# Копируем код приложения
COPY cicd/db /app/alerter/cicd/db
COPY alerter.py db_management.py options.ini ./

# Говорим контейнеру какой порт слушай
EXPOSE 5140

CMD ["python", "/app/alerter/alerter.py"]
