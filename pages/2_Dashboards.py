"""
Dashboards Section Page.
Define filters and execute analytical runs.

A RUN is:
- Domain (Sales / Procurement / Finance)
- Filter parameters (based on domain contract)
- Execution timestamp
- Results (KPIs, charts)

Filter UI is rendered BASED ON DOMAIN.
Filters translate to SQL WHERE clauses - the UI NEVER filters data itself.
KPI calculations happen in the database, NOT in the UI.
"""

import streamlit as st
from datetime import date, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from services import api, state
from models.run import Run, RunStatus
from components.result_charts import render_run_results
from components.db_status import render_db_status
from components.data_source_badge import render_date_range_source, render_results_source

# Page configuration
st.set_page_config(
    page_title="Dashboards | Data Portal",
    page_icon="📈",
    layout="wide",
)

# Initialize state
state.init_state()

# =============================================================================
# Sidebar - Domain Selector (consistent across all pages)
# =============================================================================

with st.sidebar:
    st.header("Domain")

    domains = state.get_domains()
    current_domain = state.get_domain()

    selected_domain = st.radio(
        "Select Domain",
        domains,
        format_func=str.title,
        index=domains.index(current_domain),
        label_visibility="collapsed",
    )

    if selected_domain != current_domain:
        state.set_domain(selected_domain)
        state.clear_current_run()
        st.rerun()

    st.divider()

    run_count = state.get_run_count()
    st.caption(f"Total runs: {run_count}")

    st.divider()
    render_db_status()

# =============================================================================
# Main Content
# =============================================================================

st.title("Dashboards")

# Display current domain
domain = state.get_domain()
domain_display = domain.title()
st.markdown(f"**Domain:** {domain_display}")

st.markdown("---")

# Get filter options for this domain
filter_options = api.get_filter_options(domain)

# Get date range from database for date-based filters
date_range_min, date_range_max = api.get_date_range(domain)

# Get table info for source badges
table_info = api.DOMAIN_TABLES.get(domain, {})
table_name = table_info.get("table", "unknown")

# =============================================================================
# Domain-Specific Filter UI
# =============================================================================

st.subheader("Filters")
st.caption("Configure filters for your analysis. Filters translate to SQL WHERE clauses.")

filters = {}

if domain == "sales":
    # Sales filters: order_date (range), region, product_category, channel
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Order Date Range**")
        render_date_range_source(table_name, "order_date")
        # Use database date range or fallback to defaults
        default_from = date.fromisoformat(date_range_min) if date_range_min else date.today() - timedelta(days=180)
        default_to = date.fromisoformat(date_range_max) if date_range_max else date.today()
        date_col1, date_col2 = st.columns(2)
        with date_col1:
            date_from = st.date_input(
                "From",
                value=default_from,
                min_value=default_from if date_range_min else None,
                max_value=default_to if date_range_max else None,
                key="sales_date_from"
            )
        with date_col2:
            date_to = st.date_input(
                "To",
                value=default_to,
                min_value=default_from if date_range_min else None,
                max_value=default_to if date_range_max else None,
                key="sales_date_to"
            )
        filters["date_from"] = date_from.isoformat() if date_from else None
        filters["date_to"] = date_to.isoformat() if date_to else None

    with col2:
        regions = st.multiselect(
            "Region",
            options=filter_options.get("regions", []),
            help="Select one or more regions"
        )
        filters["regions"] = regions

    col3, col4 = st.columns(2)

    with col3:
        categories = st.multiselect(
            "Product Category",
            options=filter_options.get("product_categories", []),
            help="Select one or more product categories"
        )
        filters["product_categories"] = categories

    with col4:
        channels = st.multiselect(
            "Channel",
            options=filter_options.get("channels", []),
            help="Select one or more sales channels"
        )
        filters["channels"] = channels

elif domain == "procurement":
    # Procurement filters: purchase_date (range), supplier, material_group, plant
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Purchase Date Range**")
        render_date_range_source(table_name, "purchase_date")
        # Use database date range or fallback to defaults
        default_from = date.fromisoformat(date_range_min) if date_range_min else date.today() - timedelta(days=180)
        default_to = date.fromisoformat(date_range_max) if date_range_max else date.today()
        date_col1, date_col2 = st.columns(2)
        with date_col1:
            date_from = st.date_input(
                "From",
                value=default_from,
                min_value=default_from if date_range_min else None,
                max_value=default_to if date_range_max else None,
                key="proc_date_from"
            )
        with date_col2:
            date_to = st.date_input(
                "To",
                value=default_to,
                min_value=default_from if date_range_min else None,
                max_value=default_to if date_range_max else None,
                key="proc_date_to"
            )
        filters["date_from"] = date_from.isoformat() if date_from else None
        filters["date_to"] = date_to.isoformat() if date_to else None

    with col2:
        suppliers = st.multiselect(
            "Supplier",
            options=filter_options.get("suppliers", []),
            help="Select one or more suppliers"
        )
        filters["suppliers"] = suppliers

    col3, col4 = st.columns(2)

    with col3:
        material_groups = st.multiselect(
            "Material Group",
            options=filter_options.get("material_groups", []),
            help="Select one or more material groups"
        )
        filters["material_groups"] = material_groups

    with col4:
        plants = st.multiselect(
            "Plant",
            options=filter_options.get("plants", []),
            help="Select one or more plants"
        )
        filters["plants"] = plants

