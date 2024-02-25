from core.parsing_data import parse_data
from core.lemmatized_text import parse_text, get_lems
from core.get_site_position import get_position_megaindex
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Request
import httpx
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import re
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from core.core import main


import requests

instruments_routers = APIRouter(prefix="/instruments", tags=["Instruments"])

templates = Jinja2Templates(directory="backend/templates")

instruments_routers.mount(
    "/static", StaticFiles(directory="backend/static"), name="static"
)


def clean_domain(domain):
    cleaned_domain = re.sub(r"https?://(www\.)?", "", domain)
    if cleaned_domain[-1] == "/":
        cleaned_domain = cleaned_domain[:-1]
    return cleaned_domain


@instruments_routers.post("/gsc_api_result")
async def get_index_page(request: Request):
    form = await request.form()
    domain = form.get("domain")
    position = form.get("position")
    days = form.get("days")
    url_filter = form.get("url-filter")
    minus_words = form.get("minus_words")
    minus_words = list(map(lambda word: word.strip(), minus_words.split("\n")))
    main.get_extraction_result(
        site_domain=domain,
        days=int(days),
        gt_position=int(position),
        url_filter=url_filter,
        minus_words=minus_words,
    )
    return FileResponse(
        path="core/core/results/result.xlsx",
        filename="result.xlsx",
        media_type="multipart/form-data",
    )


@instruments_routers.get("/gsc_api")
async def get_gsc_api_page(request: Request):
    return templates.TemplateResponse("src/gsc_api.html", {"request": request})


@instruments_routers.post("/parsing_top10_meta")
async def parsing_top10_meta(request: Request):
    form = await request.form()
    query = form.get("query")
    result = jsonable_encoder(parse_data(query))
    return templates.TemplateResponse(
        "src/parsing_top10_meta.html", {"request": request, "data": result}
    )


@instruments_routers.post("/lemmatize_text")
async def parse_text_data(request: Request):
    form = await request.form()
    url = form.get("urlinput")
    text = form.get("textinput")
    result = jsonable_encoder(parse_text(url, text))
    return templates.TemplateResponse(
        "src/lemmatize_text.html", {"request": request, "data": result}
    )


@instruments_routers.post("/lemmatize_queries")
async def lemmatize_queries(request: Request):
    form = await request.form()
    queries = form.get("queriesinput")
    result = jsonable_encoder(get_lems(queries))
    return templates.TemplateResponse(
        "src/lemmatize_queries.html", {"request": request, "data": result}
    )


@instruments_routers.get("/combine_queries")
async def combine_queries(request: Request):
    return templates.TemplateResponse("src/combine_queries.html", {"request": request})


@instruments_routers.post("/get_positions")
async def get_positions_both(request: Request):
    form = await request.form()
    domain = clean_domain(form.get("domaininput"))
    region = form.get("region")
    queries = list(
        map(lambda query: query.strip(), form.get("queriesinput").split("\n"))
    )
    result = jsonable_encoder(get_position_megaindex(domain, queries, region))
    return templates.TemplateResponse(
        "src/get_positions.html", {"request": request, "data": result}
    )


class UrlData(BaseModel):
    url: str


@instruments_routers.post("/get_status_code")
async def get_response_code(data: UrlData):
    url = data.url
    try:
        response = requests.get(url, allow_redirects=False)
        resp_code = response.status_code
        return JSONResponse(content={"response_code": resp_code})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
