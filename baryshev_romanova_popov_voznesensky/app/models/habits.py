from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)

    checks = relationship("HabitCheck", back_populates="habit", cascade="all, delete-orphan")

class HabitCheck(Base):
    __tablename__ = "habit_checks"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)

    habit = relationship("Habit", back_populates="checks")

    __table_args__ = (UniqueConstraint("habit_id", "date", name="uix_habit_date"),)