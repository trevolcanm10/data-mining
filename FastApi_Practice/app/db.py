from sqlalchemy import Column,Integer,String,create_engine
#Motor que conecta con la base de datos create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Sesision maker crea la fabrica de sesiones
DATABASE_URL = "sqlite:///./usuarios.db"

engine = create_engine(
    DATABASE_URL,connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(
    autocommit= False,
    autoflush=False,
    bind = engine
)

#Base común para todo los modelos
Base = declarative_base()

#Definición de modelos ORM
class UsuarioDB(Base):
    __tablename__= "usuarios" #Nombre real de la tabla dentro de la DB
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    email = Column(String, unique=True, index=True)
    
#Crea la base de datos en la DB si no existen
Base.metadata.create_all(bind=engine)