from fastapi import FastAPI
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.responses import Response
from fastapi import FastAPI, Request
from pydantic import BaseModel
from routers.jwt_tokens import generate_jwt_token
from config_sqlalchemy.database import Base, engine
from config_sqlalchemy.middlewares.error_handler import ErrorHandler
from routers.pacientes import paciente_router
from routers.user import user_router

#creamos la variable
app = FastAPI()
app.title = "MEDICAL_ANALISIS_ING"
app.version = "0.0.1"

#creamos el middleware e incluimos los routers
app.add_middleware(ErrorHandler)
app.include_router(paciente_router)
app.include_router(user_router)

#creamos la tabla para la base de datos
Base.metadata.create_all(engine)

# definimos ruta name de la app
@app.get('/', tags=['INICIO'])
def name_app():
    return HTMLResponse('<h1>MEDICAL_ANALISIS_ING</h1>')


   
    

















