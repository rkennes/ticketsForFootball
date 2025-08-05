from fastapi import status
from httpx import AsyncClient

async def test_get_sectors_success(client: AsyncClient):
    # Given
    cnpj = "74492097000133"
    sectors_data = [
        {"cnpj": cnpj, "name": f"Sector {i}"} for i in range(1, 6)
    ]

    for data in sectors_data:
        await client.post("/sector", json=data)

    # When
    response = await client.get(f"/sector/{cnpj}?limit=10&skip=0")

    # Then
    content = response.json()
    
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(content, list)
    assert len(content) == 5
    assert all(sector["cnpj"] == cnpj for sector in content)
