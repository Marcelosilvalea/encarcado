import os
os.environ['PYTHONUNBUFFERED'] = '1'  # Força output imediato no Windows

from datetime import date, timedelta
from decimal import Decimal

print("INICIANDO SEED...")
print("Passo 1: Importando bibliotecas...")

try:
    import psycopg2
    from dotenv import load_dotenv
    print("✓ Bibliotecas básicas OK")
except Exception as e:
    print(f"ERRO: {e}")
    exit(1)

print("\nPasso 2: Carregando .env...")
load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'sistema')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

print(f"✓ Configurações: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print("\nPasso 3: Conectando ao PostgreSQL...")
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.autocommit = False
    cursor = conn.cursor()
    print("✓ Conectado")
except Exception as e:
    print(f"ERRO na conexão: {e}")
    exit(1)

print("\nPasso 4: Criando tabelas...")
try:
    # Criar tabela USUARIO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL
        );
    """)
    
    # Criar tabela CONTA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conta (
            id_conta SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            saldo NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
            tipo VARCHAR(50) NOT NULL,
            id_usuario INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
        );
    """)
    
    # Criar tabela CATEGORIA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            id_usuario INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
        );
    """)
    
    # Criar tabela TRANSACAO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacao (
            id_transacao SERIAL PRIMARY KEY,
            valor NUMERIC(15, 2) NOT NULL,
            data DATE NOT NULL,
            descricao VARCHAR(500) NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            id_usuario INTEGER NOT NULL,
            id_conta INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
            FOREIGN KEY (id_conta) REFERENCES conta(id_conta) ON DELETE CASCADE,
            FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    print("✓ Tabelas criadas")
except Exception as e:
    print(f"ERRO ao criar tabelas: {e}")
    conn.rollback()
    exit(1)

print("\nPasso 5: Limpando dados antigos...")
try:
    cursor.execute("DELETE FROM transacao;")
    cursor.execute("DELETE FROM categoria;")
    cursor.execute("DELETE FROM conta;")
    cursor.execute("DELETE FROM usuario;")
    cursor.execute("ALTER SEQUENCE usuario_id_usuario_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE conta_id_conta_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE categoria_id_categoria_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE transacao_id_transacao_seq RESTART WITH 1;")
    conn.commit()
    print("✓ Dados limpos")
except Exception as e:
    print(f"ERRO ao limpar: {e}")
    conn.rollback()
    exit(1)

print("\nPasso 6: Hash de senhas...")
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

senha1 = hash_password("senha123")
senha2 = hash_password("senha456")
senha3 = hash_password("senha789")
print("✓ Senhas hasheadas")

print("\nPasso 7: Inserindo usuários...")
try:
    cursor.execute("""
        INSERT INTO usuario (nome, email, senha) VALUES
        ('João Silva', 'joao@email.com', %s),
        ('Maria Santos', 'maria@email.com', %s),
        ('Pedro Oliveira', 'pedro@email.com', %s)
        RETURNING id_usuario;
    """, (senha1, senha2, senha3))
    
    ids_usuarios = [row[0] for row in cursor.fetchall()]
    conn.commit()
    print(f"✓ 3 usuários criados: {ids_usuarios}")
except Exception as e:
    print(f"ERRO ao inserir usuários: {e}")
    conn.rollback()
    exit(1)

print("\nPasso 8: Inserindo contas...")
try:
    cursor.execute("""
        INSERT INTO conta (nome, saldo, tipo, id_usuario) VALUES
        ('Conta Corrente', 5000.00, 'corrente', %s),
        ('Poupança', 15000.00, 'poupanca', %s),
        ('Investimentos', 30000.00, 'investimento', %s),
        ('Conta Corrente', 8500.00, 'corrente', %s),
        ('Conta Salário', 4200.00, 'salario', %s),
        ('Conta Corrente', 3200.00, 'corrente', %s),
        ('Carteira Digital', 850.00, 'digital', %s)
        RETURNING id_conta;
    """, (ids_usuarios[0], ids_usuarios[0], ids_usuarios[0], 
          ids_usuarios[1], ids_usuarios[1], 
          ids_usuarios[2], ids_usuarios[2]))
    
    ids_contas = [row[0] for row in cursor.fetchall()]
    conn.commit()
    print(f"✓ 7 contas criadas")
except Exception as e:
    print(f"ERRO ao inserir contas: {e}")
    conn.rollback()
    exit(1)

print("\nPasso 9: Inserindo categorias...")
try:
    cursor.execute("""
        INSERT INTO categoria (nome, tipo, id_usuario) VALUES
        ('Salário', 'receita', %s),
        ('Freelance', 'receita', %s),
        ('Alimentação', 'despesa', %s),
        ('Transporte', 'despesa', %s),
        ('Lazer', 'despesa', %s),
        ('Salário', 'receita', %s),
        ('Investimentos', 'receita', %s),
        ('Moradia', 'despesa', %s),
        ('Saúde', 'despesa', %s),
        ('Salário', 'receita', %s),
        ('Educação', 'despesa', %s),
        ('Contas', 'despesa', %s)
        RETURNING id_categoria;
    """, (ids_usuarios[0], ids_usuarios[0], ids_usuarios[0], ids_usuarios[0], ids_usuarios[0],
          ids_usuarios[1], ids_usuarios[1], ids_usuarios[1], ids_usuarios[1],
          ids_usuarios[2], ids_usuarios[2], ids_usuarios[2]))
    
    ids_categorias = [row[0] for row in cursor.fetchall()]
    conn.commit()
    print(f"✓ 12 categorias criadas")
except Exception as e:
    print(f"ERRO ao inserir categorias: {e}")
    conn.rollback()
    exit(1)

print("\nPasso 10: Inserindo transações...")
try:
    hoje = date.today()
    
    cursor.execute("""
        INSERT INTO transacao (valor, data, descricao, tipo, id_usuario, id_conta, id_categoria) VALUES
        (6500.00, %s, 'Salário mensal', 'receita', %s, %s, %s),
        (1200.00, %s, 'Projeto freelance', 'receita', %s, %s, %s),
        (450.00, %s, 'Supermercado', 'despesa', %s, %s, %s),
        (120.00, %s, 'Uber', 'despesa', %s, %s, %s),
        (200.00, %s, 'Cinema e jantar', 'despesa', %s, %s, %s),
        (8500.00, %s, 'Salário mensal', 'receita', %s, %s, %s),
        (350.00, %s, 'Rendimento investimentos', 'receita', %s, %s, %s),
        (1800.00, %s, 'Aluguel', 'despesa', %s, %s, %s),
        (250.00, %s, 'Consulta médica', 'despesa', %s, %s, %s),
        (4200.00, %s, 'Salário mensal', 'receita', %s, %s, %s),
        (850.00, %s, 'Curso online', 'despesa', %s, %s, %s),
        (320.00, %s, 'Conta de luz e internet', 'despesa', %s, %s, %s);
    """, (
        # João
        hoje - timedelta(days=5), ids_usuarios[0], ids_contas[0], ids_categorias[0],
        hoje - timedelta(days=3), ids_usuarios[0], ids_contas[0], ids_categorias[1],
        hoje - timedelta(days=2), ids_usuarios[0], ids_contas[0], ids_categorias[2],
        hoje - timedelta(days=1), ids_usuarios[0], ids_contas[0], ids_categorias[3],
        hoje, ids_usuarios[0], ids_contas[0], ids_categorias[4],
        # Maria
        hoje - timedelta(days=4), ids_usuarios[1], ids_contas[3], ids_categorias[5],
        hoje - timedelta(days=2), ids_usuarios[1], ids_contas[3], ids_categorias[6],
        hoje - timedelta(days=1), ids_usuarios[1], ids_contas[3], ids_categorias[7],
        hoje, ids_usuarios[1], ids_contas[3], ids_categorias[8],
        # Pedro
        hoje - timedelta(days=6), ids_usuarios[2], ids_contas[5], ids_categorias[9],
        hoje - timedelta(days=3), ids_usuarios[2], ids_contas[5], ids_categorias[10],
        hoje - timedelta(days=1), ids_usuarios[2], ids_contas[5], ids_categorias[11],
    ))
    
    conn.commit()
    print(f"✓ 12 transações criadas")
except Exception as e:
    print(f"ERRO ao inserir transações: {e}")
    conn.rollback()
    exit(1)

print("\n" + "="*60)
print("✅ SEED CONCLUÍDO COM SUCESSO!")
print("="*60)

# Verificar
cursor.execute("SELECT COUNT(*) FROM usuario;")
print(f"\nUsuários: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM conta;")
print(f"Contas: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM categoria;")
print(f"Categorias: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM transacao;")
print(f"Transações: {cursor.fetchone()[0]}")

print("\n📧 Credenciais:")
print("  • joao@email.com / senha123")
print("  • maria@email.com / senha456")
print("  • pedro@email.com / senha789")

cursor.close()
conn.close()
print("\n✓ Conexão fechada")