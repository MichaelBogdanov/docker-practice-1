from pydantic import BaseModel, ConfigDict
from typing import List

class QuoteBase(BaseModel):
    text: str
    author: str
    tags: List[str]

class QuoteCreate(QuoteBase):
    pass

class QuoteRead(QuoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)