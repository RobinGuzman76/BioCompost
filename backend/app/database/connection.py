import os
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

ORDS_BASE_URL = os.getenv("ORDS_BASE_URL", "https://apex.oracle.com/ords/biocompost").rstrip("/")

def fetch_ords(endpoint: str, method: str = "GET", data: dict = None):
    """
    Realiza peticiones a la API ORDS de Oracle APEX usando requests.
    """
    clean_endpoint = endpoint.strip("/")
    url = f"{ORDS_BASE_URL}/{clean_endpoint}/"
    
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, verify=False, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, verify=False, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, verify=False, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, verify=False, timeout=10)
            
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as exc:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    except Exception as exc:
        raise Exception(f"Error al conectar con ORDS ({url}): {str(exc)}")
