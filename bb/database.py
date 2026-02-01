import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'sistema')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

# Engine como None - só será criado quando necessário
_engine = None
_SessionLocal = None

def get_engine():
    global _engine, _SessionLocal
    if _engine is None:
        print(f"[DB] Conectando em {DB_HOST}:{DB_PORT}/{DB_NAME}...", flush=True)
        _engine = create_engine(
            DATABASE_URL, 
            echo=False, 
            pool_pre_ping=True,
            connect_args={"connect_timeout": 5}
        )
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
        print("[DB] Engine criado", flush=True)
    return _engine

def get_db():
    engine = get_engine()
    return _SessionLocal()