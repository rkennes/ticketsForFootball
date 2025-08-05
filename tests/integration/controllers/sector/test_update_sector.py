from fastapi import status
from httpx import AsyncClient
from tests.utils.factories import create_sector_for_test

async def test_update_sector_success(client: AsyncClient):
    # Given
    cnpj = "74492097000133"
    created = await create_sector_for_test(client, cnpj, "Setor a ser removido")
    sector_id = created["sector_id"]

    update_data = {"cnpj": cnpj, "name": "Setor Atualizado"}

    # When
    response = await client.put(f"/sector/{sector_id}", json=update_data)

    # Then
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content["message"] == "Sector updated."

    # Confirmando com um GET
    response_get = await client.get(f"/sector/{cnpj}?limit=10&skip=0")
    sectors = response_get.json()
    updated_sector = next((s for s in sectors if s["sector_id"] == sector_id), None)
    assert updated_sector["name"] == "Setor Atualizado"
