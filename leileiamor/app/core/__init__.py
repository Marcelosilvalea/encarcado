"""
Core da aplicação
Contém configurações, segurança, banco de dados e utilitários
"""

from app.core.database import engine, Base, SessionLocal, get_db, DATABASE_URL, SECRET_KEY
from app.core.security import (
    verify_password,
    hash_password,
    get_password_hash,
    create_access_token,
    get_current_user,
)

__all__ = [
    # Database
    "engine",
    "Base",
    "SessionLocal",
    "get_db",
    "DATABASE_URL",
    "SECRET_KEY",
    
    # Security
    "verify_password",
    "hash_password",
    "get_password_hash",
    "create_access_token",
    "get_current_user",
]