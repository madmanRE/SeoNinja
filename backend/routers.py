from core.parsing_data import parse_data
from core.lemmatized_text import parse_text
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

instruments_routers = APIRouter(prefix="/instruments", tags=["Instruments"])

templates = Jinja2Templates(directory='backend/templates')

instruments_routers.mount("/static", StaticFiles(directory="backend/static"), name="static")


@instruments_routers.post("/parsing_top10_meta")
async def parsing_top10_meta(request: Request):
    form = await request.form()
    query = form.get("query")
    result = jsonable_encoder(parse_data(query))
    return templates.TemplateResponse("src/parsing_top10_meta.html", {"request": request, "data": result})



@instruments_routers.post("/lemmatize_text")
async def parse_text_data(request: Request):
    form = await request.form()
    url = form.get('urlinput')
    text = form.get('textinput')
    result = jsonable_encoder(parse_text(url, text))
    return templates.TemplateResponse("src/lemmatize_text.html", {"request": request, "data": result})
