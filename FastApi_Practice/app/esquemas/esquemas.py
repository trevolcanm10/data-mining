from pydantic import BaseModel

#Lo que el frontend manda al crear
class CrearUsuario(BaseModel):
    nombre:str
    edad: int
    email: str
    
#Lo que el fronted manda al actualizar
class ActualizarUsuario(BaseModel):
    nombre: str
    edad: int
    email: str
    
#Respuesta de la API
class UsuarioOut(BaseModel):
    id: int
    nombre: str
    edad: int
    email: str
    
    class Config:
        from_attributes = True #Para que funcione con SQLAlchemy