from sql_server_connection import get_connection
from export_data import export_query_to_csv


from queries import query_1 

def main():
    conn = get_connection()
    try:
        print("Executando a query e gerando o arquivo CSV...")
        

        export_query_to_csv(conn, query=query_1, file_name="total_spending_on_players_for_each_team.csv")
        
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()