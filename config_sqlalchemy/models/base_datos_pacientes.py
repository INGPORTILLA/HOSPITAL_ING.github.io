
from config_sqlalchemy.database import Base
from sqlalchemy import Column, Integer, String

# Creamos el modelo para la tabla pacientes

class Paciente(Base):

    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    sex = Column(String(50))
    symptom = Column(String(50))
    diagnostic = Column(String(50))
    treatment = Column(String(50))
    optional = Column(Integer)
    
   

    





