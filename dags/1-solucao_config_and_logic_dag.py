# Importa as classes necessárias do Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable # Para interagir com as variáveis do Airflow
from datetime import datetime, timedelta # Para definir datas e intervalos de tempo
import os # Para operações de sistema de arquivos

# --- Definição das funções Python que serão executadas pelas tarefas ---

def _fetch_initial_data():
    """
    Simula a obtenção de dados iniciais.
    Salva o conteúdo de 'data/initial_data.txt' em '/tmp/raw_data.txt'.
    Esta é uma tarefa de preparação, sem problema intencional aqui.
    """
    print("Iniciando a busca de dados iniciais...")
    try:
        # Obtém o diretório atual do arquivo da DAG
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Sobe um nível para chegar à raiz do projeto (onde está a pasta 'data')
        project_root = os.path.join(current_dir, '..')
        # Constrói o caminho completo para o arquivo initial_data.txt
        data_file_path = os.path.join(project_root, 'data', 'initial_data.txt')

        # Garante que o diretório /tmp existe no ambiente do container Airflow
        # Isso é importante porque /tmp pode ser volátil ou não existir por padrão em alguns setups.
        os.makedirs('/tmp', exist_ok=True)

        # Abre o arquivo original (initial_data.txt) para leitura
        with open(data_file_path, 'r') as f:
            data = f.read() # Lê todo o conteúdo do arquivo

        # Escreve o conteúdo lido em um novo arquivo temporário
        with open('/tmp/raw_data.txt', 'w') as f:
            f.write(data) # Salva os "dados brutos" no diretório temporário
        print("Dados iniciais salvos em /tmp/raw_data.txt com sucesso.")
    except Exception as e:
        # Captura qualquer exceção durante a leitura/escrita e a imprime
        print(f"Erro ao obter dados iniciais: {e}")
        raise # Re-lança a exceção para que a tarefa falhe no Airflow

def _process_data_with_config_and_logic_error():
    """
    Simula o processamento de dados que depende de uma variável de configuração
    e contém um erro de lógica intencional para fins de demonstração.
    """
    print("Iniciando o processamento de dados com configuração e lógica...")

    # --- PROBLEMA 1: VARIÁVEL DE CONFIGURAÇÃO AUSENTE (Slide 13 - Categoria 5: Permissões/Variáveis) ---
    # Tenta obter uma configuração que os alunos precisarão definir nas Airflow Variables.
    # Se a variável 'processing_chunk_size' NÃO estiver definida, Variable.get() levantará um KeyError.
    # O objetivo é que os alunos vejam a tarefa falhar e aprendam a depurar 'KeyError' em logs.
    try:
        # Variable.get() busca uma variável no banco de dados do Airflow.
        # Por padrão, 'processing_chunk_size' não existirá, causando um KeyError.
        # A solução será criar essa variável na UI do Airflow (Admin -> Variables).
        chunk_size = int(Variable.get("processing_chunk_size"))
        print(f"Tamanho do chunk para processamento: {chunk_size}")
    except KeyError:
        print("\n--- ERRO INTENCIONAL ---")
        print("Erro: A variável 'processing_chunk_size' não foi definida no Airflow Variables.")
        print("Por favor, defina-a para permitir que a tarefa continue.")
        print("Exemplo: Vá em Admin -> Variables na UI do Airflow e adicione 'processing_chunk_size' com valor '10'.")
        # Levanta um ValueError para garantir que a tarefa falhe com uma mensagem clara.
        raise ValueError("Variável de configuração ausente. Falha no processamento.")
    except ValueError as e:
        # Captura erro se o valor da variável não puder ser convertido para int.
        print(f"\n--- ERRO INTENCIONAL ---")
        print(f"Erro: Valor inválido para 'processing_chunk_size'. Deve ser um número inteiro. Detalhes: {e}")
        raise # Re-lança a exceção

    # --- PROBLEMA 2: ERRO DE LÓGICA NO CÓDIGO (Slide 13 - Categoria 2: Lógica da Task) ---
    # Este erro (IndexError) só ocorreria se o arquivo 'raw_data.txt' estivesse vazio.
    # Agora, a lógica é corrigida para lidar com essa situação.
    try:
        # Tenta ler os dados brutos gerados pela tarefa anterior.
        with open('/tmp/raw_data.txt', 'r') as f:
            raw_data = f.read()

        processed_lines = [] # Lista para armazenar as linhas processadas
        lines = raw_data.splitlines() # Divide o conteúdo em uma lista de linhas

        # --- CORREÇÃO PARA O ERRO DE LÓGICA INTENCIONAL ---
        # Se 'lines' estiver vazio, em vez de gerar um IndexError, a tarefa agora
        # reconhece que não há dados para processar e prossegue sem falhar.
        if not lines:
            print("\n--- CORREÇÃO APLICADA: Dados brutos vazios. Nada para processar nesta etapa. ---")
            # Garante que o arquivo de saída seja criado (mesmo que vazio),
            # para que a tarefa seguinte (_load_processed_data_to_destination) não falhe por FileNotFoundError.
            os.makedirs('/tmp', exist_ok=True) # Garante que o diretório /tmp existe
            with open('/tmp/processed_data.txt', 'w') as f:
                f.write("") # Escreve um arquivo vazio
            print("Arquivo processed_data.txt criado (vazio, pois não havia linhas para processar).")
            return # A tarefa finaliza com sucesso aqui, sem dados para processar.

        # Se houver linhas, o processamento normal continua.
        first_line = lines[0] # Esta linha NÃO gerará IndexError se 'lines' não estiver vazio
        processed_lines.append(first_line.upper()) # Exemplo de processamento: converte a primeira linha para maiúsculas

        # Salva os dados processados em um novo arquivo temporário.
        with open('/tmp/processed_data.txt', 'w') as f:
            for line in processed_lines:
                f.write(line + '\n')
        print("Dados processados salvos em /tmp/processed_data.txt.")

    except Exception as e:
        # Captura qualquer outra exceção inesperada durante o processamento.
        print(f"Erro inesperado durante o processamento: {e}")
        raise # Re-lança a exceção

    # --- PROBLEMA 2: ERRO DE LÓGICA NO CÓDIGO (Slide 13 - Categoria 2: Lógica da Task) ---
    # Este erro (IndexError) só ocorrerá se o arquivo 'raw_data.txt' estiver vazio,
    # simulando um caso de borda não tratado em um cenário real.
    try:
        # Tenta ler os dados brutos gerados pela tarefa anterior.
        with open('/tmp/raw_data.txt', 'r') as f:
            raw_data = f.read()

        processed_lines = [] # Lista para armazenar as linhas processadas
        lines = raw_data.splitlines() # Divide o conteúdo em uma lista de linhas

        # Ponto de falha intencional: Se 'lines' estiver vazio, acessar 'lines[0]'
        # resultará em um IndexError. Este é o erro de lógica a ser depurado.
        # Atualmente, 'initial_data.txt' não está vazio, então este erro só ocorrerá
        # se 'initial_data.txt' for esvaziado ou a tarefa anterior falhar.
        # No entanto, a mensagem de erro customizada abaixo será disparada para demonstração.
        if not lines:
            print("\n--- AVISO INTENCIONAL (PARA ERRO DE LÓGICA) ---")
            print("O arquivo de dados brutos está vazio. Isso causará um IndexError se não for tratado.")
            # Intencionalmente levantamos o IndexError para que os alunos vejam este tipo de falha.
            raise IndexError("Dados brutos vazios, não há o que processar na primeira linha.")

        first_line = lines[0] # Esta linha pode gerar IndexError se 'lines' estiver vazio
        processed_lines.append(first_line.upper()) # Exemplo de processamento: converte a primeira linha para maiúsculas

        # Salva os dados processados em um novo arquivo temporário.
        with open('/tmp/processed_data.txt', 'w') as f:
            for line in processed_lines:
                f.write(line + '\n')
        print("Dados processados salvos em /tmp/processed_data.txt.")

    except IndexError:
        # Captura o IndexError e fornece uma mensagem mais explicativa.
        print("\n--- ERRO INTENCIONAL ---")
        print("Erro de lógica: Tentativa de acessar um índice inválido em uma lista vazia de dados.")
        print("Isso geralmente ocorre quando os dados de entrada não correspondem ao formato esperado.")
        raise ValueError("Erro de lógica no processamento de dados.") # Re-lança como ValueError para consistência
    except Exception as e:
        # Captura qualquer outra exceção inesperada durante o processamento.
        print(f"Erro inesperado durante o processamento: {e}")
        raise # Re-lança a exceção

