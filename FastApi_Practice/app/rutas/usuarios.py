from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal,UsuarioDB
from app.esquemas.esquemas import CrearUsuario,ActualizarUsuario,UsuarioOut

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

    
def traer_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/",response_model=UsuarioOut)
def crear_usuario(usuario:CrearUsuario,db:Session = Depends(traer_db)):
    
    nuevo_usuario = UsuarioDB(
        nombre = usuario.nombre,
        edad = usuario.edad,
        email = usuario.email
    )
    
    db.add(nuevo_usuario)#prepara
    db.commit()#guarda en DB
    db.refresh(nuevo_usuario)#ID generado
    
    return nuevo_usuario
    


@router.get("/",response_model=list[UsuarioOut])
def traer_usuarios(db: Session = Depends(traer_db)):
    usuarios = db.query(UsuarioDB).all() #SELECT * FROM usuarios
    return usuarios

@router.get("/{id}",response_model=UsuarioOut)
def traer_usuario(id:int,db: Session = Depends(traer_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{id}",response_model=UsuarioOut)
def actualizar_usuario(id: int,datos: ActualizarUsuario, db: Session = Depends(traer_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.nombre = datos.nombre
    usuario.edad = datos.edad
    usuario.email = datos.email
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{id}")
def eliminar_usuario(id:int,db: Session = Depends(traer_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    
    if not usuario:
        raise HTTPException(status_code=404,detail="Usuaio no encontrado")
    db.delete(usuario)
    db.commit()
    return {"mensaje":"Usuario eliminado correctamente"}