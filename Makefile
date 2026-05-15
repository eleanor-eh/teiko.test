.PHONY: setup pipeline dashboard

PYTHON = python3

## Install all dependencies
setup:
	pip install -r requirements.txt

## Run the full pipeline: init DB → load data → generate all tables and plots
pipeline:
	$(PYTHON) init_db.py
	$(PYTHON) load_data.py

## Start the interactive dashboard
dashboard:
	streamlit run dashboard.py
