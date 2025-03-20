from fastapi import HTTPException
import logging
from sqlalchemy.sql import text
import requests
import json
from typing import List, Optional
from .db import Dish, Restaurant, AsyncSession
from fastapi.responses import JSONResponse

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Аналіз вхідного тексту за допомогою Ollama
def analyze_input_with_ollama(input_text: str) -> dict:
    """
    Аналізує вхідний текст за допомогою Ollama та повертає структуровані умови.
    """
    prompt = f"""
Проаналізуй наступний запит і витягни умови для пошуку страв:
- Тип страви (Main Course, Side, Drink, Dessert) — лише якщо явно вказано.
- Назва страви (наприклад, "Cheeseburger", "Caesar Salad") — лише якщо явно вказано.
- Діапазон цін (наприклад, "under $5", "up to 10 dollars", "less than 15 dollars") — лише якщо явно вказано.
- Діапазон калорій (наприклад, "less than 300 calories", "more than 500 calories") — лише якщо явно вказано.
- Час прийому їжі (наприклад, "breakfast", "lunch", "dinner") — лише якщо явно вказано.
- Категорія страви (наприклад, "burgers", "pizza", "coffee") — лише якщо явно вказано.
- Ресторан (наприклад, "McDonald's", "KFC", "Starbucks") — лише якщо явно вказано.

**Увага!** Не додавай параметри, які не були явно вказані в запиті. Якщо параметр не вказаний, поверни "n/a".

Запит: "{input_text}"

Поверни відповідь у форматі JSON:
{{
  "type": "тип страви (або 'n/a', якщо не вказано)",
  "name": "назва страви (або 'n/a', якщо не вказано)",
  "price": "умова ціни (у форматі, який підтримується бекендом, або 'n/a', якщо не вказано)",
  "calories": "умова калорій (або 'n/a', якщо не вказано)",
  "meal_time": "час прийому їжі (або 'n/a', якщо не вказано)",
  "category": "категорія страви (або 'n/a', якщо не вказано)",
  "restaurant": "назва ресторану (або 'n/a', якщо не вказано)"
}}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "format": "json",
                "stream": False
            },
            timeout=120  # Збільшуємо тайм-аут до 120 секунд
        )

        if response.status_code == 200:
            response_data = json.loads(response.text)
            conditions = json.loads(response_data["response"])
            logger.info(f"Умови від Ollama: {conditions}")
            return conditions
        else:
            logger.error(f"Помилка запиту до Ollama: {response.status_code}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Помилка запиту до Ollama: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        logger.error(f"Помилка підключення до Ollama: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Помилка підключення до Ollama: {e}"
        )

# Генерація SQL-запиту
def generate_sql(conditions: dict) -> tuple:
    """
    Генерує SQL-запит на основі умов, які є в таблиці Dish.
    """
    sql_conditions = []
    params = {}

    # Логуємо отримані умови
    logger.info(f"Умови для генерації SQL: {conditions}")

    # Тип страви (Main Course, Side, Drink, Dessert)
    if conditions.get("type") and conditions["type"].lower() != "n/a":
        sql_conditions.append("LOWER(Dish.type) = :type")
        params["type"] = conditions["type"].lower()

    # Назва страви (якщо вказано явно)
    if conditions.get("name") and conditions["name"].lower() != "n/a":
        sql_conditions.append("LOWER(Dish.name) LIKE :name")
        params["name"] = f"%{conditions['name'].lower()}%"

    # Ціна
    if conditions.get("price") and conditions["price"].lower() != "n/a":
        price_condition = conditions["price"]
        price_value = "".join(filter(str.isdigit, price_condition))
        if price_condition.startswith("<="):
            sql_conditions.append("Dish.price <= :max_price")
            params["max_price"] = float(price_value)
        elif price_condition.startswith(">="):
            sql_conditions.append("Dish.price >= :min_price")
            params["min_price"] = float(price_value)
        elif price_condition.startswith("<"):
            sql_conditions.append("Dish.price < :max_price")
            params["max_price"] = float(price_value)
        elif price_condition.startswith(">"):
            sql_conditions.append("Dish.price > :min_price")
            params["min_price"] = float(price_value)
        elif price_condition.startswith("=="):
            sql_conditions.append("Dish.price = :exact_price")
            params["exact_price"] = float(price_value)

    # Калорійність (якщо вказано явно)
    if conditions.get("calories") and conditions["calories"].lower() != "n/a":
        calories_condition = conditions["calories"]
        if calories_condition.startswith("<="):
            max_calories = calories_condition.split()[-1]
            sql_conditions.append("Dish.calories <= :max_calories")
            params["max_calories"] = float(max_calories)
        elif calories_condition.startswith(">="):
            min_calories = calories_condition.split()[-1]
            sql_conditions.append("Dish.calories >= :min_calories")
            params["min_calories"] = float(min_calories)
        elif calories_condition.startswith("<"):
            max_calories = calories_condition.split()[-1]
            sql_conditions.append("Dish.calories < :max_calories")
            params["max_calories"] = float(max_calories)
        elif calories_condition.startswith(">"):
            min_calories = calories_condition.split()[-1]
            sql_conditions.append("Dish.calories > :min_calories")
            params["min_calories"] = float(min_calories)
        elif calories_condition.startswith("=="):
            exact_calories = calories_condition.split()[-1]
            sql_conditions.append("Dish.calories = :exact_calories")
            params["exact_calories"] = float(exact_calories)

    # Категорія страви (якщо вказано явно)
    if conditions.get("category") and conditions["category"].lower() != "n/a":
        sql_conditions.append("LOWER(Dish.category) = :category")
        params["category"] = conditions["category"].lower()

    # Ресторан (якщо вказано явно)
    if conditions.get("restaurant") and conditions["restaurant"].lower() != "n/a":
        sql_conditions.append("LOWER(Restaurant.name) LIKE :restaurant_name")
        params["restaurant_name"] = f"%{conditions['restaurant'].lower()}%"

    # Генеруємо SQL-запит
    if sql_conditions:
        sql_query = f"""
        SELECT Dish.*, Restaurant.name AS restaurant_name
        FROM Dish
        JOIN Restaurant ON Dish.restaurant_id = Restaurant.id
        WHERE {' AND '.join(sql_conditions)};
        """
    else:
        sql_query = """
        SELECT Dish.*, Restaurant.name AS restaurant_name
        FROM Dish
        JOIN Restaurant ON Dish.restaurant_id = Restaurant.id;
        """

    return sql_query, params

# Рекомендації щодо часу прийому їжі
def recommend_meal_time(dish: dict) -> str:
    """
    Рекомендує час прийому їжі на основі характеристик страви.
    """
    if dish["type"].lower() == "drink":
        return "breakfast"
    elif dish["calories"] < 300:
        return "breakfast"
    elif 300 <= dish["calories"] <= 600:
        return "lunch"
    else:
        return "dinner"

# Фільтрація результатів з бази даних за допомогою Ollama
async def filter_results_with_llm(input_text: str, data: List[dict]) -> List[dict]:
    """
    Відправляє результати з бази даних та початковий запит до LLM для фільтрації.
    """
    # Формуємо промпт для LLM
    prompt = f"""
