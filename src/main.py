from fastapi import FastAPI,Request
from src.controllers import sector, ticket_model, event_service, login, login_permission, permission_type
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


@app.middleware("http")
async def log_method(request: Request, call_next):
    print(f"Request method: {request.method}, URL: {request.url}")
    response = await call_next(request)
    return response

app.include_router(sector.router, tags=["sector"])
app.include_router(ticket_model.router, tags=["ticket model"])
app.include_router(event_service.router, tags=["event service"])
app.include_router(login.router, tags=["login"])
app.include_router(login_permission.router, tags=["login_permission"])
app.include_router(permission_type.router, tags=["permission_type"])