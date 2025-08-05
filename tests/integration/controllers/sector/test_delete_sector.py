from tests.utils.factories import create_sector_for_test
from fastapi import status
from httpx import AsyncClient

async def test_delete_sector_success(client: AsyncClient):
    # Given
    cnpj = "74492097000133"
    created = await create_sector_for_test(client, cnpj, "Setor a ser removido")
    sector_id = created["sector_id"]

    # When
    response = await client.delete(f"/sector/{cnpj}/{sector_id}")

    # Then
    content = response.json()
    assert response.status_code == 200
    assert content["message"] == "Sector removed."

    # Confirmando com um GET
    response_get = await client.get(f"/sector/{cnpj}?limit=10&skip=0")
    sectors = response_get.json()
    assert all(s["sector_id"] != sector_id for s in sectors)
