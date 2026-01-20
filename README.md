# Data Portal UI

A Streamlit-based read-only data portal with domain-driven architecture. This is a demo/v1 implementation focused on UI/UX structure, state modeling, and extensibility.

## Overview

The Data Portal provides analytical dashboards for three business domains:
- **Sales** - Sales order analysis
- **Procurement** - Purchase order analysis
- **Finance** - General ledger analysis

### Key Architectural Principles

1. **Read-Only Portal** - No data mutation, no KPI calculations in the UI
2. **Database as Single Source of Truth** - All filtering via SQL (mocked), UI only collects parameters
3. **Domain-Driven** - Domains define what is possible; tables are not user-selectable
4. **Clear Separation of Concerns** - UI rendering, state handling, and data access are separated

## Project Structure

```
data-portal-ui/
├── Home.py                      # Entry point with domain selector
├── pages/
│   ├── 1_Input.py               # Domain table info (read-only)
│   ├── 2_Dashboards.py          # Filter configuration + run execution
│   └── 3_Archive.py             # Historical run results
├── components/
│   ├── __init__.py
│   ├── kpi_cards.py             # KPI display component
│   └── result_charts.py         # Chart/visualization components
├── services/
│   ├── __init__.py
│   ├── api.py                   # Mock API with SQL generation
│   └── state.py                 # Session state management
├── models/
│   ├── __init__.py
│   └── run.py                   # Run model + domain filter contracts
└── requirements.txt
```

## Domain Filter Contracts

Each domain has specific filters that translate to SQL WHERE clauses:

### Sales
| Filter | Type | SQL Column |
|--------|------|------------|
| Order Date | Date Range | `order_date` |
| Region | Multi-select | `region` |
| Product Category | Multi-select | `product_category` |
| Channel | Multi-select | `channel` |

**Gold Table:** `mart.sales_orders_fact`

### Procurement
| Filter | Type | SQL Column |
|--------|------|------------|
| Purchase Date | Date Range | `purchase_date` |
| Supplier | Multi-select | `supplier` |
| Material Group | Multi-select | `material_group` |
| Plant | Multi-select | `plant` |

**Gold Table:** `mart.procurement_orders_fact`

### Finance
| Filter | Type | SQL Column |
|--------|------|------------|
| Posting Period | Period Range | `posting_period` |
| Company Code | Multi-select | `company_code` |
| Cost Center | Multi-select | `cost_center` |
| Account | Multi-select | `account` |

**Gold Table:** `mart.gl_postings_fact`

## Sections

### 1. Input (Data Sources)
- Shows the gold table used for the selected domain
- Displays schema information and sample data preview
- Lists available filter options
- **Read-only** - tables are domain-defined, not user-selectable

### 2. Dashboards (Run Execution)
- Configure domain-specific filters
- View SQL preview (for transparency)
- Execute analytical runs
- View results: KPIs, trends, breakdowns

A **Run** consists of:
- Domain (Sales / Procurement / Finance)
- Filter parameters
- Execution timestamp
- Results (pre-computed by backend)

### 3. Archive (Historical Runs)
- View all completed runs
- Filter by domain or view all
- Re-open any historical run
- View original filters and SQL query

## Installation

```bash
# Clone the repository
git clone https://github.com/fewa2000/data-portal-ui.git
cd data-portal-ui

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run Home.py
```

## Requirements

- Python 3.10+
- Streamlit 1.28+
- Pandas 2.0+

## Usage

1. **Select Domain** - Use the sidebar to choose Sales, Procurement, or Finance
2. **View Data Source** - Go to Input to see the domain's gold table and schema
3. **Configure Filters** - Go to Dashboards, set your filter parameters
4. **Execute Run** - Click "Run" to execute the analysis
5. **View Results** - See KPIs, trends, and breakdowns
6. **Review History** - Go to Archive to view past runs

## Technical Notes

### Mock Implementation
This is a demo version with mocked data:
- API responses are simulated
- SQL is generated but not executed
- Results vary based on filter selections

### Future Backend Integration
The codebase is structured for easy backend integration:
- Replace `services/api.py` functions with actual API calls
- Filter parameters are already structured for SQL translation
- Run persistence can be moved to database storage

### What the UI Does NOT Do
- No data filtering in pandas
- No KPI calculations
- No schema inference from data
- No dynamic table selection

## License

MIT

## Contributing

This is a demo project. For production use, replace mock services with actual backend integration.
