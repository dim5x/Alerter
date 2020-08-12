# Берем нужный базовый образ
FROM python:3.8-slim
# Копируем все файлы из текущей директории в /app контейнера
COPY ./ /app
RUN apt-get update && apt-get upgrade -y && apt-get install -y netcat-openbsd gcc && apt-get clean
# Устанавливаем все зависимости
RUN pip install -r /app/requirements.txt --no-cache-dir
# Устанавливаем приложение (Подробнее смотри Distutils)
WORKDIR /app
CMD python /app/FlaskPNHIA.py
#CMD python /app/FlaskPNHIA.py
# Говорим контейнеру какой порт слушай
EXPOSE 5000
# Запуск нашего приложения при старте контейнера
#CMD web_server

# В качестве альтернативы distutils можно просто указать что выполнить
#CMD python /app/src/app.py
