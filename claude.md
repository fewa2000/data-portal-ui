# Data Portal – v1 Context

## Goal
Build a minimal, demo-ready Data Portal UI.

## Architecture
Sources
→ Ingestion scripts
→ PostgreSQL (raw / Bronze)
→ dbt (Silver)
→ dbt (Gold)
→ FastAPI
→ Streamlit UI (this repository)

## Rules
- Streamlit UI is read-only
- UI does NOT compute KPIs
- UI does NOT connect to the database
- UI consumes data via an API (mocked for now)
- Business logic is upstream (dbt / backend)

## Scope (v1)
- KPI overview
- Drilldowns
- Filters
- Mock API layer

No agents, no orchestration, no AI logic.
