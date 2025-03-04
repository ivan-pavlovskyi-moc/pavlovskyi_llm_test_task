import openai  
import os  

# Отримуємо API-ключ із змінних середовища (якщо використовується)
OPENAI_API_KEY = os.getenv("Osk-proj-YH4pOiR8O1wpkbG5uU8J_0ajDHQuYOW_IjQ3ak15dMGnQ6AS52PGy-fMpBxANBf0Ylfu-38suKT3BlbkFJRNOw4bZFKdrJV78buel5sNlSXHqr0W0AtgyheFgsBIsr-vZdd7mwBP7sl959vY6lXoAnI0z8sA")

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
