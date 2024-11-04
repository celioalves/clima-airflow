from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator as EO
from airflow.operators.bash import BashOperator as BO

with DAG(
    'primeiro_dag',
    start_date=days_ago(2),
    schedule_interval='@daily'
) as dag:
    tarefa_1 = EO(task_id='Tarefa_um')
    tarefa_2 = EO(task_id='Tarefa_dois')
    tarefa_3 = EO(task_id='Tarefa_três')
    tarefa_4 = BO(
        task_id='cria_pasta',
        bash_command= 'mkdir -p "/home/celioalves/Documentos/airflow/pasta={{data_interval_end}}"'
        )
    
    tarefa_1 >> [tarefa_2, tarefa_3]
    tarefa_3 >> tarefa_4