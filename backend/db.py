from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

# Налаштування логування
import logging
logging.basicConfig(level=logging.INFO)

# Модель бази даних
Base = declarative_base()

class Restaurant(Base):
    __tablename__ = "Restaurant"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dishes = relationship("Dish", back_populates="restaurant")

class Dish(Base):
    __tablename__ = "Dish"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    calories = Column(Integer)
    price = Column(Float)
    type = Column(String)
    category = Column(String)  # Новий стовпець для категорії
    restaurant_id = Column(Integer, ForeignKey("Restaurant.id"))  # Зовнішній ключ
    restaurant = relationship("Restaurant", back_populates="dishes")  # Зв'язок

# Підключення до БД
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Створення engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Створення sessionmaker для асинхронних сесій
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Функція для створення таблиць у БД
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await insert_test_data()

# Функція для вставки тестових даних
async def insert_test_data():
    async with SessionLocal() as db:
        # Створення ресторанів
        restaurants = [
            Restaurant(name="McDonald's"),
            Restaurant(name="KFC"),
            Restaurant(name="Chick-fil-A"),
            Restaurant(name="Burger King"),
            Restaurant(name="Subway"),
            Restaurant(name="Taco Bell"),
            Restaurant(name="Pizza Hut"),
            Restaurant(name="Domino's"),
            Restaurant(name="Starbucks"),
            Restaurant(name="Dunkin' Donuts"),
        ]
        db.add_all(restaurants)
        await db.commit()

        # Оновлюємо об'єкти ресторанів, щоб отримати їхні id
        for restaurant in restaurants:
            await db.refresh(restaurant)
        # Створення страв
        test_dishes = [
            # McDonald's
            Dish(name="Big Mac", calories=550, price=5.99, type="Main Course", category="burgers", restaurant_id=restaurants[0].id),
            Dish(name="McChicken", calories=400, price=4.49, type="Main Course", category="burgers", restaurant_id=restaurants[0].id),
            Dish(name="Cheeseburger", calories=300, price=3.49, type="Main Course", category="burgers", restaurant_id=restaurants[0].id),
            Dish(name="Quarter Pounder", calories=520, price=6.49, type="Main Course", category="burgers", restaurant_id=restaurants[0].id),
            Dish(name="Filet-O-Fish", calories=390, price=4.79, type="Main Course", category="seafood", restaurant_id=restaurants[0].id),
            Dish(name="French Fries (Small)", calories=230, price=2.49, type="Side", category="potato", restaurant_id=restaurants[0].id),
            Dish(name="French Fries (Medium)", calories=340, price=3.19, type="Side", category="potato", restaurant_id=restaurants[0].id),
            Dish(name="French Fries (Large)", calories=510, price=3.79, type="Side", category="potato", restaurant_id=restaurants[0].id),
            Dish(name="McFlurry", calories=640, price=3.99, type="Dessert", category="dessert", restaurant_id=restaurants[0].id),
            Dish(name="Coca-Cola (Small)", calories=150, price=1.99, type="Drink", category="drink", restaurant_id=restaurants[0].id),
            Dish(name="Coca-Cola (Medium)", calories=210, price=2.19, type="Drink", category="drink", restaurant_id=restaurants[0].id),
            Dish(name="Coca-Cola (Large)", calories=290, price=2.49, type="Drink", category="drink", restaurant_id=restaurants[0].id),

            # KFC
            Dish(name="Original Recipe Chicken", calories=390, price=3.99, type="Main Course", category="chicken", restaurant_id=restaurants[1].id),
            Dish(name="Extra Crispy Chicken", calories=410, price=4.19, type="Main Course", category="chicken", restaurant_id=restaurants[1].id),
            Dish(name="Spicy Chicken Sandwich", calories=700, price=4.99, type="Main Course", category="burgers", restaurant_id=restaurants[1].id),
            Dish(name="Famous Bowl", calories=710, price=5.49, type="Main Course", category="chicken", restaurant_id=restaurants[1].id),
            Dish(name="Chicken Popcorn", calories=400, price=3.99, type="Main Course", category="chicken", restaurant_id=restaurants[1].id),
            Dish(name="Mashed Potatoes", calories=110, price=2.29, type="Side", category="potato", restaurant_id=restaurants[1].id),
            Dish(name="Mac & Cheese", calories=140, price=2.49, type="Side", category="pasta", restaurant_id=restaurants[1].id),
            Dish(name="Coleslaw", calories=170, price=2.39, type="Side", category="salad", restaurant_id=restaurants[1].id),
            Dish(name="Biscuit", calories=180, price=1.29, type="Side", category="bakery", restaurant_id=restaurants[1].id),
            Dish(name="Pepsi (Small)", calories=150, price=1.99, type="Drink", category="drink", restaurant_id=restaurants[1].id),
            Dish(name="Pepsi (Medium)", calories=210, price=2.19, type="Drink", category="drink", restaurant_id=restaurants[1].id),
            Dish(name="Pepsi (Large)", calories=290, price=2.49, type="Drink", category="drink", restaurant_id=restaurants[1].id),

            # Chick-fil-A
            Dish(name="Chicken Sandwich", calories=440, price=4.49, type="Main Course", category="chicken", restaurant_id=restaurants[2].id),
            Dish(name="Spicy Chicken Sandwich", calories=460, price=4.69, type="Main Course", category="chicken", restaurant_id=restaurants[2].id),
            Dish(name="Chicken Nuggets (8 pc)", calories=250, price=3.99, type="Main Course", category="chicken", restaurant_id=restaurants[2].id),
            Dish(name="Chicken Nuggets (12 pc)", calories=380, price=5.99, type="Main Course", category="chicken", restaurant_id=restaurants[2].id),
            Dish(name="Waffle Fries (Small)", calories=310, price=2.49, type="Side", category="potato", restaurant_id=restaurants[2].id),
            Dish(name="Waffle Fries (Medium)", calories=420, price=3.19, type="Side", category="potato", restaurant_id=restaurants[2].id),
            Dish(name="Waffle Fries (Large)", calories=540, price=3.79, type="Side", category="potato", restaurant_id=restaurants[2].id),
            Dish(name="Lemonade (Small)", calories=150, price=1.99, type="Drink", category="drink", restaurant_id=restaurants[2].id),
            Dish(name="Lemonade (Medium)", calories=220, price=2.49, type="Drink", category="drink", restaurant_id=restaurants[2].id),
            Dish(name="Lemonade (Large)", calories=300, price=2.99, type="Drink", category="drink", restaurant_id=restaurants[2].id),

            # Burger King
            Dish(name="Whopper", calories=660, price=6.99, type="Main Course", category="burgers", restaurant_id=restaurants[3].id),
            Dish(name="Chicken Fries", calories=280, price=3.49, type="Main Course", category="chicken", restaurant_id=restaurants[3].id),
            Dish(name="Bacon King", calories=800, price=7.49, type="Main Course", category="burgers", restaurant_id=restaurants[3].id),
            Dish(name="Onion Rings", calories=320, price=2.99, type="Side", category="snack", restaurant_id=restaurants[3].id),
            Dish(name="Mozzarella Sticks", calories=340, price=3.29, type="Side", category="snack", restaurant_id=restaurants[3].id),
            Dish(name="Vanilla Shake", calories=600, price=3.99, type="Dessert", category="dessert", restaurant_id=restaurants[3].id),
            Dish(name="Chocolate Shake", calories=620, price=3.99, type="Dessert", category="dessert", restaurant_id=restaurants[3].id),
            Dish(name="Sprite (Small)", calories=140, price=1.99, type="Drink", category="drink", restaurant_id=restaurants[3].id),
            Dish(name="Sprite (Medium)", calories=200, price=2.19, type="Drink", category="drink", restaurant_id=restaurants[3].id),
            Dish(name="Sprite (Large)", calories=280, price=2.49, type="Drink", category="drink", restaurant_id=restaurants[3].id),

            # Subway
            Dish(name="Italian B.M.T.", calories=480, price=6.99, type="Main Course", category="sandwiches", restaurant_id=restaurants[4].id),
            Dish(name="Turkey Breast", calories=280, price=5.99, type="Main Course", category="sandwiches", restaurant_id=restaurants[4].id),
            Dish(name="Veggie Delite", calories=230, price=5.49, type="Main Course", category="sandwiches", restaurant_id=restaurants[4].id),
            Dish(name="Chicken & Bacon Ranch", calories=570, price=7.49, type="Main Course", category="sandwiches", restaurant_id=restaurants[4].id),
            Dish(name="Cookies (Chocolate Chip)", calories=220, price=1.99, type="Dessert", category="dessert", restaurant_id=restaurants[4].id),
            Dish(name="Cookies (Oatmeal Raisin)", calories=210, price=1.99, type="Dessert", category="dessert", restaurant_id=restaurants[4].id),
            Dish(name="Apple Slices", calories=35, price=1.49, type="Side", category="fruit", restaurant_id=restaurants[4].id),
            Dish(name="Fountain Drink (Small)", calories=150, price=1.99, type="Drink", category="drink", restaurant_id=restaurants[4].id),
            Dish(name="Fountain Drink (Medium)", calories=210, price=2.19, type="Drink", category="drink", restaurant_id=restaurants[4].id),
            Dish(name="Fountain Drink (Large)", calories=290, price=2.49, type="Drink", category="drink", restaurant_id=restaurants[4].id),

            # Taco Bell
            Dish(name="Crunchy Taco", calories=170, price=1.99, type="Main Course", category="tacos", restaurant_id=restaurants[5].id),
            Dish(name="Soft Taco", calories=180, price=1.99, type="Main Course", category="tacos", restaurant_id=restaurants[5].id),
            Dish(name="Burrito Supreme", calories=440, price=4.49, type="Main Course", category="burritos", restaurant_id=restaurants[5].id),
            Dish(name="Nachos BellGrande", calories=740, price=5.99, type="Main Course", category="nachos", restaurant_id=restaurants[5].id),
            Dish(name="Cinnamon Twists", calories=170, price=1.49, type="Dessert", category="dessert", restaurant_id=restaurants[5].id),
            Dish(name="Cheesy Fiesta Potatoes", calories=240, price=2.49, type="Side", category="potato", restaurant_id=restaurants[5].id),
            Dish(name="Mountain Dew (Small)", calories=150, price=1.99, type="Drink", category="drink", restaurant_id=restaurants[5].id),
            Dish(name="Mountain Dew (Medium)", calories=210, price=2.19, type="Drink", category="drink", restaurant_id=restaurants[5].id),
            Dish(name="Mountain Dew (Large)", calories=290, price=2.49, type="Drink", category="drink", restaurant_id=restaurants[5].id),

            # Pizza Hut
            Dish(name="Pepperoni Pizza (Small)", calories=640, price=8.99, type="Main Course", category="pizza", restaurant_id=restaurants[6].id),
            Dish(name="Cheese Pizza (Medium)", calories=720, price=10.99, type="Main Course", category="pizza", restaurant_id=restaurants[6].id),
            Dish(name="Veggie Pizza (Large)", calories=800, price=12.99, type="Main Course", category="pizza", restaurant_id=restaurants[6].id),
            Dish(name="Garlic Breadsticks", calories=140, price=3.99, type="Side", category="bakery", restaurant_id=restaurants[6].id),
            Dish(name="Cinnamon Sticks", calories=220, price=4.49, type="Dessert", category="dessert", restaurant_id=restaurants[6].id),
            Dish(name="Pepsi (Small)", calories=150, price=1.99, type="Drink", category="drink", restaurant_id=restaurants[6].id),
            Dish(name="Pepsi (Medium)", calories=210, price=2.19, type="Drink", category="drink", restaurant_id=restaurants[6].id),
            Dish(name="Pepsi (Large)", calories=290, price=2.49, type="Drink", category="drink", restaurant_id=restaurants[6].id),

            # Domino's
            Dish(name="Margherita Pizza", calories=600, price=9.99, type="Main Course", category="pizza", restaurant_id=restaurants[7].id),
            Dish(name="BBQ Chicken Pizza", calories=720, price=11.99, type="Main Course", category="pizza", restaurant_id=restaurants[7].id),
            Dish(name="Buffalo Wings", calories=360, price=6.99, type="Side", category="chicken", restaurant_id=restaurants[7].id),
            Dish(name="Chocolate Lava Cake", calories=340, price=4.99, type="Dessert", category="dessert", restaurant_id=restaurants[7].id),
            Dish(name="Coke (Small)", calories=150, price=1.99, type="Drink", category="drink", restaurant_id=restaurants[7].id),
            Dish(name="Coke (Medium)", calories=210, price=2.19, type="Drink", category="drink", restaurant_id=restaurants[7].id),
            Dish(name="Coke (Large)", calories=290, price=2.49, type="Drink", category="drink", restaurant_id=restaurants[7].id),

            # Starbucks
            Dish(name="Caramel Macchiato", calories=250, price=4.99, type="Drink", category="coffee", restaurant_id=restaurants[8].id),
            Dish(name="Latte", calories=190, price=3.99, type="Drink", category="coffee", restaurant_id=restaurants[8].id),
            Dish(name="Cappuccino", calories=120, price=3.49, type="Drink", category="coffee", restaurant_id=restaurants[8].id),
            Dish(name="Blueberry Muffin", calories=350, price=2.99, type="Dessert", category="dessert", restaurant_id=restaurants[8].id),
            Dish(name="Chocolate Croissant", calories=280, price=3.49, type="Dessert", category="dessert", restaurant_id=restaurants[8].id),

            # Dunkin' Donuts
            Dish(name="Glazed Donut", calories=260, price=1.99, type="Dessert", category="dessert", restaurant_id=restaurants[9].id),
            Dish(name="Boston Kreme Donut", calories=270, price=2.29, type="Dessert", category="dessert", restaurant_id=restaurants[9].id),
            Dish(name="Iced Coffee", calories=90, price=2.99, type="Drink", category="coffee", restaurant_id=restaurants[9].id),
            Dish(name="Hot Coffee", calories=5, price=1.99, type="Drink", category="coffee", restaurant_id=restaurants[9].id),
        ]
        db.add_all(test_dishes)
        await db.commit()

# Функція для отримання сесії з БД
async def get_db():
    async with SessionLocal() as db:
        yield db