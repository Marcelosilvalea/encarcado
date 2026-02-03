"""
Routers da API FastAPI
Contém todos os endpoints organizados por recurso
"""

from app.routers import auth, usuarios, contas, categorias, transacoes

__all__ = [
    "auth",
    "usuarios",
    "contas",
    "categorias",
    "transacoes",
]