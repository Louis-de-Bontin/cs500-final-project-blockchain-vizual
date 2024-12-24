CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing primary key
    address CHAR(42) NOT NULL UNIQUE,   -- Required unique address field
    alias TEXT NOT NULL,                -- Required alias field
    type VARCHAR(20) NOT NULL,          -- Required type field
    malicious BOOLEAN DEFAULT FALSE,    -- Boolean field, default value is false
    continue BOOLEAN DEFAULT TRUE       -- Boolean field, default value is true
);