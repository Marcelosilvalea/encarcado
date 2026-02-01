from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Usuario, Conta, Categoria, Transacao
from database import get_db
import json

class JSONResponse:
    """Helper para padronizar respostas JSON"""
    @staticmethod
    def success(data: Any = None, message: str = "Operação realizada com sucesso") -> Dict:
        return {
            "success": True,
            "message": message,
            "data": data
        }

    @staticmethod
    def error(message: str = "Erro na operação", details: str = None) -> Dict:
        response = {
            "success": False,
            "message": message
        }
        if details:
            response["details"] = details
        return response

class UsuarioRepository:
    """Repositório para operações de Usuario - retorna sempre JSON"""

    @staticmethod
    def get_by_id(user_id: int, db: Session = None) -> Dict:
        """Busca usuario por ID retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()

            if close_after:
                db.close()

            if usuario:
                return JSONResponse.success(data=usuario.to_dict())
            return JSONResponse.error("Usuário não encontrado")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar usuário", str(e))

    @staticmethod
    def get_by_email(email: str, db: Session = None) -> Dict:
        """Busca usuario por email retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            usuario = db.query(Usuario).filter(Usuario.email == email).first()

            if close_after:
                db.close()

            if usuario:
                return JSONResponse.success(data=usuario.to_dict())
            return JSONResponse.error("Usuário não encontrado")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar usuário", str(e))

    @staticmethod
    def list_all(db: Session = None) -> Dict:
        """Lista todos os usuários em JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            usuarios = db.query(Usuario).all()
            data = [u.to_dict() for u in usuarios]

            if close_after:
                db.close()

            return JSONResponse.success(data=data, message=f"{len(data)} usuários encontrados")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao listar usuários", str(e))

    @staticmethod
    def get_full_profile(user_id: int, db: Session = None) -> Dict:
        """Retorna perfil completo com relacionamentos em JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()

            if close_after:
                db.close()

            if usuario:
                return JSONResponse.success(data=usuario.to_dict(include_relationships=True))
            return JSONResponse.error("Usuário não encontrado")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar perfil", str(e))

class ContaRepository:
    """Repositório para operações de Conta - retorna sempre JSON"""

    @staticmethod
    def get_by_id(conta_id: int, db: Session = None) -> Dict:
        """Busca conta por ID retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            conta = db.query(Conta).filter(Conta.id_conta == conta_id).first()

            if close_after:
                db.close()

            if conta:
                return JSONResponse.success(data=conta.to_dict())
            return JSONResponse.error("Conta não encontrada")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar conta", str(e))

    @staticmethod
    def get_by_user(user_id: int, db: Session = None) -> Dict:
        """Busca contas do usuário retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            contas = db.query(Conta).filter(Conta.id_usuario == user_id).all()
            data = [c.to_dict() for c in contas]

            if close_after:
                db.close()

            return JSONResponse.success(data=data, message=f"{len(data)} contas encontradas")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar contas", str(e))

    @staticmethod
    def get_with_transacoes(conta_id: int, db: Session = None) -> Dict:
        """Busca conta com transações em JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            conta = db.query(Conta).filter(Conta.id_conta == conta_id).first()

            if close_after:
                db.close()

            if conta:
                return JSONResponse.success(data=conta.to_dict(include_transacoes=True))
            return JSONResponse.error("Conta não encontrada")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar conta", str(e))

class CategoriaRepository:
    """Repositório para operações de Categoria - retorna sempre JSON"""

    @staticmethod
    def get_by_id(categoria_id: int, db: Session = None) -> Dict:
        """Busca categoria por ID retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            categoria = db.query(Categoria).filter(Categoria.id_categoria == categoria_id).first()

            if close_after:
                db.close()

            if categoria:
                return JSONResponse.success(data=categoria.to_dict())
            return JSONResponse.error("Categoria não encontrada")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar categoria", str(e))

    @staticmethod
    def get_by_user(user_id: int, db: Session = None) -> Dict:
        """Busca categorias do usuário retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            categorias = db.query(Categoria).filter(Categoria.id_usuario == user_id).all()
            data = [c.to_dict() for c in categorias]

            if close_after:
                db.close()

            return JSONResponse.success(data=data, message=f"{len(data)} categorias encontradas")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar categorias", str(e))

    @staticmethod
    def get_by_tipo(user_id: int, tipo: str, db: Session = None) -> Dict:
        """Busca categorias por tipo (receita/despesa) retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            categorias = db.query(Categoria).filter(
                Categoria.id_usuario == user_id,
                Categoria.tipo == tipo
            ).all()
            data = [c.to_dict() for c in categorias]

            if close_after:
                db.close()

            return JSONResponse.success(data=data, message=f"{len(data)} categorias de {tipo} encontradas")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar categorias", str(e))

class TransacaoRepository:
    """Repositório para operações de Transacao - retorna sempre JSON"""

    @staticmethod
    def get_by_id(transacao_id: int, db: Session = None) -> Dict:
        """Busca transação por ID retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            transacao = db.query(Transacao).filter(Transacao.id_transacao == transacao_id).first()

            if close_after:
                db.close()

            if transacao:
                return JSONResponse.success(data=transacao.to_dict())
            return JSONResponse.error("Transação não encontrada")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar transação", str(e))

    @staticmethod
    def get_by_user(user_id: int, db: Session = None) -> Dict:
        """Busca transações do usuário retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            transacoes = db.query(Transacao).filter(Transacao.id_usuario == user_id).all()
            data = [t.to_dict() for t in transacoes]

            if close_after:
                db.close()

            return JSONResponse.success(data=data, message=f"{len(data)} transações encontradas")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar transações", str(e))

    @staticmethod
    def get_with_relationships(transacao_id: int, db: Session = None) -> Dict:
        """Busca transação com todos os relacionamentos (conta e categoria) em JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            transacao = db.query(Transacao).filter(Transacao.id_transacao == transacao_id).first()

            if close_after:
                db.close()

            if transacao:
                return JSONResponse.success(data=transacao.to_dict(include_relationships=True))
            return JSONResponse.error("Transação não encontrada")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar transação", str(e))

    @staticmethod
    def get_by_conta(conta_id: int, db: Session = None) -> Dict:
        """Busca transações por conta retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            transacoes = db.query(Transacao).filter(Transacao.id_conta == conta_id).all()
            data = [t.to_dict() for t in transacoes]

            if close_after:
                db.close()

            return JSONResponse.success(data=data, message=f"{len(data)} transações encontradas")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar transações", str(e))

    @staticmethod
    def get_by_categoria(categoria_id: int, db: Session = None) -> Dict:
        """Busca transações por categoria retornando JSON"""
        try:
            if db is None:
                db = get_db()
                close_after = True
            else:
                close_after = False

            transacoes = db.query(Transacao).filter(Transacao.id_categoria == categoria_id).all()
            data = [t.to_dict() for t in transacoes]

            if close_after:
                db.close()

            return JSONResponse.success(data=data, message=f"{len(data)} transações encontradas")

        except SQLAlchemyError as e:
            return JSONResponse.error("Erro ao buscar transações", str(e))


usuario_repo = UsuarioRepository()
conta_repo = ContaRepository()
categoria_repo = CategoriaRepository()
transacao_repo = TransacaoRepository()