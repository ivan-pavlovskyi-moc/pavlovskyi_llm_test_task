from fastapi import FastAPI
from routes import router

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Дозволено фронтенд доступ
    allow_credentials=True,
    allow_methods=["*"],  # Дозволено всі методи (GET, POST, OPTIONS, і т.д.)
    allow_headers=["*"],  # Дозволено всі заголовки
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
