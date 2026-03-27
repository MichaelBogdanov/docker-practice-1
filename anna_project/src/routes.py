from __future__ import annotations

from fastapi import APIRouter
from models import ReportCreate
import crud

router = APIRouter()


@router.get("/reports")
def get_reports(city: str | None = None):
    if city is None:
        return crud.get_all_reports()
    return crud.get_reports_by_city(city)


@router.post("/reports")
def add_report(report: ReportCreate):
    return crud.create_report(report)


@router.get("/reports/recent")
def recent_reports(limit: int = 5):
    return crud.get_recent_reports(limit)
