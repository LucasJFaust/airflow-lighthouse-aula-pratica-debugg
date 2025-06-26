from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import os

# Caminho onde o sensor espera o arquivo de notificação
FILE_NOTIFICATION_PATH = '/tmp/data_notification_file.txt'

def _generate_data_but_fail_to_create_notification_file():
    """
    Simula a geração de dados, mas INTENCIONALMENTE NÃO cria o arquivo de notificação
    que o sensor subsequente espera.
    """
    print("Gerando dados para processamento...")
    # Em um cenário real, esta tarefa criaria o 'FILE_NOTIFICATION_PATH' após gerar os dados.
    # Mas aqui, estamos simulando uma falha (ou erro de lógica) que impede a criação do arquivo.
    # Isso fará com que o 'wait_for_notification_sensor' fique travado até o timeout.

    # --- PROBLEMA INTENCIONAL: FALHA SILENCIOSA OU ERRO DE LÓGICA (Slide 13 - Categoria 2) ---
    # Não vamos criar o arquivo!
    # Solução: Descomentar as linhas abaixo. (OBS: Necessário dar o `astro dev restart` para aplicar as mudanças)
    # os.makedirs('/tmp', exist_ok=True)
    # with open(FILE_NOTIFICATION_PATH, 'w') as f:
    #     f.write("Dados prontos para o próximo passo!")
    # print(f"Arquivo de notificação '{FILE_NOTIFICATION_PATH}' criado com sucesso.")

    print(f"ATENÇÃO: O arquivo de notificação '{FILE_NOTIFICATION_PATH}' NÃO será criado por esta tarefa.")
    print("Isso fará com que o sensor subsequente fique esperando.")

    # Pode-se adicionar uma linha para simular um erro real que impede a criação do arquivo,
    # por exemplo: raise ValueError("Simulando erro que impediu criação do arquivo!")
    # Mas para o propósito do sensor travado, apenas não criar o arquivo é suficiente.
    pass

def _process_notified_data():
    """
    Simula o processamento dos dados após a notificação ser recebida.
    """
    print("Sensor ativado! Processando os dados notificados...")
    try:
        if os.path.exists(FILE_NOTIFICATION_PATH):
            with open(FILE_NOTIFICATION_PATH, 'r') as f:
                content = f.read()
            print(f"Conteúdo do arquivo de notificação: {content}")
            os.remove(FILE_NOTIFICATION_PATH) # Limpa o arquivo após o uso
            print("Arquivo de notificação removido. Processamento concluído com sucesso.")
        else:
            # Isso não deveria acontecer se o sensor passou, mas é uma boa prática defensiva.
            print("Erro: Arquivo de notificação não encontrado após o sensor ativar.")
            raise FileNotFoundError("O arquivo de notificação não existe, o fluxo está inconsistente.")
    except Exception as e:
        print(f"Erro ao processar dados notificados: {e}")
        raise

with DAG(
    dag_id='problem_stuck_sensor_dag',
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=['problema', 'sensor', 'dependencia', 'debugging'],
) as dag:

    generate_data = PythonOperator(
        task_id='generate_data_but_fail_to_create_notification_file',
        python_callable=_generate_data_but_fail_to_create_notification_file,
    )

    # --- PROBLEMA INTENCIONAL: SENSOR TRAVADO (Slide 13 - Categoria 3: Conexão Externa/Dependência) ---
    # Este sensor ficará esperando pelo arquivo que a tarefa anterior não cria.
    # Ele atingirá o timeout se o arquivo não aparecer.
    # Solução: Corrigir a tarefa anterior para que crie o arquivo.
    wait_for_notification_sensor = FileSensor(
        task_id='wait_for_data_notification',
        filepath=FILE_NOTIFICATION_PATH,
        fs_conn_id='fs_default',  # Conexão padrão do Airflow para filesystem.
                                  # Necessário garantir que esta conexão exista ou seja criada (default existe).
        poke_interval=5,          # Verifica a cada 5 segundos
        timeout=60,               # O sensor vai falhar após 60 segundos se o arquivo não aparecer
        mode='poke',              # Modo de verificação (polling)
    )

    process_notified_data_task = PythonOperator(
        task_id='process_notified_data',
        python_callable=_process_notified_data,
    )

    generate_data >> wait_for_notification_sensor >> process_notified_data_task