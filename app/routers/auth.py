from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, JSONResponse


from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])



@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'wrong combination of login and password')

    is_correct_psw = utils.verify_passwords(user_credentials.password, user.password)

    if not is_correct_psw:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'wrong combination of login and password')

    access_token = oauth2.auth_handler.create_access_token(data={"user_id": user.id})  # информация для payload

    return {"msg": "success", "access_token": access_token, "token_type": "bearer"}
    #return RedirectResponse(url='/dashboard', status_code=status.HTTP_302_FOUND)
