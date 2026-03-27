from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import timedelta

from app.database import get_session
from app.models.habits import Habit, HabitCheck
from app.schemas.habits import HabitCreate, HabitRead, CheckCreate, CheckRead, StreakResponse

router = APIRouter()

@router.get("/", response_model=List[HabitRead])
async def list_habits(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Habit))
    habits = result.scalars().all()
    return habits

@router.post("/", response_model=HabitRead, status_code=201)
async def create_habit(habit: HabitCreate, session: AsyncSession = Depends(get_session)):
    new_habit = Habit(**habit.model_dump())
    session.add(new_habit)
    await session.commit()
    await session.refresh(new_habit)
    return new_habit

@router.post("/{habit_id}/check", response_model=CheckRead, status_code=201)
async def check_habit(habit_id: int, check: CheckCreate, session: AsyncSession = Depends(get_session)):
    habit_result = await session.execute(select(Habit).where(Habit.id == habit_id))
    habit = habit_result.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Упс... Что-то не так!")

    new_check = HabitCheck(habit_id=habit_id, date=check.date)
    session.add(new_check)
    try:
        await session.commit()
        await session.refresh(new_check)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Упс... Что-то не так!")
    return new_check

@router.get("/{habit_id}/streak", response_model=StreakResponse)
async def get_streak(habit_id: int, session: AsyncSession = Depends(get_session)):
    habit_result = await session.execute(select(Habit).where(Habit.id == habit_id))
    habit = habit_result.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Упс... Что-то не так!")

    result = await session.execute(
        select(HabitCheck.date)
        .where(HabitCheck.habit_id == habit_id)
        .order_by(HabitCheck.date)
    )
    dates = [row[0] for row in result.all()]

    if not dates:
        return StreakResponse(streak=0)

    streak = 1
    for i in range(len(dates)-2, -1, -1):
        if dates[i+1] - dates[i] == timedelta(days=1):
            streak += 1
        else:
            break
    return StreakResponse(streak=streak)