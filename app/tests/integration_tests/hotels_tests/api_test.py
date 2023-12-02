from datetime import date

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location, date_from, date_to, status_code",
    [
        ("Алтай", "2023-05-15", "2023-05-10", 400),
        ("Алтай", "2023-05-15", "2023-08-10", 400),
        ("Алтай", "2023-05-15", "2023-05-20", 200),
        ("Алтай", "2023-05-15", "2023-06-10", 200),
    ],
)
async def test_get_hotels_by_location_and_times(
    ac: AsyncClient, location: str, date_from: date, date_to: date, status_code
):
    response = await ac.get(
        "/hotels/{location}",
        params={"location": location, "date_from": date_from, "date_to": date_to},
    )
    if response.json():
        print(response.json()["detail"])
    assert response.status_code == status_code
