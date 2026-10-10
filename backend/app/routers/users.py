from fastapi import APIRouter, HTTPException, status
from app.database.connection import fetch_ords
from app.models.user import UserCreate, UserUpdate

router = APIRouter(
    prefix="/api/usuarios",
    tags=["Usuarios"]
)

@router.get("/", summary="Obtener todos los usuarios")
def get_usuarios():
    try:
        data = fetch_ords("usuarios")
        return {"data": data.get("items", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", summary="Crear un nuevo usuario", status_code=status.HTTP_201_CREATED)
def create_usuario(user: UserCreate):
    try:
        # Enviamos los datos en formato JSON a ORDS / AutoREST
        payload = user.dict()
        response = fetch_ords("usuarios", method="POST", data=payload)
        return {"message": "Usuario creado exitosamente", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))