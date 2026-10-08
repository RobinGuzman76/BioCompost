from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import roles

app = FastAPI(
    title="BioCompost API",
    description="API REST para la gestión y trazabilidad de compostaje agrícola",
    version="1.0.0"
)

# Configuración de CORS para conexión con el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers de la API
app.include_router(roles.router)

@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "status": "online",
        "system": "BioCompost API REST",
        "documentation": "/docs"
    }
