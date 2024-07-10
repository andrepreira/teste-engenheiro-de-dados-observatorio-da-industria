.PHONY: setup_airflow init start stop

AIRFLOW_HOME := .
AIRFLOW_CONFIG := $(AIRFLOW_HOME)/config
AIRFLOW_LOGS := $(AIRFLOW_HOME)/logs
AIRFLOW_PLUGINS := $(AIRFLOW_HOME)/plugins

setup_airflow:
	mkdir -p $(AIRFLOW_LOGS) $(AIRFLOW_PLUGINS) $(AIRFLOW_CONFIG)
	echo "AIRFLOW_UID=$$(id -u)" > $(AIRFLOW_HOME)/.env

init: setup_airflow
	docker compose up airflow-init -d

start:
	docker compose up -d

stop:
	docker compose down -d
