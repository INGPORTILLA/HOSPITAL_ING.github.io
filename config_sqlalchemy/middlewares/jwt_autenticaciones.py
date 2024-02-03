from fastapi.security import HTTPBearer 
from fastapi import Request, HTTPException
from routers.jwt_tokens import generate_jwt_token, validate_jwt_token

#creamos la clase para autenticaciones
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_jwt_token(auth.credentials)
        if data['email'] != "ne.marpo2408@gmail.com":
            raise HTTPException(status_code=403, detail="Acceso denegado")