from fastapi import status
from httpx import AsyncClient
from tests.utils.factories import create_sector_for_test

async def test_update_sector_success(client: AsyncClient,access_token: str):
    
    # Given
    created = await create_sector_for_test(client, access_token, "Setor a ser atualizado")
    sector_id = created["sector_id"]

    update_data = {"name": "Setor Atualizado"}

    # When
    response = await client.put(f"/sector/{sector_id}", json=update_data, headers={"Authorization": f"Bearer {access_token}"})

    # Then
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content["message"] == "Sector updated."
