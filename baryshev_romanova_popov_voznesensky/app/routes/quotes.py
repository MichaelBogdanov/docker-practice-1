from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

from app.database import get_session
from app.models.quotes import Quote
from app.schemas.quotes import QuoteCreate, QuoteRead

router = APIRouter()

@router.get("/", response_model=List[QuoteRead])
async def list_quotes(
    tag: Optional[str] = Query(None, description="Упс... Что-то не так!"),
    limit: Optional[int] = Query(None, description="Упс... Что-то не так!"),
    session: AsyncSession = Depends(get_session)
):
    query = select(Quote)
    if tag:
        query = query.where(Quote.tags.any(tag))
    if limit:
        query = query.limit(limit)
    result = await session.execute(query)
    quotes = result.scalars().all()
    return quotes

@router.get("/random", response_model=QuoteRead)
async def random_quote(
    tag: Optional[str] = Query(None, description="Упс... Что-то не так!"),
    session: AsyncSession = Depends(get_session)
):
    query = select(Quote)
    if tag:
        query = query.where(Quote.tags.any(tag))
    query = query.order_by(func.random()).limit(1)
    result = await session.execute(query)
    quote = result.scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Упс... Что-то не так!")
    return quote

@router.post("/", response_model=QuoteRead, status_code=201)
async def create_quote(
    quote: QuoteCreate,
    session: AsyncSession = Depends(get_session)
):
    new_quote = Quote(**quote.dict())
    session.add(new_quote)
    await session.commit()
    await session.refresh(new_quote)
    return new_quote

@router.delete("/{quote_id}", status_code=204)
async def delete_quote(
    quote_id: int,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Quote).where(Quote.id == quote_id))
    quote = result.scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Упс... Что-то не так!")
    await session.delete(quote)
    await session.commit()
    return None
