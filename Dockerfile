# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем все файлы в контейнер
COPY . .

# Открываем порт для Dash
EXPOSE 8050

# Запускаем приложение
CMD ["python", "banking-app.py"]