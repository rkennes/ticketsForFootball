from fastapi import status
from httpx import AsyncClient 

async def test_create_sector_success(client: AsyncClient):
    # Given
    #headers = {"Authorization": f"Bearer {access_token}"}
    data = {"cnpj" : "74492097000133", "name" : "automated test one"}
    
    # When 
    response = await client.post("/sector", json=data)
    
    # Then 
    content = response.json()
    
    assert response.status_code == status.HTTP_201_CREATED
    