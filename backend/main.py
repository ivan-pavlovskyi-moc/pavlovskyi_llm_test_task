from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from backend.db import get_db, create_db
from backend.llm import generate_sql_with_llm
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ініціалізація БД при старті
@app.on_event("startup")
async def startup():
    await create_db()

class QueryRequest(BaseModel):
    text: str  # Поле "text" для запиту

@app.post("/query/", response_model=dict)
async def query_db(request: QueryRequest, db: AsyncSession = Depends(get_db)) -> dict:
    try:
        # Генерація SQL через LLM
        sql_query, data = await generate_sql_with_llm(request.text, db)

        # Логування SQL-запиту
        logging.info(f"Executing SQL: {sql_query}")

        # Логування та повернення результату
        if not data:
            logging.info("No results found.")
            return {"message": "Нічого не знайдено.", "data": []}

        return {"data": data}

    except HTTPException as e:
        logging.error(f"HTTP error: {e.detail}")
        raise e

    except ValueError as e:
        logging.error(f"Value error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logging.error(f"Query execution error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    finally:
        await db.commit()  # Якщо зміни не потрібні, можна прибрати