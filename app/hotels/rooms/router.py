from datetime import date

from fastapi import APIRouter

from app.hotels.rooms.dao import RoomsDAO

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: int, date_from: date, date_to: date) -> list[str]:
    return await RoomsDAO.get_rooms_list(hotel_id, date_from, date_to)
