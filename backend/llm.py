import json
from fastapi import HTTPException
import logging
from sqlalchemy.sql import text
import requests
import subprocess

# Налаштування логування
logging.basicConfig(level=logging.INFO)

def start_ollama_model():
    """
    Запускає модель mistral за допомогою команди `ollama run mistral`.
    """
    try:
        # Запускаємо команду `ollama run mistral`
        process = subprocess.Popen(
            ["ollama", "run", "mistral"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logging.info("Модель mistral запущена.")
        return process
    except Exception as e:
        logging.error(f"Помилка під час запуску моделі mistral: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Помилка під час запуску моделі mistral: {e}"
        )

def analyze_input_with_ollama(input_text):
    """
    Аналізує вхідний текст за допомогою Ollama та повертає структуровані умови.
    """
    # Промт для Ollama
    prompt = f"""
    Проаналізуй наступний запит і витягни умови для пошуку страв:
    - Тип страви (Main Course, Side, Drink, Dessert).
    - Назва страви (наприклад, "Cheeseburger", "Caesar Salad").
    - Діапазон цін (наприклад, under $5, up to 10 dollars).
    - Діапазон калорій (наприклад, less than 300 calories).
    - Час прийому їжі (наприклад, breakfast, lunch, dinner).
    - Додаткові типи страв (наприклад, burger, wings, salad).

    Запит: "{input_text}"

    Поверни відповідь у форматі JSON:
    {{
      "type": "тип страви",
      "name": "назва страви",
      "price": "умова ціни",
      "calories": "умова калорій",
      "meal_time": "час прийому їжі",
      "additional_types": ["додаткові типи страв"]
    }}
    """

    try:
        # Надсилаємо запит до Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",  # URL Ollama API
            json={
                "model": "mistral",  # Модель, яку ви використовуєте
                "prompt": prompt,
                "format": "json",  # Запитуємо відповідь у форматі JSON
                "stream": False
            },
            timeout=30  # Збільшений таймаут
        )

        # Перевіряємо відповідь
        if response.status_code == 200:
            response_data = json.loads(response.text)
            # Витягуємо JSON з поля 'response'
            conditions = json.loads(response_data["response"])
            logging.info(f"Умови від Ollama: {conditions}")  # Логуємо умови
            return conditions
        else:
            logging.error(f"Помилка запиту до Ollama: {response.status_code}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Помилка запиту до Ollama: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        logging.error(f"Помилка підключення до Ollama: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Помилка підключення до Ollama: {e}"
        )

def generate_sql(conditions):
    """
    Генерує SQL-запит на основі умов від Ollama.
    """
    sql_conditions = []
    params = {}

    # Логуємо отримані умови
    logging.info(f"Умови для генерації SQL: {conditions}")

    # Тип страви (Main Course, Side, Drink, Dessert)
    if conditions.get("type"):
        sql_conditions.append("LOWER(type) = :type")
        params["type"] = conditions["type"].lower()

    # Назва страви
    if conditions.get("name"):
        name_keywords = conditions["name"].lower().split()
        name_conditions = [
            "LOWER(name) LIKE :name" + str(i)
            for i, keyword in enumerate(name_keywords)
        ]
        sql_conditions.append(f"({' OR '.join(name_conditions)})")
        for i, keyword in enumerate(name_keywords):
            params[f"name{i}"] = f"%{keyword}%"

    # Ціна
    if conditions.get("price"):
        price_condition = conditions["price"]
        # Видаляємо текст (наприклад, "dollars") і залишаємо лише число
        price_value = "".join(filter(str.isdigit, price_condition))
        if price_condition.startswith("<="):
            sql_conditions.append("price <= :max_price")
            params["max_price"] = float(price_value)
        elif price_condition.startswith(">="):
            sql_conditions.append("price >= :min_price")
            params["min_price"] = float(price_value)
        elif price_condition.startswith("<"):
            sql_conditions.append("price < :max_price")
            params["max_price"] = float(price_value)
        elif price_condition.startswith(">"):
            sql_conditions.append("price > :min_price")
            params["min_price"] = float(price_value)
        elif price_condition.startswith("=="):
            sql_conditions.append("price = :exact_price")
            params["exact_price"] = float(price_value)

    # Калорійність
    if conditions.get("calories") and conditions["calories"].lower() != "n/a":
        calories_condition = conditions["calories"]
        if calories_condition.startswith("<="):
            max_calories = calories_condition.split()[-1]
            sql_conditions.append("calories <= :max_calories")
            params["max_calories"] = float(max_calories)
        elif calories_condition.startswith(">="):
            min_calories = calories_condition.split()[-1]
            sql_conditions.append("calories >= :min_calories")
            params["min_calories"] = float(min_calories)
        elif calories_condition.startswith("<"):
            max_calories = calories_condition.split()[-1]
            sql_conditions.append("calories < :max_calories")
            params["max_calories"] = float(max_calories)
        elif calories_condition.startswith(">"):
            min_calories = calories_condition.split()[-1]
            sql_conditions.append("calories > :min_calories")
            params["min_calories"] = float(min_calories)
        elif calories_condition.startswith("=="):
            exact_calories = calories_condition.split()[-1]
            sql_conditions.append("calories = :exact_calories")
            params["exact_calories"] = float(exact_calories)

    # Час прийому їжі
    if conditions.get("meal_time") and conditions["meal_time"].lower() != "all meals":
        sql_conditions.append("LOWER(meal_time) = :meal_time")
        params["meal_time"] = conditions["meal_time"].lower()

    # Додаткові типи страв
    if conditions.get("additional_types"):
        additional_types = conditions["additional_types"]
        additional_conditions = [
            "LOWER(name) LIKE :additional_type" + str(i)
            for i, additional_type in enumerate(additional_types)
        ]
        sql_conditions.append(f"({' OR '.join(additional_conditions)})")
        for i, additional_type in enumerate(additional_types):
            params[f"additional_type{i}"] = f"%{additional_type.lower()}%"

    # Генеруємо SQL-запит
    if sql_conditions:
        sql_query = f"SELECT * FROM Dish WHERE {' AND '.join(sql_conditions)};"
    else:
        sql_query = "SELECT * FROM Dish;"

    return sql_query, params

def recommend_meal_time(dish):
    """
    Рекомендує час прийому їжі на основі характеристик страви.
    """
    if dish["type"].lower() == "drink":
        return "breakfast"  # Напої зазвичай підходять для сніданку
    elif dish["calories"] < 300:
        return "breakfast"  # Легкі страви — для сніданку
    elif 300 <= dish["calories"] <= 600:
        return "lunch"  # Страви з середньою калорійністю — для обіду
    else:
        return "dinner"  # Важкі страви — для вечері

async def generate_sql_with_llm(input_text, db):
    """
    Генерує SQL-запит на основі вхідного тексту та додає рекомендації.
    """
    # Запускаємо модель mistral перед аналізом вхідного тексту
    ollama_process = start_ollama_model()

    try:
        # Аналіз вхідного тексту за допомогою Ollama
        conditions = analyze_input_with_ollama(input_text)

        # Генерація SQL-запиту
        sql_query, params = generate_sql(conditions)
        logging.info(f"Executing SQL: {sql_query} with params: {params}")

        # Виконання SQL-запиту
        result = await db.execute(text(sql_query), params)  # Використовуємо параметри
        data = [dict(row) for row in result.mappings().all()]
        logging.info(f"Результати запиту: {data}")  # Логуємо результати

        # Додавання рекомендацій щодо часу прийому їжі
        for dish in data:
            dish["recommended_meal_time"] = recommend_meal_time(dish)

        # Фільтрація за часом прийому їжі (якщо вказано в інпуті)
        if conditions.get("meal_time"):
            requested_meal_time = conditions["meal_time"]
            logging.info(f"Фільтрація за часом прийому їжі: {requested_meal_time}")
            data = [dish for dish in data if dish["recommended_meal_time"] == requested_meal_time]

        return sql_query, data

    finally:
        # Зупиняємо процес Ollama після завершення роботи
        if ollama_process:
            ollama_process.terminate()
            logging.info("Модель mistral зупинена.")