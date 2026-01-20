# Data Portal UI

A minimal, demo-ready Data Portal built with Streamlit.

## Architecture

```
Sources → Ingestion → PostgreSQL (Bronze) → dbt (Silver) → dbt (Gold) → FastAPI → Streamlit UI
```

This repository contains the **Streamlit UI** layer, which is read-only and consumes data via API.

## Features

- KPI Overview with metrics and trend charts
- Drilldown by dimension (region, category, channel)
- Mock API layer (ready for FastAPI integration)

## Setup

```bash
pip install -r requirements.txt
streamlit run Home.py
```

Open http://localhost:8501 in your browser.

## Project Structure

```
├── Home.py                   # Entry point
├── pages/
│   ├── 1_KPI_Overview.py     # KPI metrics and trends
│   └── 2_Drilldown.py        # Dimension drilldowns
└── services/
    └── api.py                # Mock API service layer
```
