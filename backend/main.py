from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import roles, users

app = FastAPI(
    title="BioCompost API",
    version="1.0.0",
    description="API backend para la gestión del proyecto BioCompost"
)

# Configuración de CORS para permitir solicitudes desde el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo luego a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los routers de la aplicación
app.include_router(roles.router)
app.include_router(users.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido a la API de BioCompost en funcionamiento"}