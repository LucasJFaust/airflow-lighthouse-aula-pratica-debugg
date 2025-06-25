from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import os

def _fetch_initial_data():
    """
    Simula a obtenção de dados iniciais.
    Salva o conteúdo de 'data/initial_data.txt' em '/tmp/raw_data.txt'.
    """
    print("Iniciando a busca de dados iniciais...")
    try:
        # Acessa o diretório pai para encontrar a pasta 'data'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '..')
        data_file_path = os.path.join(project_root, 'data', 'initial_data.txt')

        # Garante que o diretório /tmp existe no ambiente Airflow
        os.makedirs('/tmp', exist_ok=True)

        with open(data_file_path, 'r') as f:
            data = f.read()

        with open('/tmp/raw_data.txt', 'w') as f:
            f.write(data)
        print("Dados iniciais salvos em /tmp/raw_data.txt com sucesso.")
    except Exception as e:
        print(f"Erro ao obter dados iniciais: {e}")
        raise

def _process_data_with_config_and_logic_error():
    """
    Simula o processamento de dados que depende de uma variável de configuração
    e contém um erro de lógica intencional.
    """
    print("Iniciando o processamento de dados com configuração e lógica...")

    # --- PROBLEMA 1: VARIÁVEL DE CONFIGURAÇÃO AUSENTE (Slide 13 - Categoria 5: Permissões/Variáveis) ---
    # Tenta obter uma configuração que os alunos precisarão definir nas Airflow Variables.
    # Se não definida, a tarefa falhará.
    try:
        # A variável 'processing_chunk_size' NÃO estará definida por padrão.
        # Isso causará uma exceção 'KeyError' ao tentar acessá-la.
        # Guia para a solução: Definir 'processing_chunk_size' como '10' em Admin -> Variables na UI do Airflow.
        chunk_size = int(Variable.get("processing_chunk_size"))
        print(f"Tamanho do chunk para processamento: {chunk_size}")
    except KeyError:
        print("\n--- ERRO INTENCIONAL ---")
        print("Erro: A variável 'processing_chunk_size' não foi definida no Airflow Variables.")
        print("Por favor, defina-a para permitir que a tarefa continue.")
        print("Exemplo: Vá em Admin -> Variables na UI do Airflow e adicione 'processing_chunk_size' com valor '10'.")
        raise ValueError("Variável de configuração ausente. Falha no processamento.")
    except ValueError as e:
        print(f"\n--- ERRO INTENCIONAL ---")
        print(f"Erro: Valor inválido para 'processing_chunk_size'. Deve ser um número inteiro. Detalhes: {e}")
        raise

    # --- PROBLEMA 2: ERRO DE LÓGICA NO CÓDIGO (Slide 13 - Categoria 2: Lógica da Task) ---
    # Este erro só ocorrerá se o arquivo 'raw_data.txt' estiver vazio,
    # simulando um caso de borda não tratado.
    try:
        with open('/tmp/raw_data.txt', 'r') as f:
            raw_data = f.read()

        processed_lines = []
        lines = raw_data.splitlines()
        
        # Este é o ponto onde o IndexError pode ocorrer se 'lines' estiver vazio
        # Para que o erro ocorra, o initial_data.txt teria que estar vazio,
        # ou a tarefa _fetch_initial_data teria que falhar em popular o raw_data.txt
        # Deixamos o Index Error para demonstrar a depuração de "lógica da task"
        if not lines:
            print("\n--- AVISO INTENCIONAL (PARA ERRO DE LÓGICA) ---")
            print("O arquivo de dados brutos está vazio. Isso causará um IndexError se não for tratado.")
            # Intencionalmente não tratando aqui para forçar o IndexError
            raise IndexError("Dados brutos vazios, não há o que processar na primeira linha.") # Força o erro para demonstração
        
        first_line = lines[0] # Se 'lines' estiver vazio, isso gera um IndexError
        processed_lines.append(first_line.upper()) # Exemplo de processamento

        with open('/tmp/processed_data.txt', 'w') as f:
            for line in processed_lines:
                f.write(line + '\n')
        print("Dados processados salvos em /tmp/processed_data.txt.")

    except IndexError:
        print("\n--- ERRO INTENCIONAL ---")
        print("Erro de lógica: Tentativa de acessar um índice inválido em uma lista vazia de dados.")
        print("Isso geralmente ocorre quando os dados de entrada não correspondem ao formato esperado.")
        raise ValueError("Erro de lógica no processamento de dados.")
    except Exception as e:
        print(f"Erro inesperado durante o processamento: {e}")
        raise

def _load_processed_data_to_destination():
    """
    Simula o carregamento dos dados processados para um destino final.
    """
    print("Iniciando o carregamento dos dados processados...")
    try:
        with open('/tmp/processed_data.txt', 'r') as f:
            final_data = f.read()
        print(f"Dados finais carregados (primeiros 50 chars): {final_data[:50]}...")
        print("Dados carregados com sucesso!")
    except FileNotFoundError:
        print("\n--- ERRO INTENCIONAL ---")
        print("Erro: Arquivo de dados processados '/tmp/processed_data.txt' não encontrado.")
        print("Isso pode indicar que a tarefa anterior falhou em gerar o arquivo.")
        raise
    except Exception as e:
        print(f"Erro ao carregar dados processados: {e}")
        raise

with DAG(
    dag_id='problem_config_and_logic_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['problema', 'configuracao', 'logica', 'debugging'],
) as dag:
    fetch_data = PythonOperator(
        task_id='fetch_initial_data',
        python_callable=_fetch_initial_data,
    )

    process_data = PythonOperator(
        task_id='process_data_with_config_and_logic_error',
        python_callable=_process_data_with_config_and_logic_error,
    )

    load_data = PythonOperator(
        task_id='load_processed_data_to_destination',
        python_callable=_load_processed_data_to_destination,
    )

    fetch_data >> process_data >> load_data
