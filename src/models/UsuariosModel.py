import bcrypt
from .databaseModel import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()
    
    def email_existe(self, email):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = "SELECT id_usuario FROM usuario WHERE email = %s"  # ← cambiado
        cursor.execute(query, (email,))
        existe = cursor.fetchone() is not None
        conn.close()
        return existe
        
    def registrar(self, usuario_data):
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(usuario_data.password.encode('utf-8'), salt)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO usuario (nombre, apellido, email, password)  # ← cambiado
                VALUES (%s, %s, %s, %s)
                """,
                (usuario_data.nombre, usuario_data.apellido, usuario_data.email, hashed_pw.decode('utf-8'))
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()
        
    def validar_login(self, email, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM usuario WHERE email = %s"  # ← cambiado
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user
        return None
    
    def actualizar_ultimo_acceso(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE usuario  # ← cambiado
            SET ultimo_acceso = NOW() 
            WHERE id_usuario = %s
            """,
            (id_usuario,)
        )
        conn.commit()
        conn.close()
        
    def obtener_por_id(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM usuario WHERE id_usuario = %s"  # ← cambiado
        cursor.execute(query, (id_usuario,))
        user = cursor.fetchone()
        conn.close()
        return user