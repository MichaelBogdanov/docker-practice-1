from pydantic import BaseModel, ConfigDict
from datetime import date

class HabitBase(BaseModel):
    name: str
    user_id: int

class HabitCreate(HabitBase):
    pass

class HabitRead(HabitBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CheckBase(BaseModel):
    date: date

class CheckCreate(CheckBase):
    pass

class CheckRead(CheckBase):
    id: int
    habit_id: int
    model_config = ConfigDict(from_attributes=True)

class StreakResponse(BaseModel):
    streak: int