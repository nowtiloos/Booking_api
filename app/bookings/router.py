from datetime import date

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users

from app.bookings.dao import BookingDAO
from app.tasks.tasks import send_booking_confirmation_email

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование']
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[dict]:
    return await BookingDAO.get_bookings_for_user(user_id=user.id)


@router.post('')
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked

    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    send_booking_confirmation_email.delay(booking, user.email)

    return booking


@router.delete('/{booking_id}')
async def delete_booking(booking_id: int,
                         user: Users = Depends(get_current_user)):
    return await BookingDAO.delete(user_id=user.id, id=booking_id)
