# Берем нужный базовый образ
FROM python:3.8-alpine
# Копируем все файлы из текущей директории в /app контейнера
COPY ./ /app
WORKDIR /app
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# Устанавливаем все зависимости
RUN pip install -r /app/requirements.txt --no-cache-dir
# Устанавливаем приложение (Подробнее смотри Distutils)
CMD python /app/PyNetHomeInvaderAlerter.py
#&& python /app/FlaskPNHIA.py
# Говорим контейнеру какой порт слушай
EXPOSE 5000
EXPOSE 5140/udp
# Запуск нашего приложения при старте контейнера
#CMD web_server

# В качестве альтернативы distutils можно просто указать что выполнить
#CMD python /app/src/app.py