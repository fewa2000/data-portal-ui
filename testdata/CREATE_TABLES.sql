-- =====================================================
-- Data Portal - Table Creation Script
-- =====================================================

-- Create the mart schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS mart;

-- =====================================================
-- SALES DOMAIN
-- =====================================================

DROP TABLE IF EXISTS mart.sales_orders_fact CASCADE;

CREATE TABLE mart.sales_orders_fact (
    order_id INTEGER PRIMARY KEY,
    order_date DATE NOT NULL,
    region VARCHAR(50) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    revenue NUMERIC(10, 2) NOT NULL,
    visitor_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common filter columns
CREATE INDEX idx_sales_order_date ON mart.sales_orders_fact(order_date);
CREATE INDEX idx_sales_region ON mart.sales_orders_fact(region);
CREATE INDEX idx_sales_product_category ON mart.sales_orders_fact(product_category);
CREATE INDEX idx_sales_channel ON mart.sales_orders_fact(channel);
CREATE INDEX idx_sales_visitor_id ON mart.sales_orders_fact(visitor_id);

COMMENT ON TABLE mart.sales_orders_fact IS 'Sales orders fact table for revenue and order analytics';
COMMENT ON COLUMN mart.sales_orders_fact.order_id IS 'Unique order identifier';
COMMENT ON COLUMN mart.sales_orders_fact.visitor_id IS 'Customer/visitor identifier for conversion tracking';

-- =====================================================
-- PROCUREMENT DOMAIN
-- =====================================================

DROP TABLE IF EXISTS mart.procurement_orders_fact CASCADE;

CREATE TABLE mart.procurement_orders_fact (
    purchase_order_id INTEGER PRIMARY KEY,
    purchase_date DATE NOT NULL,
    supplier VARCHAR(100) NOT NULL,
    material_group VARCHAR(100) NOT NULL,
    plant VARCHAR(100) NOT NULL,
    spend NUMERIC(12, 2) NOT NULL,
    requested_delivery_date DATE NOT NULL,
    actual_delivery_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common filter columns
CREATE INDEX idx_procurement_purchase_date ON mart.procurement_orders_fact(purchase_date);
CREATE INDEX idx_procurement_supplier ON mart.procurement_orders_fact(supplier);
CREATE INDEX idx_procurement_material_group ON mart.procurement_orders_fact(material_group);
CREATE INDEX idx_procurement_plant ON mart.procurement_orders_fact(plant);
CREATE INDEX idx_procurement_delivery_dates ON mart.procurement_orders_fact(requested_delivery_date, actual_delivery_date);

COMMENT ON TABLE mart.procurement_orders_fact IS 'Procurement orders fact table for spend and supplier performance analytics';
COMMENT ON COLUMN mart.procurement_orders_fact.actual_delivery_date IS 'Used to calculate on-time delivery KPI';

-- =====================================================
-- FINANCE DOMAIN
-- =====================================================

DROP TABLE IF EXISTS mart.gl_postings_fact CASCADE;

CREATE TABLE mart.gl_postings_fact (
    posting_id INTEGER PRIMARY KEY,
    posting_period DATE NOT NULL,
    company_code VARCHAR(10) NOT NULL,
    cost_center VARCHAR(20) NOT NULL,
    account VARCHAR(10) NOT NULL,
    account_type VARCHAR(50) NOT NULL CHECK (account_type IN ('REVENUE', 'OPERATING_INCOME', 'EXPENSE')),
    amount NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common filter columns
CREATE INDEX idx_finance_posting_period ON mart.gl_postings_fact(posting_period);
CREATE INDEX idx_finance_company_code ON mart.gl_postings_fact(company_code);
CREATE INDEX idx_finance_cost_center ON mart.gl_postings_fact(cost_center);
CREATE INDEX idx_finance_account ON mart.gl_postings_fact(account);
CREATE INDEX idx_finance_account_type ON mart.gl_postings_fact(account_type);

COMMENT ON TABLE mart.gl_postings_fact IS 'General ledger postings fact table for financial analytics';
COMMENT ON COLUMN mart.gl_postings_fact.amount IS 'Positive for income/revenue, negative for expenses';
COMMENT ON COLUMN mart.gl_postings_fact.account_type IS 'Categorization for KPI calculations (REVENUE, OPERATING_INCOME, EXPENSE)';

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Check table structures
SELECT 
    table_schema, 
    table_name, 
    column_name, 
    data_type, 
    character_maximum_length
FROM information_schema.columns
WHERE table_schema = 'mart'
ORDER BY table_name, ordinal_position;