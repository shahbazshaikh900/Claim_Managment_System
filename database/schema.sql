-- =====================================================
-- Tyre Claim Management System (TCMS)
-- Database Schema
-- Version: 1.0
-- =====================================================

CREATE TABLE IF NOT EXISTS claims (

    claim_number TEXT PRIMARY KEY,

    docket_date TEXT,

    notification_number TEXT,

    customer_name TEXT NOT NULL,

    tyre_model TEXT,

    serial_number TEXT,

    status TEXT,

    defect_reason TEXT,

    replacement_offer REAL,

    claim_loss REAL,

    wear_percent REAL,

    invoice_number TEXT,

    invoice_date TEXT,

    uploaded_at TEXT
);
