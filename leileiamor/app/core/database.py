"""
Configurações do Banco de Dados
"""
import os  # ADICIONAR ESTE IMPORT
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ============================================================================
# CONFIGURAÇÃO VIA VARIÁVEIS DE AMBIENTE (Docker)
# ============================================================================
# Pega do ambiente ou usa valor padrão (localhost para desenvolvimento local)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:aluno@localhost:5432/leidiane"  # fallback para localhost
)

SECRET_KEY = os.getenv("SECRET_KEY", "1234")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
# ============================================================================

# Criação do engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# SessionLocal para criar sessões de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM
Base = declarative_base()


def get_db():
    """
    Dependency para obter sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()