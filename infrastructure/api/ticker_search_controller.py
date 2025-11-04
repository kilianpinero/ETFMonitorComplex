from fastapi import APIRouter, Depends, HTTPException, Body, Request, Cookie, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
from application.ticker_search import TickerSearch

router = APIRouter(prefix="/api/ticker", tags=["ticker"])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../../web'))
ticker_search_service = TickerSearch()

@router.get("/search")
def search_ticker(query: str = ""):
    result = ticker_search_service.get_ticker(query)
    return JSONResponse(content=result)

@router.post("/search")
def search_ticker_post(query: str = Form(...)):
    result = ticker_search_service.get_ticker(query)
    return JSONResponse(content=result)
