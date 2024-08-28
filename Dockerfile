# Используйте официальный Ubuntu базовый образ
FROM python:3.11

# Установите системные зависимости
RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Установите Poetry
RUN pip3 install poetry && \
    poetry config virtualenvs.create false



# Установите другие зависимости вашего проекта
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

# Копируйте файлы проекта
COPY . .

# Откройте порт 8000
EXPOSE 8000

# Команда для запуска сервера
CMD ["sh", "-c", "python3 app_parking/manage.py makemigrations && python3 app_parking/manage.py migrate && python3 app_parking/manage.py runserver 0.0.0.0:8000"]