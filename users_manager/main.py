from fastapi import FastAPI

from employees.routers import organization as organization_router
from employees.routers import users as users_router

app = FastAPI()


def register_routers():

    app.include_router(users_router.router)
    app.include_router(organization_router.router)


register_routers()