elif domain == "finance":
    # Finance filters: posting_period (range), company_code, cost_center, account
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Posting Period Range**")
        render_date_range_source(table_name, "posting_period")
        # Use database date range (posting_period is stored as DATE)
        default_from = date.fromisoformat(date_range_min) if date_range_min else date.today().replace(day=1) - timedelta(days=365)
        default_to = date.fromisoformat(date_range_max) if date_range_max else date.today().replace(day=1)

        period_col1, period_col2 = st.columns(2)
        with period_col1:
            period_from_date = st.date_input(
                "From",
                value=default_from,
                min_value=default_from if date_range_min else None,
                max_value=default_to if date_range_max else None,
                key="fin_period_from"
            )
        with period_col2:
            period_to_date = st.date_input(
                "To",
                value=default_to,
                min_value=default_from if date_range_min else None,
                max_value=default_to if date_range_max else None,
                key="fin_period_to"
            )
        # Convert dates to YYYY-MM format for the API
        filters["period_from"] = period_from_date.strftime("%Y-%m") if period_from_date else None
        filters["period_to"] = period_to_date.strftime("%Y-%m") if period_to_date else None

    with col2:
        company_codes = st.multiselect(
            "Company Code",
            options=filter_options.get("company_codes", []),
            help="Select one or more company codes"
        )
        filters["company_codes"] = company_codes

    col3, col4 = st.columns(2)

    with col3:
        cost_centers = st.multiselect(
            "Cost Center",
            options=filter_options.get("cost_centers", []),
            help="Select one or more cost centers"
        )
        filters["cost_centers"] = cost_centers

    with col4:
        accounts = st.multiselect(
            "Account",
            options=filter_options.get("accounts", []),
            help="Select one or more GL accounts"
        )
        filters["accounts"] = accounts

# =============================================================================
# SQL Preview (Transparency)
# =============================================================================

st.divider()

with st.expander("SQL Preview (for transparency)", expanded=False):
    sql_preview = api.generate_sql_preview(domain, filters)
    st.code(sql_preview, language="sql")
    st.caption(f"Query executed against: `{table_name}`")

# =============================================================================
# Run Execution
# =============================================================================

st.divider()

if st.button("Run", type="primary", use_container_width=True):
    # Create a new run
    run = Run(
        domain=domain,
        filters=filters,
        status=RunStatus.RUNNING,
    )

    # Execute the run via mock API
    with st.spinner(f"Executing run for {domain_display}..."):
        results, sql_preview = api.execute_run(domain, filters)

    # Update run with results
    run.status = RunStatus.COMPLETED
    run.results = results
    run.sql_preview = sql_preview

    # Store run in state
    state.add_run(run)
    state.set_current_run_id(run.id)

    st.success(f"Run completed: **{run.display_name}**")
    st.rerun()

# =============================================================================
# Display Current Run Results
# =============================================================================

current_run_id = state.get_current_run_id()

if current_run_id:
    current_run = state.get_run_by_id(current_run_id)

    if current_run and current_run.status == RunStatus.COMPLETED:
        st.divider()

        # Run header with clear identification
        st.subheader(f"Results: {current_run.domain.title()}")
        render_results_source(table_name, "Aggregation with GROUP BY")
        st.markdown(f"**Filters:** {current_run.get_filter_summary()}")
        st.caption(f"Executed at: {current_run.executed_at_formatted}")

        render_run_results(current_run.results, current_run.domain)

        # Option to clear current results
        if st.button("Clear Results", type="secondary"):
            state.clear_current_run()
            st.rerun()
else:
    # Show recent runs for this domain
    recent_runs = state.get_completed_runs(domain)

    if recent_runs:
        st.divider()
        st.subheader("Recent Runs")
        st.caption("Click on a run to view its results.")

        for run in recent_runs[:5]:
            with st.expander(f"{run.display_name} - {run.executed_at_formatted}"):
                if st.button("View Results", key=f"view_{run.id}"):
                    state.set_current_run_id(run.id)
                    st.rerun()
    else:
        st.info("No runs executed yet for this domain. Configure filters above and click 'Run'.")
