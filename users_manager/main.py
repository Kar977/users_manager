from fastapi import FastAPI

from users_manager.employees.routers import organization as organization_router
from users_manager.employees.routers import users as users_router

app = FastAPI()


def register_routers():

    app.include_router(users_router.router)
    app.include_router(organization_router.router)


register_routers()
