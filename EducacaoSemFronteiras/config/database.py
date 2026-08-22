import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "SUA_SENHA",
    "database": "enem_plus"
}

def conectar():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        raise RuntimeError(f"Erro ao conectar ao MySQL: {e}")
