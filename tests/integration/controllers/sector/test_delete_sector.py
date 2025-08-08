from tests.utils.factories import create_sector_for_test
from fastapi import status
from httpx import AsyncClient

async def test_delete_sector_success(client: AsyncClient, access_token: str):
    # Given
    created = await create_sector_for_test(client, access_token, "Setor a ser removido")
    sector_id = created["sector_id"]

    # When
    response = await client.delete(f"/sector/{sector_id}", headers={"Authorization": f"Bearer {access_token}"})

    # Then
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content["message"] == "Sector removed."
