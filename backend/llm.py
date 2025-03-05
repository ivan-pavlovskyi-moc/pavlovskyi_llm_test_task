import openai  
import os  
from dotenv import load_dotenv  

# Завантажуємо змінні середовища з .env  
load_dotenv()  

# Отримуємо API-ключ  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  

if not OPENAI_API_KEY:
    raise ValueError("API-ключ OpenAI не знайдено. Додай його в .env")

# Створюємо клієнт OpenAI  
client = openai.OpenAI(api_key=OPENAI_API_KEY)  

def generate_sql(nl_query: str) -> str:  
    """  
    Перетворює природномовний запит у SQL за допомогою OpenAI API.  
    """  
    response = client.chat.completions.create(  
        model="gpt-4",  
        messages=[  
            {"role": "system", "content": "Ти SQL-асистент. Генеруй коректні SQL-запити."},  
            {"role": "user", "content": nl_query}  
        ]  
    )  

    # Отримуємо текст відповіді  
    sql_query = response.choices[0].message.content.strip()  
    return sql_query  
