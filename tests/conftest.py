import asyncio
import os
import pytest_asyncio

from httpx import ASGITransport, AsyncClient 
from src.config import settings

settings.database_url = "sqlite:///teste_ticketfootball.db"

@pytest_asyncio.fixture 
async def db(request): 
    from src.database import database, engine, metadata
    from src.models.sector import sector
    from src.models.event_service import event_service
    from src.models.ticket_model import ticket_model
    from src.models.login import login
    
    await database.connect()
    metadata.create_all(engine)
    
    def teardown():
        async def _teardown():
            await database.disconnect()
            metadata.drop_all(engine)
            
        asyncio.run(_teardown())
        
    request.addfinalizer(teardown)
    
@pytest_asyncio.fixture 
async def client(db): 
    from src.main import app
    
    transport = ASGITransport(app=app)
    headers = { 
        "Accept": "application/json", 
        "Content-Type": "application/json"           
    }
    
    async with AsyncClient(base_url="http://test", transport=transport, headers=headers) as client:
        yield client 
        
@pytest_asyncio.fixture   
async def registered_user(client: AsyncClient):
    response = await client.post("/register", json={
        "cnpj": "12345678901234",
        "email": "rodrigo.kennes@hotmail.com",
        "password": "12345678",
        "corporate_name": "teste o1"
    })
    assert response.status_code == 200, f"Erro ao registrar: {response.text}"
    return response.json()


@pytest_asyncio.fixture   
async def access_token(client: AsyncClient, registered_user):
    response = await client.post("/login", json={"cnpj": "12345678901234",
                                                 "email": "rodrigo.kennes@hotmail.com",
                                                 "password": "12345678"})
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def client_authed(client: AsyncClient, access_token: str):
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client