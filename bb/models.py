from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from decimal import Decimal
from datetime import date, datetime
import json

class CustomJSONEncoder(json.JSONEncoder):
    """Encoder personalizado para lidar com Decimal e Date"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

class Usuario(Base):
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

    contas = relationship('Conta', back_populates='usuario', cascade='all, delete-orphan')
    categorias = relationship('Categoria', back_populates='usuario', cascade='all, delete-orphan')
    transacoes = relationship('Transacao', back_populates='usuario', cascade='all, delete-orphan')

    def to_dict(self, include_relationships=False):
        data = {
            'id_usuario': self.id_usuario,
            'nome': self.nome,
            'email': self.email
        }
        if include_relationships:
            data['contas'] = [conta.to_dict() for conta in self.contas]
            data['categorias'] = [cat.to_dict() for cat in self.categorias]
            data['transacoes'] = [trans.to_dict() for trans in self.transacoes]
        return data

    def to_json(self, include_relationships=False):
        return json.dumps(self.to_dict(include_relationships), cls=CustomJSONEncoder)

class Conta(Base):
    __tablename__ = 'conta'

    id_conta = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    saldo = Column(Numeric(15, 2), nullable=False, default=0.00)
    tipo = Column(String(50), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)

    usuario = relationship('Usuario', back_populates='contas')
    transacoes = relationship('Transacao', back_populates='conta', cascade='all, delete-orphan')

    def to_dict(self, include_usuario=False, include_transacoes=False):
        data = {
            'id_conta': self.id_conta,
            'nome': self.nome,
            'saldo': float(self.saldo) if self.saldo else 0.0,
            'tipo': self.tipo,
            'id_usuario': self.id_usuario
        }
        if include_usuario:
            data['usuario'] = self.usuario.to_dict() if self.usuario else None
        if include_transacoes:
            data['transacoes'] = [trans.to_dict() for trans in self.transacoes]
        return data

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(**kwargs), cls=CustomJSONEncoder)

class Categoria(Base):
    __tablename__ = 'categoria'

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)

    usuario = relationship('Usuario', back_populates='categorias')
    transacoes = relationship('Transacao', back_populates='categoria', cascade='all, delete-orphan')

    def to_dict(self, include_usuario=False, include_transacoes=False):
        data = {
            'id_categoria': self.id_categoria,
            'nome': self.nome,
            'tipo': self.tipo,
            'id_usuario': self.id_usuario
        }
        if include_usuario:
            data['usuario'] = self.usuario.to_dict() if self.usuario else None
        if include_transacoes:
            data['transacoes'] = [trans.to_dict() for trans in self.transacoes]
        return data

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(**kwargs), cls=CustomJSONEncoder)

class Transacao(Base):
    __tablename__ = 'transacao'

    id_transacao = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Numeric(15, 2), nullable=False)
    data = Column(Date, nullable=False)
    descricao = Column(String(500), nullable=False)
    tipo = Column(String(50), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    id_conta = Column(Integer, ForeignKey('conta.id_conta'), nullable=False)
    id_categoria = Column(Integer, ForeignKey('categoria.id_categoria'), nullable=False)

    usuario = relationship('Usuario', back_populates='transacoes')
    conta = relationship('Conta', back_populates='transacoes')
    categoria = relationship('Categoria', back_populates='transacoes')

    def to_dict(self, include_relationships=False):
        data = {
            'id_transacao': self.id_transacao,
            'valor': float(self.valor) if self.valor else 0.0,
            'data': self.data.isoformat() if self.data else None,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'id_usuario': self.id_usuario,
            'id_conta': self.id_conta,
            'id_categoria': self.id_categoria
        }
        if include_relationships:
            data['usuario'] = self.usuario.to_dict() if self.usuario else None
            data['conta'] = self.conta.to_dict() if self.conta else None
            data['categoria'] = self.categoria.to_dict() if self.categoria else None
        return data

    def to_json(self, include_relationships=False):
        return json.dumps(self.to_dict(include_relationships), cls=CustomJSONEncoder)
