from fastapi import FastAPI

from app.bookings.router import router as router_bookings
from app.users.router import router_users, router_auth
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as rooms_router
from app.pages.router import router as pages_router

app = FastAPI()


app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(rooms_router)
app.include_router(pages_router)




