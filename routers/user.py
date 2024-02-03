from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from routers.jwt_tokens import generate_jwt_token


user_router = APIRouter()

class User(BaseModel):
    email: str 
    password: str

#creamos la ruta para generar el token
@user_router.post('/login', tags=['pasword'])
def login_genere_token(user: User):
    if user.email == "ne.marpo2408@gmail.com" and user.password == "Y6DHNEC7PM":
        token:str = generate_jwt_token(user.model_dump())
        return JSONResponse(status_code =200, content={"message": "Inicio de sesion exitoso", "token": token})
