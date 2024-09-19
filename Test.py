import openai
from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not found. Please check file .env")

# Настраиваем OpenAI API ключ
openai.api_key = OPENAI_API_KEY

# Создаем запрос к модели
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a bank information researcher."},
        {"role": "user", "content": "Find the latest news and trends about HSBC."}
    ]
)

# Выводим результат
print(response['choices'][0]['message']['content'])