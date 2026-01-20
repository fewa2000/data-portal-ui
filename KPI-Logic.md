# KPI Logic Documentation

This document explains the Key Performance Indicators (KPIs) used in the Data Portal for each business domain, including their business rationale, calculation methodology, and data sources.

---

## Important Architectural Note

**KPI calculations are performed in the backend (database), NOT in the UI.**

The UI only:
1. Collects filter parameters from the user
2. Sends filters to the backend as SQL WHERE clauses
3. Displays pre-computed results

This ensures:
- Single source of truth (database)
- Consistent calculations across all consumers
- No business logic leakage into the presentation layer

---

## Sales Domain

**Gold Table:** `mart.sales_orders_fact`

### KPIs

#### 1. Total Revenue
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `total_revenue` |
| **Display Label** | Total Revenue |
| **Format** | Currency (e.g., $1,250,000) |
| **Business Definition** | The sum of all sales order values within the selected filters |

**Why this KPI?**
- Primary measure of sales performance
- Directly tied to business growth objectives
- Foundation for revenue forecasting and target tracking

**SQL Calculation:**
```sql
SELECT SUM(revenue) as total_revenue
FROM mart.sales_orders_fact
WHERE <filter_conditions>
```

---

#### 2. Total Orders
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `total_orders` |
| **Display Label** | Total Orders |
| **Format** | Integer with thousands separator (e.g., 8,420) |
| **Business Definition** | Count of distinct sales orders within the selected filters |

**Why this KPI?**
- Measures transaction volume independent of value
- Indicates customer engagement and market penetration
- Used for capacity planning and fulfillment operations

**SQL Calculation:**
```sql
SELECT COUNT(*) as total_orders
FROM mart.sales_orders_fact
WHERE <filter_conditions>
```

---

#### 3. Average Order Value (AOV)
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `avg_order_value` |
| **Display Label** | Avg Order Value |
| **Format** | Currency with 2 decimals (e.g., $148.46) |
| **Business Definition** | Total revenue divided by total number of orders |

**Why this KPI?**
- Indicates purchasing behavior and basket size
- Key metric for pricing strategy evaluation
- Used to measure cross-sell/upsell effectiveness

**SQL Calculation:**
```sql
SELECT AVG(revenue) as avg_order_value
FROM mart.sales_orders_fact
WHERE <filter_conditions>
```

**Alternative calculation:**
```sql
SELECT SUM(revenue) / COUNT(*) as avg_order_value
FROM mart.sales_orders_fact
WHERE <filter_conditions>
```

---

#### 4. Conversion Rate
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `conversion_rate` |
| **Display Label** | Conversion Rate |
| **Format** | Percentage with 1 decimal (e.g., 3.2%) |
| **Business Definition** | Percentage of customer interactions that result in a sale |

**Why this KPI?**
- Measures sales funnel efficiency
- Indicates effectiveness of sales and marketing efforts
- Critical for ROI calculations on customer acquisition

**SQL Calculation:**
```sql
SELECT
    (COUNT(DISTINCT order_id) * 100.0 / COUNT(DISTINCT visitor_id)) as conversion_rate
FROM mart.sales_orders_fact
WHERE <filter_conditions>
```

---

### Sales Trends

| Trend | Description |
|-------|-------------|
| **Revenue over Time** | Monthly revenue progression to identify growth patterns |
| **Orders over Time** | Monthly order count to track transaction volume trends |

**Breakdown Dimension:** Region (DACH, Nordics, UK, France, etc.)

---

## Procurement Domain

**Gold Table:** `mart.procurement_orders_fact`

### KPIs

#### 1. Total Spend
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `total_spend` |
| **Display Label** | Total Spend |
| **Format** | Currency (e.g., $850,000) |
| **Business Definition** | Sum of all purchase order values within the selected filters |

**Why this KPI?**
- Primary measure of procurement activity
- Essential for budget tracking and cost control
- Foundation for spend analytics and savings identification

