# Используем базовый образ Python 3.10
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /usr/src/

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . .

# Устанавливаем Poetry для управления зависимостями
RUN pip install poetry

# Устанавливаем зависимости проекта с помощью Poetry
RUN poetry config virtualenvs.create false && poetry install

# Собираем статические файлы (если нужно)
RUN poetry run python manage.py collectstatic --noinput

# Указываем, что контейнер прослушивает порт 8002
EXPOSE 8002

# Устанавливаем команду по умолчанию для запуска приложения на порту 8002, при использовании docker compose не пишется
#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8002"]
