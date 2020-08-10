# Берем нужный базовый образ
FROM python:3.8-alpine
# Копируем все файлы из текущей директории в /app контейнера
COPY ./ /app
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# Устанавливаем все зависимости
RUN pip install -r /app/requirements.txt --no-cache-dir
# Устанавливаем приложение (Подробнее смотри Distutils)
RUN pip install -e /app
# Говорим контейнеру какой порт слушай
EXPOSE 5000
# Запуск нашего приложения при старте контейнера
CMD python /app/FlaskPNHIA.py

# В качестве альтернативы distutils можно просто указать что выполнить
#CMD python /app/src/app.py