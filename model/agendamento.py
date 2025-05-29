from sqlite3 import Error
from .database import connect_db

def check_user(username):
    """Verifica se um nome de usuário existe no banco de dados."""
    conn = connect_db()
    if conn is None:
        return False

    sql = "SELECT id FROM usuarios WHERE username = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (username,))
        user_exists = cur.fetchone() is not None
        conn.close()
        return user_exists
    except Error as e:
        print(f"Erro ao verificar usuário: {e}")
        conn.close()
        return False

class AgendamentoModel:
    """
    Classe Model para gerenciar as operações CRUD para agendamentos.
    """

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
            conn.close()
            print("Agendamento adicionado com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao adicionar agendamento: {e}")
            conn.close()
            return False

    def get_all_agendamentos(self):
        """Retorna todos os agendamentos do banco de dados."""
        conn = connect_db()
        if conn is None:
            return []

        sql = "SELECT * FROM agendamentos ORDER BY data"
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            conn.close()
            return rows
        except Error as e:
            print(f"Erro ao buscar agendamentos: {e}")
            conn.close()
            return []

    def get_agendamento_by_id(self, agendamento_id):
        """Retorna um agendamento específico pelo ID."""
        conn = connect_db()
        if conn is None:
            return None

        sql = "SELECT * FROM agendamentos WHERE id = ?"
        try:
            cur = conn.cursor()
            cur.execute(sql, (agendamento_id,))
            row = cur.fetchone()
            conn.close()
            return row
        except Error as e:
            print(f"Erro ao buscar agendamento por ID: {e}")
            conn.close()
            return None

    def update_agendamento(self, agendamento_id, nome, telefone, email, data, valor_servico, servico):
        """Atualiza um agendamento existente."""
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
            conn.close()
            print(f"Agendamento {agendamento_id} atualizado com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao atualizar agendamento: {e}")
            conn.close()
            return False

    def delete_agendamento(self, agendamento_id):
        """Deleta um agendamento pelo ID."""
        conn = connect_db()
        if conn is None:
            return False

        sql = 'DELETE FROM agendamentos WHERE id = ?'
        try:
            cur = conn.cursor()
            cur.execute(sql, (agendamento_id,))
            conn.commit()
            conn.close()
            print(f"Agendamento {agendamento_id} deletado com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao deletar agendamento: {e}")
            conn.close()
            return False