Початковий запит: {input_text}

Результати з бази даних:
{json.dumps(data, indent=2)}

Проаналізуй результати з бази даних і поверни лише ті, які відповідають початковому запиту.
Враховуй рекомендований час прийому їжі (recommended_meal_time), категорію страви (category), та інші параметри, якщо вони вказані в початковому інпуті.

Поверни відповідь у форматі JSON:
{{
  "filtered_results": [
    {{
      "name": "Назва страви",
      "calories": "Калорійність",
      "price": "Ціна",
      "type": "Тип страви",
      "category": "Категорія страви",
      "restaurant_name": "Назва ресторану",
      "recommended_meal_time": "Рекомендований час прийому їжі"
    }},
    ...
  ]
}}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "format": "json",
                "stream": False
            },
            timeout=120  # Збільшуємо тайм-аут до 120 секунд
        )

        if response.status_code == 200:
            response_data = json.loads(response.text)
            filtered_results = json.loads(response_data["response"])["filtered_results"]
            logger.info(f"Відфільтровані результати від LLM: {filtered_results}")
            return filtered_results  # Повертаємо Python об'єкт, а не JSONResponse
        else:
            logger.error(f"Помилка запиту до Ollama: {response.status_code}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Помилка запиту до Ollama: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        logger.error(f"Помилка підключення до Ollama: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Помилка підключення до Ollama: {e}"
        )

async def generate_sql_with_llm(input_text: str, db: AsyncSession):
    """
    Генерує SQL-запит на основі вхідного тексту та повертає JSON-відповідь.
    """
    try:
        conditions = analyze_input_with_ollama(input_text)
        sql_query, params = generate_sql(conditions)
        logger.info(f"Executing SQL: {sql_query} with params: {params}")

        result = await db.execute(text(sql_query), params)
        data = [dict(row) for row in result.mappings().all()]
        logger.info(f"Результати запиту: {data}")

        for dish in data:
            dish["recommended_meal_time"] = recommend_meal_time(dish)

        filtered_data = await filter_results_with_llm(input_text, data)

        # Повертаємо результат як Python об'єкт
        return filtered_data

    except Exception as e:
        logger.error(f"Помилка під час генерації SQL або фільтрації: {e}")
        raise HTTPException(status_code=500, detail=str(e))