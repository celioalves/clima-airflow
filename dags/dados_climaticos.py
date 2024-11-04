from airflow import DAG
import pendulum
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.macros import ds_add
import os
from os.path import join
import pandas as pd
from dotenv import load_dotenv

with DAG(
    "dados_climaticos",
    start_date=pendulum.datetime(2024, 10, 7, tz="UTC"),
    schedule_interval='0 0 * * 1' # dia, hora, dia do mês, mês, dia da semana - CRON expression
) as dag:

    cria_pasta = BashOperator (
        task_id = "cria_pasta", 
        bash_command= 'mkdir -p "/home/celioalves/Documentos/airflow/semana={{data_interval_end.strftime("%Y-%m-%d")}}"'
    )

    def extrai_dados(data_interval_end):
        
        load_dotenv()

        city = 'Blumenau'
        key = os.getenv('USER_KEY')

        URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
                    f'{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={key}&contentType=csv')

        dados = pd.read_csv(URL)

        file_path = f'/home/celioalves/Documentos/airflow/semana={data_interval_end}/'

        dados.to_csv (file_path + 'dados_brutos.csv')
        dados[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperatura.csv')
        dados[['datetime', 'description', 'icon']].to_csv(file_path + 'condicoes.csv')

    extracao_api = PythonOperator(
        task_id = 'extrai_dados',
        python_callable= extrai_dados, 
        op_kwargs= {'data_interval_end': '{{data_interval_end.strftime("%Y-%m-%d")}}'}
    )

    cria_pasta >> extracao_api