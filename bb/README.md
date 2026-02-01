# Sistema de Banco de Dados e Autenticação

Sistema de gerenciamento financeiro com autenticação JWT e PostgreSQL.

## Estrutura do Projeto

```
.
├── database.py       # Conexão com PostgreSQL
├── models.py         # Models SQLAlchemy (Usuario, Conta, Categoria, Transacao)
├── auth.py           # Autenticação e JWT
├── seed.py           # Popular banco com dados iniciais
├── .env.example      # Exemplo de variáveis de ambiente
└── requirements.txt  # Dependências Python
```

## Requisitos

- Python 3.8+
- PostgreSQL 12+

## Configuração

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar PostgreSQL

Criar o banco de dados:

```sql
CREATE DATABASE sistema;
```

### 3. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e ajuste as credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais do PostgreSQL.

### 4. Popular o banco de dados

```bash
python seed.py
```

## Uso

### Autenticação

```python
from auth import authenticate_user

# Autenticar usuário
result = authenticate_user("joao@email.com", "senha123")

if result:
    print(f"Token JWT: {result['token']}")
    print(f"Usuário: {result['nome']}")
else:
    print("Falha na autenticação")
```

### Validar Token JWT

```python
from auth import decode_jwt_token

payload = decode_jwt_token(token)
if payload:
    print(f"Token válido para user_id: {payload['user_id']}")
```

## Credenciais de Teste

Após executar o seed, você pode usar:

- **Email:** joao@email.com | **Senha:** senha123
- **Email:** maria@email.com | **Senha:** senha456
- **Email:** pedro@email.com | **Senha:** senha789

## Modelo de Dados

### USUARIO
- id_usuario (PK)
- nome
- email (único)
- senha (hash SHA-256)

### CONTA
- id_conta (PK)
- nome
- saldo
- tipo
- id_usuario (FK)

### CATEGORIA
- id_categoria (PK)
- nome
- tipo
- id_usuario (FK)

### TRANSACAO
- id_transacao (PK)
- valor
- data
- descricao
- tipo
- id_usuario (FK)
- id_conta (FK)
- id_categoria (FK)

## Segurança

- Senhas armazenadas com hash SHA-256
- Tokens JWT com expiração configurável
- Credenciais do banco carregadas de variáveis de ambiente
