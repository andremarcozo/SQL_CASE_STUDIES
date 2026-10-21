import pyodbc
import csv
import os

def export_query_to_csv(conn: pyodbc.Connection, query: str, file_name: str) -> None:
    """Executa a query e salva os resultados em um arquivo CSV na pasta results."""
    
    pasta_resultados = "C:\\Users\\AndréMarcozo\\Desktop\\ESTUDOS\\SQL_COURSE\\results\\case_study_2"
    

    os.makedirs(pasta_resultados, exist_ok=True)
    
    caminho_completo = os.path.join(pasta_resultados, file_name)
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        
        # 1. Extrair os nomes das colunas
        colunas = [column[0] for column in cursor.description]
        
        # 2. Extrair os dados (linhas)
        linhas = cursor.fetchall()
        
        # 3. Criar e escrever no arquivo CSV
        # Usamos encoding 'utf-8-sig' para o Excel abrir os acentos corretamente
        with open(caminho_completo, mode="w", newline="", encoding="utf-8-sig") as arquivo_csv:
            escritor = csv.writer(arquivo_csv, delimiter=";") # Ponto e vírgula costuma ser melhor para o Excel no Brasil
            
            # Escreve o cabeçalho
            escritor.writerow(colunas)
            
            # Escreve os dados
            for linha in linhas:
                escritor.writerow(linha)
                
        print(f"✅ Sucesso! {len(linhas)} registros salvos em: {caminho_completo}")
        
    except pyodbc.Error as e:
        print(f"❌ Erro no SQL ao tentar exportar: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado ao gerar CSV: {e}")