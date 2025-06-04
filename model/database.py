import sqlite3
from sqlite3 import Error, OperationalError

DATABASE_NAME = "database.db"

def connect_db():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except OperationalError as oe: # Erro ao tentar abrir/conectar o arquivo do BD
        print(f"Erro operacional ao conectar ao banco de dados: {oe}")
    except Error as e: # Outros erros genéricos do sqlite3
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conn

def create_table(conn, create_table_sql):
    """Executa uma instrução SQL para criar uma tabela."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except OperationalError as oe: 
        print(f"Erro operacional ao criar tabela: {oe}")
    except Error as e:
        print(f"Erro ao criar tabela: {e}")

def setup_database():
    """Configura o banco de dados inicial, criando as tabelas se não existirem."""
    sql_create_agendamentos_table = """
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        email TEXT,
        data TEXT NOT NULL,
        valor_servico REAL,
        servico TEXT NOT NULL
    );
    """

    sql_create_usuarios_table = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL
    );
    """

    conn = connect_db()

    if conn is not None:
        try:
            print("Criando/Verificando tabelas...")
            create_table(conn, sql_create_agendamentos_table)
            create_table(conn, sql_create_usuarios_table)
            conn.commit()
            print("Configuração do banco de dados concluída.")
        except Error as e:
            print(f"Erro durante o setup do banco de dados: {e}")
        finally:
            conn.close()
    else:
        print("Erro! Não foi possível criar uma conexão com o banco de dados para o setup.")