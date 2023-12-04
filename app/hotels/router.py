from datetime import date, datetime

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exceptions import CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo
from app.hotels.dao import HotelsDAO

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_times(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
):
    if date_from >= date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 30:
        raise CannotBookHotelForLongPeriod
    return await HotelsDAO.find_all(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel_on_id(hotel_id: int):
    return await HotelsDAO.find_one_or_none(id=hotel_id)
