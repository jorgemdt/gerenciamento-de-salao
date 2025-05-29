# model/database.py

import sqlite3
from sqlite3 import Error

DATABASE_NAME = "database.db"

def connect_db():
    """Cria uma conexão com o banco de dados SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        # print(f"Conexão bem-sucedida com {DATABASE_NAME}")
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conn

def create_table(conn, create_table_sql):
    """Cria uma tabela a partir da instrução SQL fornecida."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(f"Erro ao criar tabela: {e}")

def setup_database():
    """
    Configura o banco de dados: cria a conexão e as tabelas necessárias
    (agendamentos e usuarios) caso elas não existirem.
    """
    
    # SQL para criar a tabela de agendamentos (clientes agendados)
    sql_create_agendamentos_table = """
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        email TEXT,
        data TEXT NOT NULL,          -- Formato sugerido: 'YYYY-MM-DD HH:MM'
        valor_servico REAL,          -- Usar REAL para valores monetários
        servico TEXT NOT NULL
    );
    """

    # SQL para criar a tabela de usuários (para login simples)
    sql_create_usuarios_table = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL
    );
    """

    # SQL para inserir um usuário padrão (se não existir)
    sql_insert_default_user = """
    INSERT OR IGNORE INTO usuarios (username) VALUES ('neide');
    """

    # Cria a conexão com o banco
    conn = connect_db()

    # Cria as tabelas se a conexão foi bem-sucedida
    if conn is not None:
        print("Criando/Verificando tabelas...")
        create_table(conn, sql_create_agendamentos_table)
        create_table(conn, sql_create_usuarios_table)
        
        # Insere o usuário padrão
        try:
            c = conn.cursor()
            c.execute(sql_insert_default_user)
            conn.commit()
            print("Usuário padrão 'admin' garantido.")
        except Error as e:
            print(f"Erro ao inserir usuário padrão: {e}")

        # Fecha a conexão
        conn.close()
        print("Configuração do banco de dados concluída.")
    else:
        print("Erro! Não foi possível criar uma conexão com o banco de dados.")
