from airflow import DAG  # Importa a classe DAG para definir o fluxo
from airflow.operators.python import PythonOperator  # Import correto para o Airflow 2.x
from datetime import datetime, timedelta  # Para definir datas e intervalos

# Função Python para a tarefa
def hello_world_function():
    print("Hello, Airflow!")  # Mensagem correta sem erros de sintaxe

# Definição do DAG — agora corrigido
with DAG(
    dag_id="solution_dag_parsing_error",  # ID único do DAG
    start_date=datetime(2023, 1, 1),     # Definindo um objeto `datetime` corretamente
    schedule=None,                       # Usando `schedule` (em vez de `schedule_interval`) para agendamento manual
    catchup=False,                       # Evita execuções retroativas pendentes
    tags=["debug", "parsing_error"],     # Tags para organização no Airflow UI
) as dag:

    # Definição da tarefa
    say_hello_task = PythonOperator(
        task_id="say_hello_task",         # ID único para a tarefa
        python_callable=hello_world_function,  # Função a ser executada
        retry_delay=timedelta(minutes=5),  # Corrigido para usar um `timedelta` para atrasos entre tentativas
    )