**SQL Calculation:**
```sql
SELECT SUM(spend) as total_spend
FROM mart.procurement_orders_fact
WHERE <filter_conditions>
```

---

#### 2. Purchase Orders
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `purchase_orders` |
| **Display Label** | Purchase Orders |
| **Format** | Integer with thousands separator (e.g., 2,340) |
| **Business Definition** | Count of purchase orders within the selected filters |

**Why this KPI?**
- Measures procurement transaction volume
- Indicates operational workload for procurement team
- Used for process efficiency analysis (spend per PO)

**SQL Calculation:**
```sql
SELECT COUNT(*) as purchase_orders
FROM mart.procurement_orders_fact
WHERE <filter_conditions>
```

---

#### 3. Average PO Value
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `avg_po_value` |
| **Display Label** | Avg PO Value |
| **Format** | Currency with 2 decimals (e.g., $363.25) |
| **Business Definition** | Total spend divided by number of purchase orders |

**Why this KPI?**
- Indicates purchasing patterns and order consolidation
- Higher values may indicate better volume discounts
- Used to identify fragmented spending

**SQL Calculation:**
```sql
SELECT AVG(spend) as avg_po_value
FROM mart.procurement_orders_fact
WHERE <filter_conditions>
```

---

#### 4. On-Time Delivery Rate
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `on_time_delivery` |
| **Display Label** | On-Time Delivery |
| **Format** | Percentage with 1 decimal (e.g., 94.5%) |
| **Business Definition** | Percentage of purchase orders delivered on or before the requested date |

**Why this KPI?**
- Measures supplier reliability
- Critical for production planning and inventory management
- Key input for supplier performance reviews

**SQL Calculation:**
```sql
SELECT
    (COUNT(CASE WHEN actual_delivery_date <= requested_delivery_date THEN 1 END) * 100.0
     / COUNT(*)) as on_time_delivery
FROM mart.procurement_orders_fact
WHERE <filter_conditions>
```

---

### Procurement Trends

| Trend | Description |
|-------|-------------|
| **Spend over Time** | Monthly spend progression for budget tracking |
| **Orders over Time** | Monthly PO count to track procurement activity |

**Breakdown Dimension:** Material Group (Raw Materials, Components, Services, Equipment)

---

## Finance Domain

**Gold Table:** `mart.gl_postings_fact`

### KPIs

#### 1. Net Income
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `net_income` |
| **Display Label** | Net Income |
| **Format** | Currency (e.g., $320,000) |
| **Business Definition** | Total income minus total expenses within the selected filters |

**Why this KPI?**
- Bottom-line profitability measure
- Primary indicator of financial health
- Used for performance evaluation and investor reporting

**SQL Calculation:**
```sql
SELECT SUM(amount) as net_income
FROM mart.gl_postings_fact
WHERE <filter_conditions>
```

*Note: Assumes income is positive, expenses are negative in the GL*

**Alternative with explicit categorization:**
```sql
SELECT
    SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) -
    SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as net_income
FROM mart.gl_postings_fact
WHERE <filter_conditions>
```

---

#### 2. Operating Margin
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `operating_margin` |
| **Display Label** | Operating Margin |
| **Format** | Percentage with 1 decimal (e.g., 12.5%) |
| **Business Definition** | Operating income as a percentage of total revenue |

**Why this KPI?**
- Measures operational efficiency
- Indicates profitability from core business operations
- Comparable across time periods and business units

**SQL Calculation:**
```sql
SELECT
    (SUM(CASE WHEN account_type = 'OPERATING_INCOME' THEN amount ELSE 0 END) * 100.0
     / SUM(CASE WHEN account_type = 'REVENUE' THEN amount ELSE 0 END)) as operating_margin
FROM mart.gl_postings_fact
WHERE <filter_conditions>
```

---

#### 3. Total Expenses
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `total_expenses` |
| **Display Label** | Total Expenses |
| **Format** | Currency (e.g., $460,000) |
| **Business Definition** | Sum of all expense postings within the selected filters |

