from typing import Optional

from fastapi import APIRouter, Request, Depends, Cookie, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .. import oauth2, database, models

router = APIRouter(
    tags=['Pages']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('/')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/signup', response_class=HTMLResponse)
def registration(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


@router.get('/login', response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.get('/dashboard', response_class=HTMLResponse)
def dashboard(request: Request):

    return templates.TemplateResponse('dashboard.html', {'request': request})




