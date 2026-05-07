import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def get_connection(self):
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),  # ← usa el .env
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            auth_plugin='mysql_native_password'  # ← añade esta línea para evitar el error
        )