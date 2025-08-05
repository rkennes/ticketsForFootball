from httpx import AsyncClient

async def create_sector_for_test(client: AsyncClient, cnpj: str, name: str) -> dict:
    response = await client.post("/sector", json={"cnpj": cnpj, "name": name})
    assert response.status_code == 201  
    return response.json()
