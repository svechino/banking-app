# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы в контейнер
COPY . .

# Загрузим переменные окружения
ENV PORT=8080

# Открываем порт для Dash
EXPOSE 8080

# Установка переменных окружения из файла .env
RUN pip install python-dotenv

# Запускаем приложение
CMD ["python","banking-app.py"]

