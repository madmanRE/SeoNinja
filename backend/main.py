from fastapi import FastAPI
from backend.routers import instruments_routers

app = FastAPI()


app.include_router(instruments_routers)
