SHELL := /bin/bash

.PHONY: up down logs api-shell worker-shell test lint fmt web-install web-dev bench

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

api-shell:
	docker compose exec api bash

worker-shell:
	docker compose exec worker bash

test:
	python -m pytest -q

lint:
	python -m ruff check .

fmt:
	python -m ruff format .

web-install:
	cd web && npm install

web-dev:
	cd web && npm run dev

bench:
	python bench/ingest_bench.py --url http://localhost:8000 --seconds 15 --concurrency 50
