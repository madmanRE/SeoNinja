from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.routers import instruments_routers


app = FastAPI()


templates = Jinja2Templates(directory='backend/templates')

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

app.include_router(instruments_routers)

@app.get("/")
async def get_index_page(request: Request):
    return templates.TemplateResponse("src/index.html", {"request": request})