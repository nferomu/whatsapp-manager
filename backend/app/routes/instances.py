from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.supabase_service import supabase
from app.services.evolution_service import create_instance, delete_instance, get_instances, get_instance_status
from app.dependencies import get_user_id

router = APIRouter()

class InstanceCreate(BaseModel):
    name: str
    phone_number: str
    integration: str

@router.post("/create")
async def create_instance_route(data: InstanceCreate, user_id: str = Depends(get_user_id)):
    try:
        result = await create_instance(
            instance_name=data.name,
            phone_number=data.phone_number,
            integration=data.integration
        )

        instance_data = result.get("instance", {})
        instance_id = instance_data.get("instanceId")
        instance_hash = result.get("hash")
        qrcode_base64 = result.get("qrcode", {}).get("base64")

        # Salva no Supabase
        supabase_result = supabase.table("instances").insert({
            "name": data.name,
            "phone_number": data.phone_number,
            "integration": data.integration,
            "instance_id": instance_id,
            "instance_hash": instance_hash,
            "qrcode": qrcode_base64, 
            "status": instance_data.get("status", "disconnected"),
            "user_id": user_id
        }).execute()

        return {"message": "Instância criada com sucesso!", "instance_id": instance_id, "data": supabase_result.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_instances(user_id: str = Depends(get_user_id)):
    """Lista todas as instâncias do usuário logado"""
    data = supabase.table("instances").select("*").eq("user_id", user_id).execute()
    return data.data


@router.delete("/{instance_id}")
async def delete_instance_route(instance_id: str, user_id: str = Depends(get_user_id)):
    """Remove a instância do Evolution e do Supabase"""
    try:
        # Busca os dados da instância para obter o nome
        instance_data = supabase.table("instances").select("name, instance_id").eq("instance_id", instance_id).eq("user_id", user_id).execute()
        
        if not instance_data.data:
            raise HTTPException(status_code=404, detail="Instância não encontrada ou não pertence ao usuário")
        
        instance_name = instance_data.data[0]["name"]
        
        # Deleta no Evolution API usando o nome da instância
        await delete_instance(instance_name)
        
        # Deleta no Supabase usando o instance_id
        supabase.table("instances").delete().eq("instance_id", instance_id).eq("user_id", user_id).execute()
        
        return {"message": f"Instância {instance_name} removida com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{instance_key}")
async def get_instance_status_route(instance_key: str, user_id: str = Depends(get_user_id)):
    """Obtém o status atual de uma instância"""
    try:
        # Verifica se a instância pertence ao usuário
        instance_check = supabase.table("instances").select("id").eq("instance_id", instance_key).eq("user_id", user_id).execute()
        if not instance_check.data:
            raise HTTPException(status_code=404, detail="Instância não encontrada ou não pertence ao usuário")
        
        status_data = await get_instance_status(instance_key)
        
        # Atualiza o status no Supabase
        supabase.table("instances").update({"status": status_data.get("state", "disconnected")}).eq("instance_id", instance_key).eq("user_id", user_id).execute()
        
        return status_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh-status")
async def refresh_all_instances_status(user_id: str = Depends(get_user_id)):
    """Atualiza o status de todas as instâncias do usuário"""
    try:
        # Busca todas as instâncias do usuário
        instances = supabase.table("instances").select("instance_id").eq("user_id", user_id).execute()
        
        updated_instances = []
        for instance in instances.data:
            try:
                status_data = await get_instance_status(instance["instance_id"])
                new_status = status_data.get("state", "disconnected")
                
                # Atualiza no Supabase
                supabase.table("instances").update({"status": new_status}).eq("instance_id", instance["instance_id"]).eq("user_id", user_id).execute()
                
                updated_instances.append({
                    "instance_id": instance["instance_id"],
                    "status": new_status
                })
            except Exception as e:
                print(f"Erro ao atualizar status da instância {instance['instance_id']}: {e}")
                continue
        
        return {"message": "Status atualizado", "instances": updated_instances}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
