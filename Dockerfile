# Берем нужный базовый образ
FROM python:3.8-alpine
# Копируем все файлы из текущей директории в /app контейнера
COPY ./ /app
# Устанавливаем все зависимости
RUN apk update && pip install -r /app/requirements.txt --no-cache-dir
# Устанавливаем приложение (Подробнее смотри Distutils)
RUN pip install -e /app
# Говорим контейнеру какой порт слушай
EXPOSE 5000
# Запуск нашего приложения при старте контейнера
CMD python /app/FlaskPNHIA.py

# В качестве альтернативы distutils можно просто указать что выполнить
#CMD python /app/src/app.py