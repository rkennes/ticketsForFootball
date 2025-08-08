from httpx import AsyncClient

async def create_sector_for_test(client: AsyncClient, access_token: str, name: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post("/sector", json={"name": name}, headers=headers)
    assert response.status_code == 201, f"Erro ao criar setor: {response.text}"
    return response.json()