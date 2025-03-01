from contextlib import asynccontextmanager

from fastapi import FastAPI

from database_structure.database import init_db
from employees.routers import organization as organization_router
from employees.routers import users as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)


def register_routers():

    app.include_router(users_router.router)
    app.include_router(organization_router.router)


register_routers()
