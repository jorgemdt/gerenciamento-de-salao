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

# --- Bloco para Teste ---
if __name__ == '__main__':
    # Garante que o DB está configurado (executa o script anterior)
    from .database import setup_database
    setup_database()

    print("\n--- Testando AgendamentoModel ---")
    model = AgendamentoModel()

    # Testa adicionar
    print("\nAdicionando agendamentos...")
    model.add_agendamento("Cliente Teste 1", "11999998888", "teste1@email.com", "2025-06-10 10:00", 50.00, "Corte Feminino")
    model.add_agendamento("Cliente Teste 2", "21988887777", "teste2@email.com", "2025-06-10 11:00", 35.00, "Manicure")

    # Testa buscar todos
    print("\nBuscando todos...")
    agendamentos = model.get_all_agendamentos()
    for ag in agendamentos:
        print(ag)

    # Testa atualizar (assumindo que o primeiro ID é 1)
    if agendamentos:
      print("\nAtualizando agendamento ID 1...")
      model.update_agendamento(agendamentos[0][0], "Cliente Teste 1 Alterado", "11999998888", "teste1_alt@email.com", "2025-06-10 10:30", 55.00, "Corte e Escova")
      print(model.get_agendamento_by_id(agendamentos[0][0]))

    # Testa deletar (assumindo que o segundo ID é 2)
    if len(agendamentos) > 1:
        print("\nDeletando agendamento ID 2...")
        model.delete_agendamento(agendamentos[1][0])

    # Busca todos novamente para verificar
    print("\nBuscando todos novamente...")
    agendamentos = model.get_all_agendamentos()
    for ag in agendamentos:
        print(ag)

    print("\n--- Testando Login ---")
    print(f"Usuário 'neide' existe? {check_user('neide')}")
    print(f"Usuário 'guest' existe? {check_user('guest')}")
    
    print("\n--- Testes concluídos ---")