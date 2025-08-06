from fastapi import FastAPI
from src.controllers import sector, ticket_model, event_service, login
from contextlib import asynccontextmanager
from src.database import database


tags_metadata = [
    {
        "name": "Event and Tickets",
        "description": "API for event and ticket features"
    }
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="ticketsForFootball",
              openapi_tags=tags_metadata,
              summary="API for event and ticket features",
              lifespan=lifespan,
              description="""
## ticketsForFootball:
You will be able to:

* **Create Sector**.
* **Update Sector**.        
* **Delete Sector**.       
              """)


app.include_router(sector.router, tags=["sector"])
app.include_router(ticket_model.router, tags=["ticket model"])
app.include_router(event_service.router, tags=["event service"])
app.include_router(login.router, tags=["login"])
