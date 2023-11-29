from pydantic import BaseModel


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: dict
    rooms_quantity: int
    image_id: str

    # Добавляем параметр from_attributes

    class Config:
        from_attributes = True
