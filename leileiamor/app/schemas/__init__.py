"""
Schemas Pydantic da aplicação
Exporta todos os schemas para validação e serialização de dados
"""

from app.schemas.schemas import (
    # Schemas de Usuário
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    
    # Schemas de Autenticação
    Token,
    LoginRequest,
    
    # Schemas de Conta
    ContaBase,
    ContaCreate,
    ContaUpdate,
    ContaResponse,
    
    # Schemas de Categoria
    CategoriaBase,
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse,
    
    # Schemas de Transação
    TransacaoBase,
    TransacaoCreate,
    TransacaoUpdate,
    TransacaoResponse,
    
    # Schemas Genéricos
    MessageResponse,
)

__all__ = [
    # Usuário
    "UsuarioBase",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioResponse",
    
    # Autenticação
    "Token",
    "LoginRequest",
    
    # Conta
    "ContaBase",
    "ContaCreate",
    "ContaUpdate",
    "ContaResponse",
    
    # Categoria
    "CategoriaBase",
    "CategoriaCreate",
    "CategoriaUpdate",
    "CategoriaResponse",
    
    # Transação
    "TransacaoBase",
    "TransacaoCreate",
    "TransacaoUpdate",
    "TransacaoResponse",
    
    # Genéricos
    "MessageResponse",
]