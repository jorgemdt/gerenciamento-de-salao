import sqlite3
import hashlib
import os
from .database import connect_db

class UserModel:
    """Gerencia as operações relacionadas a usuários no banco de dados."""

    def _generate_salt(self):
        """Gera um salt aleatório em hexadecimal."""
        return os.urandom(16).hex()

    def _hash_password(self, password, salt):
        """Gera o hash de uma senha usando SHA256 com um salt."""
        salted_password = salt + password
        hashed = hashlib.sha256(salted_password.encode('utf-8')).hexdigest()
        return hashed

    def create_user(self, username, password):
        """Cria um novo usuário com senha hasheada e salt."""
        conn = connect_db()
        if conn is None:
            return False, "Erro de conexão com o banco."

        salt = self._generate_salt()
        password_hash = self._hash_password(password, salt)
        
        sql = ''' INSERT INTO usuarios(username, password_hash, salt)
                  VALUES(?,?,?) '''
        try:
            cur = conn.cursor()
            cur.execute(sql, (username, password_hash, salt))
            conn.commit()
            return True, "Usuário criado com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Nome de usuário já existe."
        except sqlite3.OperationalError as oe: 
            print(f"Erro operacional ao criar usuário: {oe}")
            return False, f"Erro operacional ao criar usuário: {oe}"
        except sqlite3.Error as e:
            print(f"Erro SQLite ao criar usuário: {e}")
            return False, f"Erro ao criar usuário: {e}"
        finally:
            if conn:
                conn.close()

    def check_credentials(self, username, password_to_check):
        """Verifica as credenciais (username e senha) de um usuário."""
        conn = connect_db()
        if conn is None:
            return False

        sql = "SELECT password_hash, salt FROM usuarios WHERE username = ?"
        try:
            cur = conn.cursor()
            cur.execute(sql, (username,))
            row = cur.fetchone()
            
            if row:
                stored_password_hash, salt = row
                hash_to_check = self._hash_password(password_to_check, salt)
                if hash_to_check == stored_password_hash:
                    return True
            return False
        except sqlite3.OperationalError as oe:
            print(f"Erro operacional ao verificar credenciais: {oe}")
            return False
        except sqlite3.Error as e:
            print(f"Erro SQLite ao verificar credenciais: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def has_users(self):
        """Verifica se existe algum usuário cadastrado no sistema."""
        conn = connect_db()
        if conn is None:
            print("Não foi possível conectar ao DB para verificar usuários.")
            return False 

        sql = "SELECT COUNT(id) FROM usuarios"
        try:
            cur = conn.cursor()
            cur.execute(sql)
            count = cur.fetchone()[0]
            return count > 0
        except sqlite3.OperationalError as oe:
            print(f"Erro operacional ao contar usuários: {oe}")
            return False 
        except sqlite3.Error as e:
            print(f"Erro SQLite ao contar usuários: {e}")
            return False
        finally:
            if conn:
                conn.close()