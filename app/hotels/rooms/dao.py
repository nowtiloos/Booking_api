from datetime import date

from sqlalchemy import select, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_list(cls, hotel_id, date_from: date, date_to: date):
        """WITH rooms_query AS (
SELECT rooms.id, rooms.hotel_id, hotels.name, rooms.description, hotels.services, rooms.price, rooms.quantity, rooms.image_id FROM rooms
JOIN hotels ON hotels.id = rooms.hotel_id
WHERE hotels.id = 4),

booked_rooms AS (SELECT room_id, COUNT(*) AS booked_rooms FROM bookings
WHERE date_from >= '2023-05-15' AND date_to <= '2026-06-20'
GROUP BY room_id)


SELECT id, hotel_id, name, description, services, price, quantity, image_id, (price * 25) AS total_cost, (quantity - COALESCE(booked_rooms, 0)) AS rooms_left FROM rooms_query
LEFT JOIN booked_rooms ON rooms_query.id = booked_rooms.room_id
ORDER BY id ASC"""

        total_days = (date_to - date_from).days
        async with async_session_maker() as session:
            rooms_query = (
                select(Rooms.id,
                       Rooms.hotel_id,
                       Hotels.name,
                       Rooms.description,
                       Hotels.services,
                       Rooms.price,
                       Rooms.quantity,
                       Rooms.image_id
                       )
                .select_from(Rooms)
                .join(Hotels, Hotels.id == Rooms.hotel_id)
                .where(Hotels.id == hotel_id)
                .cte('rooms_query')
            )

            booked_rooms = (
                select(Bookings.room_id,
                       func.count(Bookings.room_id).label('booked_rooms'))
                .select_from(Bookings)
                .where((Bookings.date_from >= date_from) &
                       (Bookings.date_to <= date_to))
                .group_by(Bookings.room_id)
                .cte('booked_rooms')
            )

            data = (
                select(rooms_query.c.id,
                       rooms_query.c.hotel_id,
                       rooms_query.c.name,
                       rooms_query.c.description,
                       rooms_query.c.services,
                       rooms_query.c.price,
                       rooms_query.c.quantity,
                       rooms_query.c.image_id,
                       (rooms_query.c.price * total_days).label('total_cost'),
                       (rooms_query.c.quantity - func.coalesce(booked_rooms.c.booked_rooms, 0)).label('rooms_left')
                       )
                .select_from(rooms_query)
                .join(booked_rooms, rooms_query.c.id == booked_rooms.c.room_id, isouter=True)
                .order_by(rooms_query.c.id)
            )
            print(total_days)
            result = await session.execute(data)
            return result.mappings().all()
