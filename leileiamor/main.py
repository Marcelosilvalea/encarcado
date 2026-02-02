"""
Arquivo Principal da API FastAPI
Contém configuração do app, seed de dados e rotas
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

from app.core.database import engine, Base, get_db
from app.core.security import get_password_hash
from app.models.usuario import Usuario
from app.models.conta import Conta
from app.models.categoria import Categoria
from app.models.transacao import Transacao
from app.routers import auth, usuarios, contas, categorias, transacoes
from app.schemas.schemas import MessageResponse

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Configuração do Swagger para autenticação JWT
app = FastAPI(
    title="API de Controle Financeiro",
    description="""
    ## API RESTful completa para controle financeiro pessoal
    
    ### Funcionalidades:
    * 🔐 **Autenticação JWT** - Login seguro com tokens
    * 👤 **Gerenciamento de Usuários** - CRUD completo
    * 💰 **Contas** - Gerencie suas contas bancárias
    * 📑 **Categorias** - Organize receitas e despesas
    * 💸 **Transações** - Registre e acompanhe movimentações financeiras
    
    ### Como usar a autenticação no Swagger:
    1. Primeiro, crie um usuário em `POST /usuarios` (não requer auth)
    2. Faça login em `POST /auth/login` com email e senha
    3. Copie o `access_token` retornado
    4. Clique no botão **Authorize** 🔓 (canto superior direito)
    5. Cole o token no campo e clique em **Authorize**
    6. Agora você pode acessar as rotas protegidas! 🎉
    
    ### Estrutura do Sistema:
    - **Usuário** possui várias **Contas** e **Categorias**
    - Cada **Transação** está vinculada a uma Conta e Categoria
    - Saldo das contas é atualizado automaticamente com as transações
    """,
    version="2.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True,
    }
)

# Registra os routers
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(contas.router)
app.include_router(categorias.router)
app.include_router(transacoes.router)


@app.get("/", tags=["Root"])
def root():
    """
    Endpoint raiz da API
    """
    return {
        "message": "Bem-vindo à API de Controle Financeiro!",
        "docs": "/docs",
        "version": "2.0.0",
        "endpoints": {
            "auth": "/auth/login",
            "usuarios": "/usuarios",
            "contas": "/contas",
            "categorias": "/categorias",
            "transacoes": "/transacoes"
        }
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Verifica se a API está funcionando
    """
    return {"status": "healthy", "message": "API está online"}


# ============================================================================
# FUNÇÃO DE SEED - DADOS FICTÍCIOS PARA TESTE (COMENTADA)
# ============================================================================
# IMPORTANTE: Esta função está comentada porque precisa ser ajustada após
# conectar ao banco de dados real. Descomente e adapte conforme necessário.
# ============================================================================

