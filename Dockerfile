# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы в контейнер
COPY . .

# Открываем порт для Dash
EXPOSE 8050
# Загрузим переменные окружения
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Добавляем строки для загрузки переменных из файла .env
RUN pip install python-dotenv

# Запуск приложения
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "banking-app:server"]
CMD env && gunicorn -w 4 -b 0.0.0.0:8080 app:server

