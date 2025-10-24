import httpx
import os
from dotenv import load_dotenv

load_dotenv()

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")

# Cria cliente HTTP compartilhado
client = httpx.AsyncClient(timeout=15.0)

async def create_instance(instance_name: str, phone_number: str, integration: str = "WHATSAPP-BAILEYS"):
    payload = {
        "instanceName": instance_name,
        "phoneNumber": phone_number,
        "qrcode": True,
        "integration": integration
    }

    headers = {"apikey": EVOLUTION_API_KEY}

    response = await client.post(f"{EVOLUTION_API_URL}/instance/create", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

async def delete_instance(instance_name: str):
    """Remove uma instância do Evolution API usando o nome da instância."""
    headers = {"apikey": EVOLUTION_API_KEY}
    response = await client.delete(f"{EVOLUTION_API_URL}/instance/delete/{instance_name}", headers=headers)
    response.raise_for_status()
    return response.json()

async def get_instances():
    """Lista todas as instâncias do Evolution API."""
    headers = {"apikey": EVOLUTION_API_KEY}
    response = await client.get(f"{EVOLUTION_API_URL}/instance/list", headers=headers)
    response.raise_for_status()
    return response.json()

async def get_instance_status(instance_key: str):
    """Obtém o status atual de uma instância."""
    headers = {"apikey": EVOLUTION_API_KEY}
    response = await client.get(f"{EVOLUTION_API_URL}/instance/connectionState/{instance_key}", headers=headers)
    response.raise_for_status()
    return response.json()
