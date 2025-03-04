from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel

from db import get_db
from llm import generate_sql

router = APIRouter()

# Опис моделі для запиту
class QueryRequest(BaseModel):
    nl_query: str

@router.post("/query/")
async def query_db(request: QueryRequest, db: AsyncSession = Depends(get_db)):
    sql_query = generate_sql(request.nl_query)  # Викликаємо LLM для генерації SQL
    result = await db.execute(text(sql_query))  # Виконуємо SQL-запит
    return {"data": result.fetchall()}  # Повертаємо результат
