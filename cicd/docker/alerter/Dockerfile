# Берем нужный базовый образ
FROM python:3.10-slim
# Копируем все файлы из текущей директории в /app контейнера
COPY cicd/db /app/alerter/cicd/db
COPY ["*.py", "options.ini", "cicd/docker/alerter/requirements_alerter.txt", "/app/alerter/"]

# Устанавливаем все зависимости
RUN pip install -r /app/alerter/requirements_alerter.txt --no-cache-dir

# Устанавливаем приложение (Подробнее смотри Distutils)
WORKDIR /app/alerter

CMD ["python", "/app/alerter/alerter.py"]

# Говорим контейнеру какой порт слушай
EXPOSE 5140
