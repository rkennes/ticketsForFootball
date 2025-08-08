from fastapi import status
from httpx import AsyncClient

async def test_get_sectors_success(client_authed: AsyncClient):
    #given
    sectors_data = [{"name": f"Sector {i}"} for i in range(1, 6)]
    for data in sectors_data:
        await client_authed.post("/sector", json=data)

    #when
    response = await client_authed.get("/sector?limit=10&skip=0")

    #then
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(content, list)
    assert len(content) == 5
