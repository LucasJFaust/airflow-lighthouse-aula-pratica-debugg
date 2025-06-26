from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import time
import random

# --- Funções das tarefas da DAG ---

def _massive_computation_task():
    """
    Tarefa que simula uma computação extremamente pesada.
    Neste exemplo, ela chega a consumir 100% da CPU por vários segundos.
    """
    print("Iniciando tarefa de computação massiva...")
    start_time = time.time()

    # Simula uma carga extremamente pesada (exemplo: cálculo intensivo de Fibonacci)
    result = 0
    for i in range(10**7):  # Um laço extremamente longo
        result += random.randint(1, 100) * random.randint(1, 100)

    print(f"Resultado da computação massiva: {result}")
    print(f"Tarefa concluída em {time.time() - start_time:.2f}s.")

def _large_data_transfer():
    """
    Tarefa que simula transferência de dados extremamente grandes.
    Neste exemplo, cria arquivos para simular carga no sistema de disco e memória.
    """
    print("Iniciando transferência de dados simulada...")

    # Simula geração de arquivos pesados em disco
    num_files = 100
    file_size_mb = 50  # Cada arquivo terá ~50MB
    directory = '/tmp/airflow_large_data_transfer/'

    # Garante que o diretório existe
    import os
    os.makedirs(directory, exist_ok=True)

    # Cria os arquivos para simular transferência de grandes volumes
    for i in range(num_files):
        file_path = os.path.join(directory, f"file_{i}.txt")
        with open(file_path, 'wb') as f:
            f.write(os.urandom(file_size_mb * 1024 * 1024))  # Gera dados aleatórios (~50MB por arquivo)
        print(f"Arquivo gerado: {file_path}")

    print(f"{num_files} arquivos grandes criados em {directory}")

def _long_waiting_task():
    """
    Tarefa que simula uma espera longa (causando bloqueio de recursos).
    """
    print("Iniciando tarefa de espera longa...")
    time.sleep(600)  # Espera por 10 minutos sem fazer nada
    print("Tarefa de espera concluída.")

# --- Definição do DAG ---

with DAG(
    dag_id="problem_resource_intensive_dag",  # ID único do DAG
    start_date=datetime(2023, 1, 1),        # Data inicial
    schedule=None,                          # DAG será executado manualmente
    catchup=False,                          # Não faz backfill de execuções passadas
    tags=["resource_intensive", "debugging"],  # Tags para organização
) as dag:

    # Tarefa 1: Computação intensiva
    massive_computation_task = PythonOperator(
        task_id="massive_computation_task",
        python_callable=_massive_computation_task,
    )

    # Tarefa 2: Transferência de grandes volumes de dados
    large_data_transfer = PythonOperator(
        task_id="large_data_transfer",
        python_callable=_large_data_transfer,
    )

    # Tarefa 3: Espera longa bloqueante
    long_waiting_task = PythonOperator(
        task_id="long_waiting_task",
        python_callable=_long_waiting_task,
    )

    # Definindo a ordem das tarefas
    massive_computation_task >> large_data_transfer >> long_waiting_task