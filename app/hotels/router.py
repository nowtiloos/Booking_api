from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelsDAO

router = APIRouter(prefix='/hotels')


@router.get('/{location}')
async def get_hotels(location: str,
                     date_from: date,
                     date_to: date) -> list[dict]:
    return await HotelsDAO.find_all(location, date_from, date_to)


@router.get('/{hotel_id}/rooms')
async def get_hotel_rooms(hotel_id: int,
                          date_from: date,
                          date_to: date) -> list[dict]:
    return await HotelsDAO.get_rooms_list(hotel_id, date_from, date_to)
