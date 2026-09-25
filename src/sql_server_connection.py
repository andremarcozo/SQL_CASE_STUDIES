import os
import pyodbc
from dotenv import load_dotenv


load_dotenv()

def get_connection() -> pyodbc.Connection:
    
    
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD") 

    if not password:
        raise ValueError("A senha (DB_PASSWORD) não foi encontrada no arquivo .env!")

    connection_string = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )
    
    try:
        conn = pyodbc.connect(connection_string, autocommit=True)
        print("Conexão estabelecida com sucesso usando .env!")
        return conn
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao SQL Server: {e}")
        raise