from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Dish(Base):
    __tablename__ = "Dish"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    calories = Column(Integer)
    price = Column(Float)
    type = Column(String)

# Підключення до БД
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Створення engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Створення sessionmaker для асинхронних сесій
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Додаємо цю змінну, щоб її можна було імпортувати
async_session = SessionLocal

# Функція для створення таблиць у БД
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await insert_test_data()

# Функція для вставки тестових даних
async def insert_test_data():
    async with SessionLocal() as db:
        test_dishes = [
    # McDonald's
    Dish(name="Big Mac", calories=550, price=5.99, type="Main Course"),
    Dish(name="McChicken", calories=400, price=4.49, type="Main Course"),
    Dish(name="Cheeseburger", calories=300, price=3.49, type="Main Course"),
    Dish(name="Quarter Pounder", calories=520, price=6.49, type="Main Course"),
    Dish(name="Filet-O-Fish", calories=390, price=4.79, type="Main Course"),
    Dish(name="French Fries (Small)", calories=230, price=2.49, type="Side"),
    Dish(name="French Fries (Medium)", calories=340, price=3.19, type="Side"),
    Dish(name="French Fries (Large)", calories=510, price=3.79, type="Side"),
    Dish(name="McFlurry", calories=640, price=3.99, type="Dessert"),
    Dish(name="Coca-Cola (Small)", calories=150, price=1.99, type="Drink"),
    Dish(name="Coca-Cola (Medium)", calories=210, price=2.19, type="Drink"),
    Dish(name="Coca-Cola (Large)", calories=290, price=2.49, type="Drink"),

    # KFC
    Dish(name="Original Recipe Chicken", calories=390, price=3.99, type="Main Course"),
    Dish(name="Extra Crispy Chicken", calories=410, price=4.19, type="Main Course"),
    Dish(name="Spicy Chicken Sandwich", calories=700, price=4.99, type="Main Course"),
    Dish(name="Famous Bowl", calories=710, price=5.49, type="Main Course"),
    Dish(name="Chicken Popcorn", calories=400, price=3.99, type="Main Course"),
    Dish(name="Mashed Potatoes", calories=110, price=2.29, type="Side"),
    Dish(name="Mac & Cheese", calories=140, price=2.49, type="Side"),
    Dish(name="Coleslaw", calories=170, price=2.39, type="Side"),
    Dish(name="Biscuit", calories=180, price=1.29, type="Side"),
    Dish(name="Pepsi (Small)", calories=150, price=1.99, type="Drink"),
    Dish(name="Pepsi (Medium)", calories=210, price=2.19, type="Drink"),
    Dish(name="Pepsi (Large)", calories=290, price=2.49, type="Drink"),

    # Chick-fil-A
    Dish(name="Chicken Sandwich", calories=440, price=4.49, type="Main Course"),
    Dish(name="Spicy Chicken Sandwich", calories=460, price=4.69, type="Main Course"),
    Dish(name="Chicken Nuggets (8 pc)", calories=250, price=3.99, type="Main Course"),
    Dish(name="Chicken Nuggets (12 pc)", calories=380, price=5.99, type="Main Course"),
    Dish(name="Waffle Fries (Small)", calories=310, price=2.49, type="Side"),
    Dish(name="Waffle Fries (Medium)", calories=420, price=3.19, type="Side"),
    Dish(name="Waffle Fries (Large)", calories=540, price=3.79, type="Side"),
    Dish(name="Lemonade (Small)", calories=150, price=1.99, type="Drink"),
    Dish(name="Lemonade (Medium)", calories=220, price=2.49, type="Drink"),
    Dish(name="Lemonade (Large)", calories=300, price=2.99, type="Drink"),

    # Burger King
    Dish(name="Whopper", calories=660, price=6.99, type="Main Course"),
    Dish(name="Chicken Fries", calories=280, price=3.49, type="Main Course"),
    Dish(name="Bacon King", calories=800, price=7.49, type="Main Course"),
    Dish(name="Onion Rings", calories=320, price=2.99, type="Side"),
    Dish(name="Mozzarella Sticks", calories=340, price=3.29, type="Side"),
    Dish(name="Vanilla Shake", calories=600, price=3.99, type="Dessert"),
    Dish(name="Chocolate Shake", calories=620, price=3.99, type="Dessert"),
    Dish(name="Sprite (Small)", calories=140, price=1.99, type="Drink"),
    Dish(name="Sprite (Medium)", calories=200, price=2.19, type="Drink"),
    Dish(name="Sprite (Large)", calories=280, price=2.49, type="Drink"),

    # Subway
    Dish(name="Italian B.M.T.", calories=480, price=6.99, type="Main Course"),
    Dish(name="Turkey Breast", calories=280, price=5.99, type="Main Course"),
    Dish(name="Veggie Delite", calories=230, price=5.49, type="Main Course"),
    Dish(name="Chicken & Bacon Ranch", calories=570, price=7.49, type="Main Course"),
    Dish(name="Cookies (Chocolate Chip)", calories=220, price=1.99, type="Dessert"),
    Dish(name="Cookies (Oatmeal Raisin)", calories=210, price=1.99, type="Dessert"),
    Dish(name="Apple Slices", calories=35, price=1.49, type="Side"),
    Dish(name="Fountain Drink (Small)", calories=150, price=1.99, type="Drink"),
    Dish(name="Fountain Drink (Medium)", calories=210, price=2.19, type="Drink"),
    Dish(name="Fountain Drink (Large)", calories=290, price=2.49, type="Drink"),

    # Taco Bell
    Dish(name="Crunchy Taco", calories=170, price=1.99, type="Main Course"),
    Dish(name="Soft Taco", calories=180, price=1.99, type="Main Course"),
    Dish(name="Burrito Supreme", calories=440, price=4.49, type="Main Course"),
    Dish(name="Nachos BellGrande", calories=740, price=5.99, type="Main Course"),
    Dish(name="Cinnamon Twists", calories=170, price=1.49, type="Dessert"),
    Dish(name="Cheesy Fiesta Potatoes", calories=240, price=2.49, type="Side"),
    Dish(name="Mountain Dew (Small)", calories=150, price=1.99, type="Drink"),
    Dish(name="Mountain Dew (Medium)", calories=210, price=2.19, type="Drink"),
    Dish(name="Mountain Dew (Large)", calories=290, price=2.49, type="Drink"),

    # Pizza Hut
    Dish(name="Pepperoni Pizza (Small)", calories=640, price=8.99, type="Main Course"),
    Dish(name="Cheese Pizza (Medium)", calories=720, price=10.99, type="Main Course"),
    Dish(name="Veggie Pizza (Large)", calories=800, price=12.99, type="Main Course"),
    Dish(name="Garlic Breadsticks", calories=140, price=3.99, type="Side"),
    Dish(name="Cinnamon Sticks", calories=220, price=4.49, type="Dessert"),
    Dish(name="Pepsi (Small)", calories=150, price=1.99, type="Drink"),
    Dish(name="Pepsi (Medium)", calories=210, price=2.19, type="Drink"),
    Dish(name="Pepsi (Large)", calories=290, price=2.49, type="Drink"),

    # Domino's
    Dish(name="Margherita Pizza", calories=600, price=9.99, type="Main Course"),
    Dish(name="BBQ Chicken Pizza", calories=720, price=11.99, type="Main Course"),
    Dish(name="Buffalo Wings", calories=360, price=6.99, type="Side"),
    Dish(name="Chocolate Lava Cake", calories=340, price=4.99, type="Dessert"),
    Dish(name="Coke (Small)", calories=150, price=1.99, type="Drink"),
    Dish(name="Coke (Medium)", calories=210, price=2.19, type="Drink"),
    Dish(name="Coke (Large)", calories=290, price=2.49, type="Drink"),

    # Starbucks
    Dish(name="Caramel Macchiato", calories=250, price=4.99, type="Drink"),
    Dish(name="Latte", calories=190, price=3.99, type="Drink"),
    Dish(name="Cappuccino", calories=120, price=3.49, type="Drink"),
    Dish(name="Blueberry Muffin", calories=350, price=2.99, type="Dessert"),
    Dish(name="Chocolate Croissant", calories=280, price=3.49, type="Dessert"),

    # Dunkin' Donuts
    Dish(name="Glazed Donut", calories=260, price=1.99, type="Dessert"),
    Dish(name="Boston Kreme Donut", calories=270, price=2.29, type="Dessert"),
    Dish(name="Iced Coffee", calories=90, price=2.99, type="Drink"),
    Dish(name="Hot Coffee", calories=5, price=1.99, type="Drink"),

    # Additional Dishes
    Dish(name="Grilled Cheese Sandwich", calories=300, price=4.99, type="Main Course"),
    Dish(name="Caesar Salad", calories=180, price=5.99, type="Main Course"),
    Dish(name="Chicken Caesar Wrap", calories=320, price=6.49, type="Main Course"),
    Dish(name="Vegetable Soup", calories=120, price=3.99, type="Side"),
    Dish(name="Chocolate Cake", calories=400, price=4.99, type="Dessert"),
    Dish(name="Vanilla Ice Cream", calories=200, price=2.99, type="Dessert"),
    Dish(name="Iced Tea", calories=70, price=1.99, type="Drink"),
    Dish(name="Orange Juice", calories=110, price=2.49, type="Drink"),
    Dish(name="Apple Juice", calories=120, price=2.49, type="Drink"),
    Dish(name="Mineral Water", calories=0, price=1.49, type="Drink"),
]
        db.add_all(test_dishes)
        await db.commit()

# Функція для отримання сесії з БД
async def get_db():
    async with SessionLocal() as db:
        yield db