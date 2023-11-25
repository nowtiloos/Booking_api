from datetime import date

from sqlalchemy import select, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls,
                       location: str,
                       date_from: date,
                       date_to: date):
        """WITH booked_rooms AS (
SELECT hotel_id, room_id, COUNT(*) AS booked_rooms FROM hotels
JOIN rooms ON hotels.id = rooms.hotel_id
JOIN bookings ON rooms.id = bookings.room_id
WHERE (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
      (date_from <= '2023-05-15' AND date_to > '2023-05-15')
GROUP BY hotel_id, room_id
)

SELECT
id, name, location, services, rooms_quantity, image_id, (rooms_quantity - COALESCE(booked_rooms, 0)) AS rooms_left
FROM hotels
LEFT JOIN booked_rooms ON hotels.id = booked_rooms.hotel_id
WHERE hotels.location LIKE '%Алтай%'
ORDER BY id"""
        async with async_session_maker() as session:
            booked_rooms = (
                select(Rooms.hotel_id, Bookings.room_id, func.count(Rooms.hotel_id).label('booked_rooms'))
                .select_from(Hotels)
                .join(Rooms, Hotels.id == Rooms.hotel_id)
                .join(Bookings, Rooms.id == Bookings.room_id)
                .where(
                    (
                            (Bookings.date_from >= date_from) &
                            (Bookings.date_from <= date_to)
                    ) | (
                            (Bookings.date_from <= date_from) &
                            (Bookings.date_to > date_from)
                    )
                )
                .group_by(Rooms.hotel_id, Bookings.room_id)
                .cte('booked_rooms')
            )
            result = (
                select(Hotels.id,
                       Hotels.name,
                       Hotels.location,
                       Hotels.services,
                       Hotels.rooms_quantity,
                       Hotels.image_id,
                       (Hotels.rooms_quantity - func.coalesce(booked_rooms.c.booked_rooms, 0)).label('rooms_left')
                       )
                .join(booked_rooms, Hotels.id == booked_rooms.c.hotel_id, isouter=True)
                .where(Hotels.location.ilike(f'%{location}%'))
            )
            result = await session.execute(result)
            return result.mappings().all()
