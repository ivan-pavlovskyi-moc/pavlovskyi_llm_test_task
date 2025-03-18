from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel
from backend.db import get_db
from backend.llm import generate_sql
from backend.models import Dish

router = APIRouter()
class QueryRequest(BaseModel):
    text: str  # Поле "text" для запиту

@router.post("/query/", response_model=dict)
async def query_db(request: QueryRequest, db: AsyncSession = Depends(get_db)) -> dict:
    try:
        # Викликаємо LLM для генерації SQL-запиту
        sql_query = generate_sql(request.text)  # Генерація SQL запиту за допомогою LLM
        print(f"Generated SQL: {sql_query}")  # Логування SQL запиту для дебагу

        # Виконуємо SQL-запит
        result = await db.execute(text(sql_query))  
        data = [dict(row) for row in result.mappings().all()]
        
        # Повертаємо дані
        return {"data": data}
    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"SQL error: {str(e)}")  # Помилка виконання SQL
