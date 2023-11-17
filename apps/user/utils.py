from datetime import date, timedelta
from typing import Optional


def calculate_birthdate_from_age(age: str) -> Optional[date]:
    if age is not None:
        today = date.today()
        birthdate = today - timedelta(days=365 * int(age))
        return birthdate
    return None
