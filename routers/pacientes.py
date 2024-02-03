from fastapi import APIRouter
from fastapi import Path,Query,Depends
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from typing import Optional, List
from config_sqlalchemy.models.base_datos_pacientes import Paciente as PacienteModel
from fastapi.encoders import jsonable_encoder
from config_sqlalchemy.middlewares.jwt_autenticaciones import JWTBearer
from sqlalchemy import func
from config_sqlalchemy.database import Session

#Creamos los routers para la api

paciente_router = APIRouter()


class Paciente (BaseModel):
    id: Optional[int] = None 
    name: str = Field(default="Name",min_length=2, max_length=15)
    age: int = Field(default="Edad",gt=0, le=115)
    sex: str = Field(default="Genero",min_length=1, max_length=15)
    symptom: str = Field(default="Sintoma",min_length=2, max_length=50)
    diagnostic: str = Field(default="Diagnostico",min_length=2, max_length=50)
    treatment: str = Field(default="Tratamiento",min_length=2, max_length=200)
    optional: str = Field(default="Opcional",min_length=2, max_length=200)

#creamos la ruta para calcular la probabilidad que un paciente tenga DOLOR DE CABEZA en una base de datos
    
@paciente_router.get('/Hospital/probabilidad-dolor_de_cabeza', tags=['pacientes'], response_model=int)
def get_probabilidad_dolor_de_cabeza() -> int:
        db = Session()
        dolor_de_cabeza = db.query(func.count(PacienteModel.id)).filter(PacienteModel.symptom == "DOLOR DE CABEZA").scalar()
        total_pacientes = db.query(func.count(PacienteModel.id)).scalar()
        probabilidad = dolor_de_cabeza / total_pacientes
        porcentaje = round(probabilidad * 100 , 2)
        return JSONResponse(status_code=200, content=porcentaje)

#creamos la ruta para calcular la probabilidad que un paciente tenga un diagnostic en una base de datos
@paciente_router.get('/Hospital/probabilidad-diagnostico', tags=['pacientes'], response_model=int)
def get_probabilidad_diagnostico(diagnostic:str = Query(min_length=2, max_length=50)) -> int:
        db = Session()
        diagnostico = db.query(func.count(PacienteModel.id)).filter(PacienteModel.diagnostic == diagnostic).scalar()
        total_pacientes = db.query(func.count(PacienteModel.id)).scalar()
        probabilidad = diagnostico / total_pacientes
        porcentaje = round(probabilidad * 100 , 2)
        return JSONResponse(status_code=200, content=porcentaje)

#creamos la ruta para calcular la edad media de los pacientes      
@paciente_router.get('/Hospital/edad-media', tags=['pacientes'], response_model=int)
def get_edad_media() -> int:
        db = Session()
        edad_media = db.query(func.avg(PacienteModel.age)).scalar()
        return JSONResponse(status_code=200, content=edad_media)

#creamos la ruta para calcular la edad maxima de los pacientes
@paciente_router.get('/Hospital/edad-maxima', tags=['pacientes'], response_model=int)
def get_edad_maxima() -> int:
        db = Session()
        edad_maxima = db.query(func.max(PacienteModel.age)).scalar()
        return JSONResponse(status_code=200, content=edad_maxima)

# creamos la ruta para calcular el total de pacientes atendidos en el hospital

@paciente_router.get('/Hospital/total-pacientes', tags=['pacientes'], response_model=int)
def get_pacientes_Totales() -> int:
        db = Session()
        total_pacientes = db.query(func.count(PacienteModel.id)).scalar()
        return JSONResponse(status_code=200, content=total_pacientes)

     
# Creamos la ruta para consultar los pacientes
@paciente_router.get('/Hospital', tags=['pacientes'], response_model=list[Paciente], status_code=200, dependencies=[Depends(JWTBearer())])   
def get_pacientes_Totales_consulta() -> list[Paciente]:
    db = Session()
    result_pacientes = db.query(PacienteModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result_pacientes))

#creamos la ruta para consultar por id del paciente
@paciente_router.get('/Hospital/{id}', tags=['pacientes'], response_model=Paciente, )
def get_pacientes_by_id_consulta(id: int = Path(ge=1,)) -> Paciente:
    db = Session ()
    result_pacientes = db.query(PacienteModel).filter(PacienteModel.id == id).first()
    if not result_pacientes:
        return JSONResponse(status_code=404,content=["paciente no encontrado"])
    return JSONResponse(status_code=200,content=jsonable_encoder(result_pacientes))
   
# creamos la ruta para consultar pacientes por el name usando parametros QUERY,\
@paciente_router.get('/Hospital/', tags=['pacientes'], response_model=List[Paciente])
def get_pacientes_by_name_consulta( name:str = Query(min_length=2, max_length=15)) -> List[Paciente]:
    db = Session()
    result_pacientes = db.query(PacienteModel).filter(PacienteModel.name == name).all()
    if not result_pacientes:
        return JSONResponse(status_code=404,content=["paciente no encontrado"])
    return JSONResponse(status_code=200,content=jsonable_encoder(result_pacientes))

               
# metodo POST para crear un nuevo paciente y guardar en la lista pacientes
@paciente_router.post('/Hospital', tags=['pacientes'],response_model=dict,status_code=201)
def create_pacientes(paciente: Paciente) -> dict:
    db = Session()
    new_paciente = PacienteModel(**paciente.model_dump())
    db.add(new_paciente)
    db.commit()
    return JSONResponse(status_code=201,content={"message": "paciente creado exitosamente"})

## crear el metodo PUT para actualizar la informacion del paciente
@paciente_router.put('/Hospital/{id}', tags=['pacientes'],response_model=dict,status_code=200)
def update_paciente_actualizar(id:int, paciente: Paciente) -> dict:
    db = Session()
    result_pacientes = db.query(PacienteModel).filter(PacienteModel.id == id).first()
    if not result_pacientes:
        return JSONResponse(status_code=404,content=["paciente no encontrado"])
    result_pacientes.name = paciente.name
    result_pacientes.age = paciente.age
    result_pacientes.sex = paciente.sex
    result_pacientes.symptom = paciente.symptom
    result_pacientes.diagnostic = paciente.diagnostic
    result_pacientes.treatment = paciente.treatment
    result_pacientes.optional = paciente.optional
    db.commit()
    return JSONResponse(status_code=200,content={"message": "paciente actualizado exitosamente"})   
    
## crear el metodo DELETE para eliminar la informacion del paciente
@paciente_router.delete('/Hospital/{id}', tags=['pacientes'],response_model=dict,status_code=200)
def delete_paciente_eliminar(id:int) -> dict:
    db = Session()
    result_pacientes = db.query(PacienteModel).filter(PacienteModel.id == id).first()
    if not result_pacientes:
        return JSONResponse(status_code=404,content=["paciente no encontrado"])
    db.delete(result_pacientes)
    db.commit()
    return JSONResponse(status_code=200,content={"message": "paciente eliminado exitosamente"})


















  




