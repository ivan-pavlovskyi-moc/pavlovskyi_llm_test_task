# init_db.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import async_session, engine, Base
from backend.models import Dish  # ✅ Працюватиме, бо models — це файл


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        await populate_dishes(session)

async def populate_dishes(session: AsyncSession):
    dishes = [
        # McDonald's
        {"name": "Quarter Pounder with Cheese", "calories": 530, "price": 4.79, "type": "Перші страви"},
        {"name": "Filet-O-Fish", "calories": 380, "price": 4.29, "type": "Перші страви"},
        {"name": "Egg McMuffin", "calories": 300, "price": 3.29, "type": "Перші страви"},
        {"name": "McCafe Coffee", "calories": 2, "price": 1.49, "type": "Напій"},
        {"name": "Apple Pie", "calories": 250, "price": 1.29, "type": "Десерт"},
        {"name": "Hash Browns", "calories": 140, "price": 1.19, "type": "Гарнір"},
        {"name": "Hotcakes", "calories": 350, "price": 3.99, "type": "Десерт"},
        {"name": "Chicken McNuggets", "calories": 270, "price": 4.99, "type": "Гарнір"},
        {"name": "Coca-Cola", "calories": 140, "price": 1.69, "type": "Напій"},
        {"name": "Iced Coffee", "calories": 100, "price": 2.49, "type": "Напій"},
        
        # KFC
        {"name": "Extra Crispy Chicken", "calories": 400, "price": 7.49, "type": "Перші страви"},
        {"name": "Chicken Tenders", "calories": 210, "price": 4.49, "type": "Гарнір"},
        {"name": "Popcorn Chicken", "calories": 120, "price": 3.99, "type": "Гарнір"},
        {"name": "Biscuits", "calories": 200, "price": 1.49, "type": "Гарнір"},
        {"name": "Gravy", "calories": 50, "price": 0.99, "type": "Гарнір"},
        {"name": "Pepsi", "calories": 150, "price": 1.89, "type": "Напій"},
        {"name": "Mountain Dew", "calories": 170, "price": 1.89, "type": "Напій"},
        {"name": "Mashed Potatoes with Gravy", "calories": 200, "price": 2.49, "type": "Гарнір"},
        {"name": "Potato Wedges", "calories": 240, "price": 2.49, "type": "Гарнір"},
        {"name": "Chili", "calories": 290, "price": 3.99, "type": "Перші страви"},
        
        # Chick-fil-A
        {"name": "Chick-fil-A Deluxe Sandwich", "calories": 500, "price": 5.19, "type": "Перші страви"},
        {"name": "Grilled Chicken Sandwich", "calories": 380, "price": 5.39, "type": "Перші страви"},
        {"name": "Chicken Wrap", "calories": 310, "price": 4.99, "type": "Перші страви"},
        {"name": "Spicy Chicken Nuggets", "calories": 270, "price": 4.69, "type": "Гарнір"},
        {"name": "Chilled Grilled Chicken", "calories": 250, "price": 5.49, "type": "Перші страви"},
        {"name": "Waffle Fries with Cheese", "calories": 400, "price": 2.99, "type": "Гарнір"},
        {"name": "Chicken Salad Sandwich", "calories": 420, "price": 4.29, "type": "Перші страви"},
        {"name": "Frosted Lemonade", "calories": 340, "price": 3.79, "type": "Десерт"},
        {"name": "Peach Milkshake", "calories": 650, "price": 4.39, "type": "Десерт"},
        {"name": "Iced Tea", "calories": 0, "price": 1.79, "type": "Напій"},
        
        # Додаткові страви для збільшення
        {"name": "Cheddar Jack Chicken", "calories": 360, "price": 6.79, "type": "Перші страви"},
        {"name": "Chicken Parmesan", "calories": 500, "price": 5.99, "type": "Перші страви"},
        {"name": "Buffalo Wings", "calories": 220, "price": 4.49, "type": "Гарнір"},
        {"name": "Garden Salad", "calories": 150, "price": 3.29, "type": "Гарнір"},
        {"name": "Caesar Salad", "calories": 300, "price": 4.19, "type": "Гарнір"},
        {"name": "Fish Sandwich", "calories": 350, "price": 3.99, "type": "Перші страви"},
        {"name": "Mozzarella Sticks", "calories": 290, "price": 4.59, "type": "Гарнір"},
        {"name": "French Toast Sticks", "calories": 320, "price": 2.99, "type": "Десерт"},
        {"name": "Fruit Cup", "calories": 60, "price": 1.99, "type": "Гарнір"},
        {"name": "Onion Rings", "calories": 250, "price": 2.49, "type": "Гарнір"},
        {"name": "Apple Slices", "calories": 40, "price": 1.19, "type": "Гарнір"},
        {"name": "Coffee", "calories": 5, "price": 1.59, "type": "Напій"},
        {"name": "Hot Chocolate", "calories": 220, "price": 2.29, "type": "Напій"},
    ]

    db_dishes = [Dish(**dish) for dish in dishes]
    session.add_all(db_dishes)
    await session.commit()
    print("✅ Страви успішно додані в базу!")

if __name__ == "__main__":
    asyncio.run(init_db())
