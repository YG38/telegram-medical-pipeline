# Shipping a Data Product: From Raw Telegram Data to an Analytical API
**Final Project Report – Kara Solutions · July 2025**  
Repository: <https://github.com/YG38/telegram-medical-pipeline>

---

## 1. Executive Summary
We built an end-to-end ELT pipeline that scrapes public Telegram channels on Ethiopian medical topics, lands raw data in a data lake + PostgreSQL warehouse, transforms it with **dbt**, enriches images with **YOLOv8**, and serves insights via a **FastAPI** analytical API. **Dagster** orchestrates the daily pipeline. The platform answers questions on top-mentioned products, channel activity, and media trends while remaining reproducible, testable, and secure.

---

## 2. High-Level Architecture
```text
┌────────────────────────────┐
│  Dagster Job (daily)       │
│  └── scrape_op             │
│  └── load_op               │
│  └── dbt_run_op            │
│  └── yolo_enrich_op        │
└──────────────┬─────────────┘
               │
      docker-compose stack
               │
┌────────────────────────────┐   writes          reads
│   Python Container         │──────────────┐  ┌────────┐
│   (scripts + FastAPI)      │              │  │  dbt   │
└────────────────────────────┘              ▼  ▼
                                         ┌───────────────┐
                                         │ PostgreSQL 15 │
                                         │ raw / staging │
                                         │  / mart       │
                                         └─┬─────────────┘
                                           │
           JSONL + images                  │
┌────────────────────────────┐             │
│   Data Lake (local FS)     │◀────────────┘
└────────────────────────────┘
```

---

## 3. Star-Schema Data Model
```text
                    ┌────────────┐
                    │ dim_dates  │
                    └──┬─────┬───┘
                       │ FK  │
┌────────────┐         │     │         ┌──────────────┐
│dim_channels│─────────┘     └────────>│fct_messages  │
└────────────┘                         │• message_id PK│
                                       │• message_len  │
                                       │• has_media    │
                                       └──┬──────┬─────┘
                                          │      │
                        ┌──────────────────┘      └──────┐
                        ▼                               ▼
                 ┌────────────────┐             ┌──────────────┐
                 │fct_image_detections│         │(future marts)│
                 └──────────────────┘             └──────────────┘
```

---

## 4. Task Breakdown
| Task | Deliverables | Key Tech |
|------|--------------|----------|
| **0** – Environment | Dockerfile, docker-compose, .env, Makefile | Docker, python-dotenv |
| **1** – Extract & Load | `scrape_telegram.py`, JSONL data lake, `load_raw_to_postgres.py` | Telethon, psycopg2 |
| **2** – Transform | `telegram_medical_dbt` project, staging + marts, tests, docs | dbt-postgres |
| **3** – Enrichment | `yolo_enrich.py`, table `raw.image_detections`, mart `fct_image_detections` | ultralytics YOLOv8 |
| **4** – API | FastAPI app (`api/`), endpoints for top products, channel activity, search | FastAPI, Pydantic |
| **5** – Orchestration | Dagster job `telegram_medical_job` & schedule | Dagster |

---

## 5. Data Quality & Testing
* **dbt tests** (`unique`, `not_null`) on all PK/FK columns + custom freshness test.
* Loader idempotent via `ON CONFLICT DO NOTHING`.
* YOLO detections deduplicated on `(image_path, object_class, confidence)` PK.

---

## 6. API Usage Examples
* Top products: `GET /api/reports/top-products?limit=5`
* Channel activity: `GET /api/channels/123456789/activity`
* Keyword search: `GET /api/search/messages?query=paracetamol`
* Interactive docs: `http://localhost:8000/docs`

---

## 7. Challenges & Lessons Learned
| Challenge | Lesson |
|-----------|--------|
| Telegram rate limits | Implemented back-off (FloodWait handling). |
| Mixed unstructured + structured data | Early schema design prevented re-work. |
| Windows CRLF warnings | Acceptable via Git autocrlf; no pipeline impact. |
| Model size in container | Chose `yolov8n` for size/performance balance. |

---

## 8. Future Enhancements
1. Cloud deployment (ECS + RDS) with CI/CD.
2. Incremental dbt models & partition pruning.
3. Redis cache for heavy API queries.
4. Sentiment analysis on messages.
5. Grafana dashboards for Dagster assets.

---

## 9. Screenshots to Include in PDF
1. docker-compose services running.
2. Dagster graph & successful run.
3. FastAPI Swagger UI responses.
4. dbt docs lineage graph.
5. GitHub repository tree.

---

## 10. References
* Telegram API – <https://core.telegram.org/api>
* dbt – <https://docs.getdbt.com/>
* YOLOv8 – <https://docs.ultralytics.com/models/yolov8/>
* Dagster – <https://docs.dagster.io/>

---

### Reflection
Containerisation and modular open-source tooling (Telethon, dbt, YOLOv8, FastAPI, Dagster) enabled rapid delivery of a reliable analytics pipeline. Early adoption of a star schema and automated tests built data trust from day one. Future work will focus on production hardening and richer ML enrichments.

---

**Prepared by:** Mahlet · Rediet · Kerod · Rehmet (Kara Solutions) – July 2025
