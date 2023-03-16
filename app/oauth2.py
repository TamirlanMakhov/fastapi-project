from typing import Optional

from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from jose import JOSEError, jwt, JWTError

from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


class AuthHandler:
    def __init__(self):
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def verify_access_token(self, token: str, credentials_exception):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get('user_id')

            if not user_id:
                raise credentials_exception
            token_data = schemas.TokenData(id=user_id)

        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'could not validate '
                                                                                 f'credentials',
                                headers={"WWW-Authenticate": "Bearer"})
        else:
            return token_data

    def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'could not validate '
                                                                                               f'credentials',
                                              headers={"WWW-Authenticate": "Bearer"})

        token = self.verify_access_token(token, credentials_exception)
        user = db.query(models.User).filter(models.User.id == token.id).first()
        return user


auth_handler = AuthHandler()
