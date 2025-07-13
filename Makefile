export $(shell sed -E -n 's/^([A-Z_]+)=.*$$/\1/p' .env 2>/dev/null)

.PHONY: scrape dbt_run

scrape:
	python scripts/scrape_telegram.py

dbt_run:
	cd dbt && dbt run
