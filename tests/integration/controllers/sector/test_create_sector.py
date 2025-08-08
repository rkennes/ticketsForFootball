from fastapi import status
from httpx import AsyncClient 

async def test_create_sector_success(client: AsyncClient, access_token: str):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"name" : "automated test one"}
    
    # When 
    response = await client.post("/sector", json=data, headers=headers)
    
    # Then 
    content = response.json()
    
    assert response.status_code == status.HTTP_201_CREATED
    