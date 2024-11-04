# Airflow e DAGs

Criamos um DAG com um pipeline de dados, para que fosse efetivada a extração das informações de clima/tempo automatizada. Assim, toda segunda-feira ele faz a extração dos dados via API (VisualCrossing)e salva em uma pasta nomeada com a primeira segunda-feira da semana. Os dados que extraímos são Condições climáticas, dados brutos e a temperatura, todos em arquivos CSV.