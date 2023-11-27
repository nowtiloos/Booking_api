from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelsDAO

router = APIRouter(prefix='/hotels',
                   tags=['Отели'])


@router.get('/{location}')
async def get_hotels_by_location_and_times(location: str,
                                           date_from: date,
                                           date_to: date):
    return await HotelsDAO.find_all(location, date_from, date_to)


@router.get('/id/{hotel_id}')
async def get_hotel_on_id(hotel_id: int):
    return await HotelsDAO.find_one_or_none(id=hotel_id)
