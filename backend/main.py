from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.routers import instruments_routers
import re


app = FastAPI()


templates = Jinja2Templates(directory="backend/templates")

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

app.include_router(instruments_routers)


def read_regions(regions_path="core/regions.txt"):
    with open(regions_path, "r", encoding="utf-8") as f:
        data = f.readlines()
        data = list(
            map(lambda region: re.split(r"\s", region.strip(), maxsplit=1), data)
        )
        return data


@app.get("/")
async def get_index_page(request: Request):
    return templates.TemplateResponse(
        "src/index.html", {"request": request, "data": read_regions()}
    )
