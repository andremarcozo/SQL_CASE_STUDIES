from sql_server_connection import get_connection
from export_data import export_query_to_csv


from queries.queries_case_study_1 import query_1, query_2, query_3, query_4, query_5, query_6, query_7, query_8, query_9, query_10

def main():
    conn = get_connection()
    try:
        print("Executando a query e gerando o arquivo CSV...")
        

        export_query_to_csv(conn, query=query_10, file_name="query_10_result.csv")
        
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()