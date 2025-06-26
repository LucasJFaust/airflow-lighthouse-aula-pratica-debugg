from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Função de exemplo que será usada no PythonOperator
def _say_hello():
    print("Hello, Airflow!")

# Definição do DAG
with DAG(
    dag_id="problem_dag_parsing_error",  # ID único do DAG
    start_date=datetime(2023, 1, 1),    # Data inicial
    schedule_interval="0 12 * * *",     # Agendamento cron para executar diariamente ao meio-dia
    catchup=False                       # Impede execuções pendentes (backfill)
) as dag:

    # Tarefa do tipo PythonOperator
    say_hello_task = PythonOperator(
        task_id="say_hello_task",       # ID único da tarefa
        python_callable=_say_hello     # Função Python que será executada
    )