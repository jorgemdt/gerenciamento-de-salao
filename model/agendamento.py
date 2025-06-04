import sqlite3 # Adicionado para referenciar os tipos de erro específicos
from .database import connect_db

class AgendamentoModel:
    """Gerencia as operações CRUD para agendamentos no banco de dados."""

    def add_agendamento(self, nome, telefone, email, data, valor_servico, servico):
        """Adiciona um novo agendamento ao banco de dados."""
        conn = connect_db()
        if conn is None:
            return False

        sql = ''' INSERT INTO agendamentos(nome, telefone, email, data, valor_servico, servico)
                  VALUES(?,?,?,?,?,?) '''
        try:
            cur = conn.cursor()
            cur.execute(sql, (nome, telefone, email, data, valor_servico, servico))
            conn.commit()
            return True
        except sqlite3.IntegrityError as ie:
            print(f"Erro de integridade ao adicionar agendamento: {ie}")
            return False
        except sqlite3.OperationalError as oe:
            print(f"Erro operacional ao adicionar agendamento: {oe}")
            return False
        except sqlite3.Error as e:
            print(f"Erro SQLite ao adicionar agendamento: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_all_agendamentos(self):
        """Retorna uma lista de todos os agendamentos, ordenados por data."""
        conn = connect_db()
        if conn is None:
            return []

        sql = "SELECT * FROM agendamentos ORDER BY data"
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows
        except sqlite3.OperationalError as oe:
            print(f"Erro operacional ao buscar agendamentos: {oe}")
            return []
        except sqlite3.Error as e:
            print(f"Erro SQLite ao buscar agendamentos: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_agendamento_by_id(self, agendamento_id):
        """Retorna um agendamento específico pelo seu ID."""
        conn = connect_db()
        if conn is None:
            return None

        sql = "SELECT * FROM agendamentos WHERE id = ?"
        try:
            cur = conn.cursor()
            cur.execute(sql, (agendamento_id,))
            row = cur.fetchone()
            return row
        except sqlite3.OperationalError as oe:
            print(f"Erro operacional ao buscar agendamento por ID: {oe}")
            return None
        except sqlite3.Error as e:
            print(f"Erro SQLite ao buscar agendamento por ID: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def update_agendamento(self, agendamento_id, nome, telefone, email, data, valor_servico, servico):
        """Atualiza um agendamento existente no banco de dados."""
        conn = connect_db()
        if conn is None:
            return False

        sql = ''' UPDATE agendamentos
                  SET nome = ?,
                      telefone = ?,
                      email = ?,
                      data = ?,
                      valor_servico = ?,
                      servico = ?
                  WHERE id = ? '''
        try:
            cur = conn.cursor()
            cur.execute(sql, (nome, telefone, email, data, valor_servico, servico, agendamento_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError as ie:
            print(f"Erro de integridade ao atualizar agendamento: {ie}")
            return False
        except sqlite3.OperationalError as oe:
            print(f"Erro operacional ao atualizar agendamento: {oe}")
            return False
        except sqlite3.Error as e:
            print(f"Erro SQLite ao atualizar agendamento: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def delete_agendamento(self, agendamento_id):
        """Deleta um agendamento do banco de dados pelo seu ID."""
        conn = connect_db()
        if conn is None:
            return False

        sql = 'DELETE FROM agendamentos WHERE id = ?'
        try:
            cur = conn.cursor()
            cur.execute(sql, (agendamento_id,))
            conn.commit()
            return True
        except sqlite3.OperationalError as oe:
            print(f"Erro operacional ao deletar agendamento: {oe}")
            return False
        except sqlite3.Error as e:
            print(f"Erro SQLite ao deletar agendamento: {e}")
            return False
        finally:
            if conn:
                conn.close()