def _load_processed_data_to_destination():
    """
    Simula o carregamento dos dados processados para um destino final.
    Esta é uma tarefa de conclusão, dependente do sucesso da anterior.
    """
    print("Iniciando o carregamento dos dados processados...")
    try:
        # Tenta ler o arquivo de dados processados.
        with open('/tmp/processed_data.txt', 'r') as f:
            final_data = f.read()
        # Imprime uma parte dos dados lidos para confirmação.
        print(f"Dados finais carregados (primeiros 50 chars): {final_data[:50]}...")
        print("Dados carregados com sucesso!")
    except FileNotFoundError:
        # Captura erro se o arquivo processado não foi criado pela tarefa anterior.
        print("\n--- ERRO INTENCIONAL ---")
        print("Erro: Arquivo de dados processados '/tmp/processed_data.txt' não encontrado.")
        print("Isso pode indicar que a tarefa anterior falhou em gerar o arquivo.")
        raise # Re-lança a exceção
    except Exception as e:
        # Captura qualquer outra exceção inesperada.
        print(f"Erro ao carregar dados processados: {e}")
        raise

# --- Definição do DAG ---
with DAG(
    dag_id='solucao_config_and_logic_dag', # ID único do DAG
    start_date=datetime(2023, 1, 1), # Data de início do DAG (historicamente)
    # ATENÇÃO: 'schedule_interval' foi substituído por 'schedule' no Airflow 2.x
    schedule=None, # Define o agendamento: None significa que só roda manualmente ou por trigger
    catchup=False, # Impede que o DAG execute para períodos passados desde o start_date
    tags=['problema', 'configuracao', 'logica', 'debugging'], # Tags para organização na UI do Airflow
) as dag:
    # --- Definição das Tarefas ---
    # PythonOperator é usado para executar funções Python.

    fetch_data = PythonOperator(
        task_id='fetch_initial_data', # ID único da tarefa
        python_callable=_fetch_initial_data, # Função Python a ser executada
    )

    process_data = PythonOperator(
        task_id='process_data_with_config_and_logic_error',
        python_callable=_process_data_with_config_and_logic_error,
    )

    load_data = PythonOperator(
        task_id='load_processed_data_to_destination',
        python_callable=_load_processed_data_to_destination,
    )

    # --- Definição do Fluxo (Orquestração) ---
    # O operador '>>' define a dependência: a tarefa à esquerda deve completar
    # com sucesso para que a tarefa à direita comece.
    fetch_data >> process_data >> load_data # fetch_data -> process_data -> load_data
