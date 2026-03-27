from pydantic import BaseModel


class ReportCreate(BaseModel):
    city: str
    text: str
    temp: int