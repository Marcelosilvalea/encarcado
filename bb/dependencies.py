from fastapi import Header, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
from auth import decode_jwt_token, validate_token
from repositories import JSONResponse as RepoJSONResponse

# Schema de segurança para Bearer Token
security = HTTPBearer()

async def get_db_session():
    """
    Dependência que fornece uma sessão do banco de dados
    Garante fechamento automático após uso
    """
    db = get_db()
    try:
        yield db
    finally:
        db.close()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    Dependência que extrai e valida o JWT, retornando o ID do usuário
    Lança HTTPException 401 se o token for inválido
    """
    token = credentials.credentials
    payload = decode_jwt_token(token)

    if not payload or "error" in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "message": "Acesso não autorizado",
                "error": payload.get("error", "Token inválido") if payload else "Token inválido",
                "data": None
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload["user_id"]

async def get_current_user_email(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependência que retorna o email do usuário atual
    """
    token = credentials.credentials
    payload = decode_jwt_token(token)

    if not payload or "error" in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "message": "Acesso não autorizado",
                "error": "Token inválido",
                "data": None
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload["email"]

async def get_current_user_data(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependência que retorna todos os dados do payload do JWT
    """
    token = credentials.credentials
    validation = validate_token(token)

    if not validation["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=validation,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return validation["data"]

class JSONResponse:
    """
    Helper para padronizar respostas JSON no FastAPI
    """
    @staticmethod
    def success(data=None, message="Operação realizada com sucesso"):
        return {
            "success": True,
            "message": message,
            "data": data
        }

    @staticmethod
    def error(message="Erro na operação", error=None, data=None):
        response = {
            "success": False,
            "message": message,
        }
        if error:
            response["error"] = error
        if data is not None:
            response["data"] = data
        return response

    @staticmethod
    def raise_unauthorized(detail="Token inválido ou expirado"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "message": "Acesso não autorizado",
                "error": detail,
                "data": None
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def raise_forbidden(detail="Permissões insuficientes"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "message": "Acesso negado",
                "error": detail,
                "data": None
            }
        )

    @staticmethod
    def raise_not_found(detail="Recurso não encontrado"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "message": "Não encontrado",
                "error": detail,
                "data": None
            }
        )

    @staticmethod
    def raise_bad_request(detail="Requisição inválida"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "Erro na requisição",
                "error": detail,
                "data": None
            }
        )