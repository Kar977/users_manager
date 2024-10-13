from fastapi import FastAPI


from employees import routers as employee_router
app = FastAPI()

app.include_router(employee_router.router)
