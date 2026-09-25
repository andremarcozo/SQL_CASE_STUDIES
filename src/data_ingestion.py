from sql_server_connection import get_connection
import pyodbc


def run_sql_script(conn: pyodbc.Connection, file_path: str) -> None:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            sql_script = file.read()

        cursor = conn.cursor()
        
        comandos_sql = sql_script.split("GO")
        
        for comando in comandos_sql:
            if comando.strip():
                cursor.execute(comando)
                
        print(f"Script '{file_path}' executado com sucesso!")
        
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        raise
    except pyodbc.Error as e:
        print(f"Erro ao executar script SQL: {e}")
        raise


def execute_data_ingestion():
    print("Iniciando a carga de dados no SQL Server...")
    
    conn = get_connection()
    
    try:
        run_sql_script(conn, file_path="../sql_ingestion/case_study_1.sql")
        
        print("Carga de dados concluída com sucesso! 🚀")
        
    except Exception as e:
        print(f"Erro ao ingerir dados: {e}")
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    execute_data_ingestion()