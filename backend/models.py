import openai
import os

# Отримуємо API-ключ із змінних середовища
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Перевіряємо, чи ключ встановлений
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не встановлений! Додай його в середовище.")

# Створюємо клієнта OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_sql(nl_query: str) -> str:
    """
    Перетворює природномовний запит у SQL за допомогою OpenAI API.
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Ти SQL-асистент. Генеруй коректні SQL-запити."},
            {"role": "user", "content": nl_query}
        ]
    )
    
    # Отримуємо текст відповіді
    sql_query = response.choices[0].message.content.strip()
    return sql_query
