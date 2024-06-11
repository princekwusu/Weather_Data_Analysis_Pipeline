from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

# Define the base path relative to the DAG file
base_path = os.path.join(os.path.dirname(__file__), 'src')

# Path definition using the base path
migration = os.path.join(base_path, 'migration.py')
extraction = os.path.join(base_path, 'extraction.py')

# Default arguments
default_args = {
    'owner': 'DE_GROUP',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 8),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15),
}

# DAG definition
dag = DAG(
    dag_id='WEATHER_DATA_PIPE',
    default_args=default_args,
    description="WEATHER PIPELINE",
    schedule_interval=timedelta(days=5),
    catchup=False,
)

# Task 1: BashOperator with additional debugging
data_migration = BashOperator(
    task_id='migration_of_data',
    bash_command=f'echo "Running migration.py" && ls -l {migration} && python {migration}',
    dag=dag,
)

# Task 2: BashOperator with additional debugging
data_extraction = BashOperator(
    task_id='extraction_of_data',
    bash_command=f'echo "Running extraction.py" && ls -l {extraction} && python {extraction}',
    dag=dag,
)

# Define task dependencies
data_migration >> data_extraction