# @app.post("/seed", response_model=MessageResponse, tags=["Seed"])
# def seed_database(db: Session = Depends(get_db)):
#     """
#     Popula o banco de dados com dados fictícios para teste
#     
#     Este endpoint cria:
#     - 2 usuários de exemplo
#     - 3 contas para cada usuário
#     - 6 categorias para cada usuário (3 receitas, 3 despesas)
#     - 10 transações de exemplo para o primeiro usuário
#     
#     **ATENÇÃO:** Verifique se os dados já existem antes de executar!
#     """
#     try:
#         # Verifica se já existem dados
#         existing_users = db.query(Usuario).count()
#         
#         if existing_users > 0:
#             return {
#                 "message": "Banco de dados já contém dados",
#                 "detail": f"Usuários existentes: {existing_users}"
#             }
#         
#         # ========================================
#         # SEED DE USUÁRIOS
#         # ========================================
#         usuario1 = Usuario(
#             nome="João Silva",
#             email="joao@example.com",
#             senha=get_password_hash("senha123")
#         )
#         usuario2 = Usuario(
#             nome="Maria Santos",
#             email="maria@example.com",
#             senha=get_password_hash("senha456")
#         )
#         
#         db.add(usuario1)
#         db.add(usuario2)
#         db.commit()
#         db.refresh(usuario1)
#         db.refresh(usuario2)
#         
#         # ========================================
#         # SEED DE CONTAS
#         # ========================================
#         contas_usuario1 = [
#             Conta(nome="Conta Corrente", saldo=Decimal("5000.00"), tipo="corrente", id_usuario=usuario1.id_usuario),
#             Conta(nome="Poupança", saldo=Decimal("10000.00"), tipo="poupanca", id_usuario=usuario1.id_usuario),
#             Conta(nome="Investimentos", saldo=Decimal("25000.00"), tipo="investimento", id_usuario=usuario1.id_usuario),
#         ]
#         
#         contas_usuario2 = [
#             Conta(nome="Conta Corrente", saldo=Decimal("3000.00"), tipo="corrente", id_usuario=usuario2.id_usuario),
#             Conta(nome="Carteira Digital", saldo=Decimal("500.00"), tipo="digital", id_usuario=usuario2.id_usuario),
#         ]
#         
#         for conta in contas_usuario1 + contas_usuario2:
#             db.add(conta)
#         db.commit()
#         
#         # Refresh para obter IDs
#         for conta in contas_usuario1:
#             db.refresh(conta)
#         
#         # ========================================
#         # SEED DE CATEGORIAS
#         # ========================================
#         categorias_usuario1 = [
#             # Receitas
#             Categoria(nome="Salário", tipo="receita", id_usuario=usuario1.id_usuario),
#             Categoria(nome="Freelance", tipo="receita", id_usuario=usuario1.id_usuario),
#             Categoria(nome="Investimentos", tipo="receita", id_usuario=usuario1.id_usuario),
#             # Despesas
#             Categoria(nome="Alimentação", tipo="despesa", id_usuario=usuario1.id_usuario),
#             Categoria(nome="Transporte", tipo="despesa", id_usuario=usuario1.id_usuario),
#             Categoria(nome="Moradia", tipo="despesa", id_usuario=usuario1.id_usuario),
#         ]
#         
#         for categoria in categorias_usuario1:
#             db.add(categoria)
#         db.commit()
#         
#         # Refresh para obter IDs
#         for categoria in categorias_usuario1:
#             db.refresh(categoria)
#         
#         # ========================================
#         # SEED DE TRANSAÇÕES
#         # ========================================
#         transacoes = [
#             # Receitas
#             Transacao(
#                 valor=Decimal("5000.00"),
#                 data=date(2025, 1, 1),
#                 descricao="Salário Janeiro",
#                 tipo="receita",
#                 id_usuario=usuario1.id_usuario,
#                 id_conta=contas_usuario1[0].id_conta,
#                 id_categoria=categorias_usuario1[0].id_categoria
#             ),
#             Transacao(
#                 valor=Decimal("1500.00"),
#                 data=date(2025, 1, 15),
#                 descricao="Projeto Freelance",
#                 tipo="receita",
#                 id_usuario=usuario1.id_usuario,
#                 id_conta=contas_usuario1[0].id_conta,
#                 id_categoria=categorias_usuario1[1].id_categoria
#             ),
#             # Despesas
#             Transacao(
#                 valor=Decimal("800.00"),
#                 data=date(2025, 1, 5),
#                 descricao="Aluguel",
#                 tipo="despesa",
#                 id_usuario=usuario1.id_usuario,
#                 id_conta=contas_usuario1[0].id_conta,
#                 id_categoria=categorias_usuario1[5].id_categoria
#             ),
#             Transacao(
#                 valor=Decimal("250.00"),
#                 data=date(2025, 1, 8),
#                 descricao="Mercado",
#                 tipo="despesa",
#                 id_usuario=usuario1.id_usuario,
#                 id_conta=contas_usuario1[0].id_conta,
#                 id_categoria=categorias_usuario1[3].id_categoria
#             ),
#             Transacao(
#                 valor=Decimal("150.00"),
#                 data=date(2025, 1, 10),
#                 descricao="Gasolina",
#                 tipo="despesa",
#                 id_usuario=usuario1.id_usuario,
#                 id_conta=contas_usuario1[0].id_conta,
#                 id_categoria=categorias_usuario1[4].id_categoria
#             ),
#         ]
#         
#         for transacao in transacoes:
#             db.add(transacao)
#         
#         db.commit()
#         
#         return {
#             "message": "Seed executado com sucesso!",
#             "detail": f"Criados: 2 usuários, {len(contas_usuario1) + len(contas_usuario2)} contas, "
#                      f"{len(categorias_usuario1)} categorias, {len(transacoes)} transações. "
#                      f"Use 'joao@example.com / senha123' para login."
#         }
#         
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=500,
#             detail=f"Erro ao executar seed: {str(e)}"
#         )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