**Why this KPI?**
- Direct measure of cost structure
- Essential for budget variance analysis
- Used for cost control and optimization initiatives

**SQL Calculation:**
```sql
SELECT SUM(ABS(amount)) as total_expenses
FROM mart.gl_postings_fact
WHERE amount < 0
  AND <filter_conditions>
```

---

#### 4. Posting Count
| Attribute | Value |
|-----------|-------|
| **Metric Name** | `posting_count` |
| **Display Label** | Posting Count |
| **Format** | Integer with thousands separator (e.g., 12,500) |
| **Business Definition** | Number of GL postings within the selected filters |

**Why this KPI?**
- Measures transaction volume in the general ledger
- Indicator of accounting activity and complexity
- Used for workload planning and automation opportunities

**SQL Calculation:**
```sql
SELECT COUNT(*) as posting_count
FROM mart.gl_postings_fact
WHERE <filter_conditions>
```

---

### Finance Trends

| Trend | Description |
|-------|-------------|
| **Income over Time** | Monthly income progression |
| **Expenses over Time** | Monthly expense progression for cost tracking |

**Breakdown Dimension:** Cost Center (CC100, CC200, CC300, CC400)

---

## Filter Impact on KPIs

When users apply filters, the KPIs are recalculated based on the filtered dataset:

| Domain | Filter | Impact on KPIs |
|--------|--------|----------------|
| Sales | Date Range | KPIs reflect only orders within the date range |
| Sales | Region | KPIs filtered to selected regions only |
| Sales | Product Category | KPIs filtered to selected categories |
| Sales | Channel | KPIs filtered to selected sales channels |
| Procurement | Date Range | KPIs reflect only POs within the date range |
| Procurement | Supplier | KPIs filtered to selected suppliers |
| Procurement | Material Group | KPIs filtered to selected material groups |
| Procurement | Plant | KPIs filtered to selected plants |
| Finance | Period Range | KPIs reflect only postings within the period range |
| Finance | Company Code | KPIs filtered to selected company codes |
| Finance | Cost Center | KPIs filtered to selected cost centers |
| Finance | Account | KPIs filtered to selected GL accounts |

---

## Mock Implementation Notes

In this demo version:
- KPIs are simulated with realistic base values
- Filter selections affect results via a multiplier (more filters = smaller dataset simulation)
- Random variance is added to simulate real-world data variability
- SQL is generated for transparency but not executed

**For production:**
- Replace mock functions with actual database queries
- Implement proper aggregation logic in the data warehouse
- Add caching for frequently-used filter combinations
- Consider pre-aggregated tables for performance

---

## KPI Display Configuration

The UI formats KPIs according to this configuration:

```python
KPI_CONFIG = {
    "sales": {
        "total_revenue": {"label": "Total Revenue", "format": "${:,.0f}"},
        "total_orders": {"label": "Total Orders", "format": "{:,}"},
        "avg_order_value": {"label": "Avg Order Value", "format": "${:.2f}"},
        "conversion_rate": {"label": "Conversion Rate", "format": "{:.1f}%"},
    },
    "procurement": {
        "total_spend": {"label": "Total Spend", "format": "${:,.0f}"},
        "purchase_orders": {"label": "Purchase Orders", "format": "{:,}"},
        "avg_po_value": {"label": "Avg PO Value", "format": "${:.2f}"},
        "on_time_delivery": {"label": "On-Time Delivery", "format": "{:.1f}%"},
    },
    "finance": {
        "net_income": {"label": "Net Income", "format": "${:,.0f}"},
        "operating_margin": {"label": "Operating Margin", "format": "{:.1f}%"},
        "total_expenses": {"label": "Total Expenses", "format": "${:,.0f}"},
        "posting_count": {"label": "Posting Count", "format": "{:,}"},
    },
}
```

This configuration lives in `components/kpi_cards.py` and ensures consistent display across the application.
