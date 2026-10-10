import os
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

ORDS_BASE_URL = os.getenv("ORDS_BASE_URL", "https://apex.oracle.com/ords/biocompost").rstrip("/")

def fetch_ords(endpoint: str, method: str = "GET", data: dict = None):
    """
    Realiza la llamada HTTP a ORDS usando el cliente curl del sistema 
    para evitar el bloqueo WAF/Cloudflare/Akamai de apex.oracle.com.
    """
    clean_endpoint = endpoint.strip("/")
    url = f"{ORDS_BASE_URL}/{clean_endpoint}/"
    
    # Construir el comando curl con cabeceras de navegador real
    cmd = [
        "curl", "-s", "-k", "-L",
        "-X", method,
        "-H", "Accept: application/json, text/plain, */*",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "-H", "Sec-Fetch-Mode: cors",
        "-H", "Sec-Fetch-Site: cross-site",
        url
    ]
    
    if data and method in ["POST", "PUT"]:
        cmd.extend(["-H", "Content-Type: application/json"])
        cmd.extend(["-d", json.dumps(data)])
        
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        raw_output = result.stdout.strip()
        
        # Intentar parsear como JSON
        return json.loads(raw_output)
    except json.JSONDecodeError:
        raise Exception(f"ORDS devolvio una respuesta no valida (HTML/Error): {raw_output[:300]}")
    except subprocess.CalledProcessError as exc:
        raise Exception(f"Error de ejecución curl: {exc.stderr}")
    except Exception as exc:
        raise Exception(f"Error al conectar con ORDS ({url}): {str(exc)}")
