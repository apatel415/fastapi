from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# secert key
# algorithm
# expiration time for token

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expiration_minutes

def create_access_token(data: dict):
    to_encoode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encoode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encoode, SECRET_KEY, algorithm = ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        
        # decodes a jwt token generated for certain data
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # access token created in auth inputs only the 'user_id' as the data, so the jwt
        # token created encodes the user id field
        # when decoding, we want to get the fields that were encoded; just the user id field 
        id: str = payload.get("user_id")
        
        if not id:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                          detail = f'Could not validate credentials',
                                          headers = {'WWW-Authenticate': 'Bearer'})
    
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
    