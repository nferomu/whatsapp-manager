from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .services.supabase_service import supabase  # usa a instância já existente

security = HTTPBearer()

async def get_user_id(token: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Retorna o ID do usuário logado no Supabase.
    """
    if not token or not token.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token não fornecido")

    try:
        user_resp = supabase.auth.get_user(token.credentials)
        user = user_resp.user
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado")
        return user.id  # retorna apenas o ID
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado")
