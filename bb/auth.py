import os
import hashlib
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from models import Usuario
from database import get_db

# Carregar variáveis de ambiente
load_dotenv()

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_secret_key')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))


def hash_password(password: str) -> str:
    """
    Gera o hash SHA-256 de uma senha
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha corresponde ao hash armazenado
    """
    return hash_password(plain_password) == hashed_password


def generate_jwt_token(user_id: int, email: str) -> str:
    """
    Gera um token JWT válido
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt_token(token: str) -> dict:
    """
    Decodifica e valida um token JWT
    Retorna o payload se válido, caso contrário retorna None
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expirado", "valid": False}
    except jwt.InvalidTokenError:
        return {"error": "Token inválido", "valid": False}


def authenticate_user(email: str, password: str) -> dict:
    """
    Autentica um usuário no banco de dados
    Retorna um dicionário JSON com os dados do usuário e token JWT se autenticado
    Retorna JSON de erro se a autenticação falhar
    """
    db = get_db()

    try:
        # Buscar usuário por email
        usuario = db.query(Usuario).filter(Usuario.email == email).first()

        if not usuario:
            return {
                "success": False,
                "message": "Falha na autenticação",
                "error": "Usuário não encontrado",
                "data": None
            }

        # Verificar senha
        if not verify_password(password, usuario.senha):
            return {
                "success": False,
                "message": "Falha na autenticação",
                "error": "Senha incorreta",
                "data": None
            }

        # Gerar token JWT
        token = generate_jwt_token(usuario.id_usuario, usuario.email)

        # Retornar dados em formato JSON consistente
        return {
            "success": True,
            "message": "Autenticação realizada com sucesso",
            "data": {
                "id_usuario": usuario.id_usuario,
                "nome": usuario.nome,
                "email": usuario.email,
                "token": token,
                "token_type": "Bearer"
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Erro interno na autenticação",
            "error": str(e),
            "data": None
        }
    finally:
        db.close()


def validate_token(token: str) -> dict:
    """
    Valida um token JWT e retorna JSON padronizado
    """
    payload = decode_jwt_token(token)

    if payload is None:
        return {
            "success": False,
            "message": "Token inválido",
            "data": {"valid": False}
        }

    if "error" in payload:
        return {
            "success": False,
            "message": payload["error"],
            "data": {"valid": False, "error": payload["error"]}
        }

    return {
        "success": True,
        "message": "Token válido",
        "data": {
            "valid": True,
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "expires_at": datetime.fromtimestamp(payload.get("exp")).isoformat() if payload.get("exp") else None
        }
    }


def get_current_user_from_token(token: str) -> dict:
    """
    Obtém os dados do usuário atual a partir do token JWT
    Retorna JSON com dados do usuário ou erro
    """
    validation = validate_token(token)

    if not validation["success"]:
        return validation

    user_id = validation["data"]["user_id"]

    db = get_db()
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()

        if not usuario:
            return {
                "success": False,
                "message": "Usuário não encontrado",
                "data": None
            }

        return {
            "success": True,
            "message": "Usuário recuperado com sucesso",
            "data": usuario.to_dict()
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Erro ao recuperar usuário",
            "error": str(e),
            "data": None
        }
    finally:
        db.close()


# Exemplo de uso
if __name__ == "__main__":
    import json

    # Teste de autenticação
    print("=== TESTE DE AUTENTICAÇÃO ===")
    result = authenticate_user("joao@email.com", "senha123")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["success"]:
        token = result["data"]["token"]

        # Testar validação do token
        print("\n=== VALIDAÇÃO DO TOKEN ===")
        validation = validate_token(token)
        print(json.dumps(validation, indent=2, ensure_ascii=False))

        # Testar recuperação de usuário
        print("\n=== RECUPERAÇÃO DE USUÁRIO ===")
        user_data = get_current_user_from_token(token)
        print(json.dumps(user_data, indent=2, ensure_ascii=False))
