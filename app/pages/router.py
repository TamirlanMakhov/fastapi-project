from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter(
    tags=['Pages']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('/')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {"request": request})


@router.get('/signup', response_class=HTMLResponse)
def registration(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})
