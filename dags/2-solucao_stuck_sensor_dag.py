# Importa as classes necessárias do Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator  # Operador para executar funções Python
from airflow.sensors.python import PythonSensor     # Sensor Python personalizado
from datetime import datetime                      # Para definir datas dentro do DAG
import os                                           # Para operações no sistema de arquivos

# Define o caminho onde o sensor espera o arquivo de notificação
# Esse arquivo será simulado e criado dentro do contêiner no diretório "/tmp/"
FILE_NOTIFICATION_PATH = '/tmp/data_notification_file.txt'

# --- Definição das funções Python que serão executadas como Tasks no DAG ---

def _generate_data_but_fail_to_create_notification_file():
    """
    Função que simula a geração de dados e cria um arquivo de notificação
    no caminho esperado. Essa notificação será usada pelo sensor na próxima etapa.
    """
    print("Gerando dados para processamento...")

    # Garante que o diretório '/tmp/' existe antes de tentar criar o arquivo
    os.makedirs('/tmp', exist_ok=True)

    # Cria o arquivo que o sensor irá monitorar e escreve uma mensagem simulada nele
    with open(FILE_NOTIFICATION_PATH, 'w') as f:
        f.write("Dados prontos para o próximo passo!")
    print(f"Arquivo de notificação '{FILE_NOTIFICATION_PATH}' criado com sucesso.")
    print("Dados gerados e notificação enviada.")

def _wait_for_file():
    """
    Função chamada pelo PythonSensor para verificar se o arquivo
    de notificação foi gerado. Retorna True se o arquivo existir, ou False caso contrário.
    """
    print(f"Verificando a existência do arquivo: {FILE_NOTIFICATION_PATH}")

    # Usa o módulo `os` para verificar se o arquivo existe no caminho especificado
    if os.path.exists(FILE_NOTIFICATION_PATH):
        print("Arquivo encontrado! O processamento pode prosseguir.")
        return True  # Retorna True para indicar sucesso e permitir o avanço no fluxo
    print("Arquivo ainda não disponível.")
    return False  # Retorna False, o que faz o sensor continuar esperando

def _process_notified_data():
    """
    Função que realiza o processamento dos dados após o sensor detectar
    a existência do arquivo de notificação.
    """
    print("Sensor ativado! Processando os dados notificados...")
    try:
        # Verifica novamente (mesmo que redundante) se o arquivo ainda existe
        if os.path.exists(FILE_NOTIFICATION_PATH):
            # Lê o conteúdo do arquivo e exibe no log
            with open(FILE_NOTIFICATION_PATH, 'r') as f:
                content = f.read()
            print(f"Conteúdo do arquivo de notificação: {content}")

            # Remove o arquivo após o processamento
            os.remove(FILE_NOTIFICATION_PATH)
            print("Arquivo de notificação removido. Processamento concluído com sucesso.")
        else:
            # Esta parte não deveria ser alcançada se o sensor funcionou corretamente
            print("Erro: Arquivo de notificação não encontrado após o sensor ativar.")
            raise FileNotFoundError("O arquivo de notificação não existe. O fluxo está inconsistente.")
    except Exception as e:
        # Captura e re-lança qualquer exceção inesperada
        print(f"Erro ao processar os dados notificados: {e}")
        raise

# --- Definição da Estrutura do DAG ---

with DAG(
    dag_id='solucao_stuck_sensor_dag',  # ID único que identifica este DAG
    start_date=datetime(2023, 1, 1),    # Data inicial para programar o início do DAG
    schedule=None,                      # Indica que o DAG será executado manualmente (sem agendamento)
    catchup=False,                      # Impede o Airflow de criar execuções pendentes (backfill)
    tags=['problema', 'sensor', 'dependencia', 'debugging'], # Tags usadas para organização no Airflow UI
) as dag:

    # --- Definição das Tarefas no Fluxo ---

    # 1. Tarefa que simula a geração de dados e cria o arquivo de notificação
    generate_data = PythonOperator(
        task_id='generate_data_but_fail_to_create_notification_file',  # Identificador único da tarefa
        python_callable=_generate_data_but_fail_to_create_notification_file,  # Função que será executada
    )

    # 2. Sensor que espera a criação do arquivo '/tmp/data_notification_file.txt'
    # O sensor usa a função `_wait_for_file` para verificar no sistema de arquivos local
    wait_for_notification_sensor = PythonSensor(
        task_id='wait_for_data_notification',  # Identificador único da tarefa
        python_callable=_wait_for_file,        # Função a ser chamada repetidamente para verificar o arquivo
        poke_interval=5,                       # Intervalo (em segundos) entre as checagens
        timeout=60,                            # Máximo tempo (em segundos) esperando pelo arquivo
        mode='poke',                           # Modo de operação: 'poke' realiza polling ativo
    )

    # 3. Tarefa que processa os dados após o sensor detectar o arquivo de notificação
    process_notified_data_task = PythonOperator(
        task_id='process_notified_data',       # Identificador único da tarefa
        python_callable=_process_notified_data,  # Função que será executada após a notificação
    )

    # Define a ordem das tarefas no Fluxo (Pipeline):
    # 1 -> 2 -> 3 (geração -> sensor -> processamento)
    generate_data >> wait_for_notification_sensor >> process_notified_data_task
