from sqlalchemy.future import select
from app.database import async_session_maker
from app.models.quotes import Quote
from app.models.habits import Habit, HabitCheck
from datetime import date

async def init_data():
    async with async_session_maker() as session:
        result = await session.execute(select(Quote).limit(1))
        quotes_exist = result.scalar_one_or_none()
        if not quotes_exist:
            quotes = [
                Quote(
                    text="Один в поле не двое",
                    author="Виталий Владимирович Кличко ",
                    tags=["life", "motivation"]
                ),
                Quote(
                    text="Упал - вставай, Встал - упай, Упай - чокопай",
                    author="Джейсон Стэйтем",
                    tags=["life", "motivation"]
                ),
                Quote(
                    text="Ладно",
                    author="Жак Фреско",
                    tags=["philosophy", "motivation"]
                ),
                Quote(
                    text="У меня все работает, так что баг на вашей стороне",
                    author="Сунь-цзы | 'Искусство войны'",
                    tags=["philosophy", "war"]
                )
            ]
            session.add_all(quotes)
            await session.commit()

        result = await session.execute(select(Habit).limit(1))
        habits_exist = result.scalar_one_or_none()
        if not habits_exist:
            habits = [
                Habit(name="Посолите", user_id=1),
                Habit(name="Поперчите", user_id=1),
                Habit(name="Пассатижи", user_id=1),
            ]
            session.add_all(habits)
            await session.flush()

            fixed_dates = [date(2026, 2, 25), date(2026, 2, 26), date(2026, 2, 27)]
            for habit in habits:
                for d in fixed_dates:
                    check = HabitCheck(habit_id=habit.id, date=d)
                    session.add(check)
            await session.commit()