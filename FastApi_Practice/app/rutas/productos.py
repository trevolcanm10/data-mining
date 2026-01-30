from fastapi import APIRouter

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

@router.get("/")
def traer_productos():
        return ["Laptop","Mouse","Teclado"]
    
@router.get("/{id}")
def traer_producto(id:int):
    return {
        "id": id,
        "nombre": "Producto ejemplo"
    }