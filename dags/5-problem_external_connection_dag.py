from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook  # Para acessar o banco de dados Postgres
from datetime import datetime

# Função que tenta acessar um banco de dados Postgres
def _fetch_data_from_postgres():
    """
    Função que tenta se conectar a um banco de dados Postgres para buscar dados.
    Um erro ocorrerá se a conexão 'postgres_default' não estiver configurada no Airflow.
    """
    print("Tentando se conectar ao banco de dados Postgres...")

    # Utiliza o Hook do Postgres para gerenciar a conexão
    pg_hook = PostgresHook(postgres_conn_id="postgres_default")

    # Tenta abrir uma conexão e executar uma consulta
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_table LIMIT 10;")  # Consulta de exemplo
    result = cursor.fetchall()

    # Exibe os resultados no log
    print(f"Resultado da consulta: {result}")

# Definição do DAG
with DAG(
    dag_id="problem_external_connection_dag",  # ID único do DAG
    start_date=datetime(2023, 1, 1),         # Data inicial
    schedule=None,                           # Agendamento manual
    catchup=False,                           # Evita execução retroativa
    tags=["external_connection", "problem"], # Tags para organização
) as dag:

    # Tarefa que tenta buscar dados do Postgres
    fetch_data_from_postgres = PythonOperator(
        task_id="fetch_data_from_postgres",      # ID único da tarefa
        python_callable=_fetch_data_from_postgres,  # Função a ser executada
    )
