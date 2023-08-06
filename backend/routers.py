from core.parsing_data import parse_data
from core.lemmatized_text import parse_text
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status

instruments_routers = APIRouter(
    prefix='/instruments',
    tags=['Instruments']
)


@instruments_routers.get("/parsing_top10")
async def parsing_top10_meta(query: str):
    result = parse_data(query)
    return jsonable_encoder(result)


@instruments_routers.post("/lemmatize_text")
async def parse_text_data(url: str = None, text: str = None):
    result = parse_text(url, text)
    return jsonable_encoder(result)
