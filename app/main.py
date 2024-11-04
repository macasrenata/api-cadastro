from fastapi import FastAPI
from app.routers.crud_routers import router

app = FastAPI()

app.include_router(router)