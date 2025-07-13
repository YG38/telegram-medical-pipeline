# Telegram Medical Pipeline

This repository contains an **end-to-end data platform** that extracts Telegram messages about Ethiopian medical products, stores them in a data lake & PostgreSQL warehouse, transforms them with **dbt**, enriches images with **YOLOv8**, and finally exposes insights through a **FastAPI** service.  

> This version fulfils the **Interim Submission** (Tasks 0-2):
> * Professional project scaffolding (Docker, python deps, env management)
> * Working Telegram scraper → `data/raw/…` JSON files  
> * PostgreSQL loading script
> * dbt project with staging + mart models & tests

---

## 1. Quick Start

```bash
# Clone + enter the repo
export PROJECT=telegram-medical-pipeline
git clone git@github.com:<your-user>/$PROJECT.git
cd $PROJECT

# Copy secrets and edit
cp .env.example .env
vi .env  # fill TELEGRAM & DB creds

# Spin-up the whole stack (Postgres + Python app)
docker compose up --build
```
The scraper will download raw data to `data/raw/…`.  To ingest & transform into the warehouse run:
```bash
## Inside the running api container
python scripts/load_raw_to_postgres.py

# dbt
cd dbt
dbt deps
dbt seed
dbt run
```
Generated docs are available with `dbt docs serve`.

---

## 2. Repository layout

```
├── data/                 # <- data lake (raw / interim / processed)
│   └── raw/
├── dbt/                  # <- dbt project (telegram_medical_dbt)
│   ├── dbt_project.yml
│   └── models/
├── scripts/              # <- helper scripts (scraper, loaders)
├── api/                  # <- FastAPI (Task 4 – not required yet)
├── Dockerfile / docker-compose.yml
├── requirements.txt
└── .env.example          # secrets template
```

---

## 3. Environment Variables
Variable | Description
--- | ---
`TELEGRAM_API_ID` | Telegram App ID
`TELEGRAM_API_HASH` | Telegram App Hash
`POSTGRES_USER` | DB user
`POSTGRES_PASSWORD` | DB password
`POSTGRES_DB` | Database name (default `telegram`)

Copy `.env.example` → `.env` and fill in your real secrets (never commit the latter – it’s in `.gitignore`).

---

## 4. Makefile (shortcuts)
```
make scrape   # run scraper locally
make dbt_run  # execute full dbt pipeline
```

---

## 5. Next Steps
* **Task 3**: YOLOv8 enrichment (scripts/yolo_enrich.py, dbt model `fct_image_detections`).
* **Task 4**: FastAPI analytical endpoints.
* **Task 5**: Dagster orchestration (`pipeline/` directory).

---

## Authors
Kara Solutions – Data Engineering Team · 2025
