from fastapi import HTTPException


def validate_city(city: str) -> str:
    city = city.strip()
    if not city:
        raise HTTPException(status_code=400, detail="City cannot be empty")
    return city


def validate_text(text: str) -> str:
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return text


def validate_temp(temp: int) -> int:
    if temp < -100 or temp > 100:
        raise HTTPException(
            status_code=400,
            detail="Temperature must be between -100 and 100"
        )
    return temp


def validate_limit(limit: int) -> int:
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be > 0")
    return limit


# ===== CRUD =====

def get_all_reports():
    return {"reports": []}


def get_reports_by_city(city: str):
    city = validate_city(city)
    return {
        "reports": [],
        "filter": city
    }


def create_report(report_data):
    city = validate_city(report_data.city)
    text = validate_text(report_data.text)
    temp = validate_temp(report_data.temp)

    return {
        "message": "Report created",
        "report": {
            "id": 1,
            "city": city,
            "text": text,
            "temp": temp
        }
    }


def get_recent_reports(limit: int = 5):
    limit = validate_limit(limit)
    return {
        "recent_reports": [],
        "limit": limit
    }