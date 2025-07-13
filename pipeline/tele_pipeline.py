"""Dagster job wiring existing scripts as ops."""
from dagster import job, op
import subprocess


@op
def scrape():
    subprocess.run(["python", "scripts/scrape_telegram.py"], check=True)


@op
def load():
    subprocess.run(["python", "scripts/load_raw_to_postgres.py"], check=True)


@op
def dbt_run():
    subprocess.run(["dbt", "run", "--project-dir", "dbt"], check=True)


@op
def enrich():
    subprocess.run(["python", "scripts/yolo_enrich.py"], check=True)


@job
def telegram_medical_job():
    enrich(dbt_run(load(scrape())))
