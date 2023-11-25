from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelsDAO

router = APIRouter(prefix='/hotels')


@router.get('/{location}')
async def get_hotels(location: str,
                     date_from: date,
                     date_to: date):
    return await HotelsDAO.find_all(location, date_from, date_to)


