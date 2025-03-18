-- Enable pgcrypto for UUID generation
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Product Table
CREATE TABLE Product (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    sku VARCHAR(50) UNIQUE NOT NULL
);
CREATE INDEX idx_product_category ON Product(category);
CREATE INDEX idx_product_price ON Product(price);

-- Inventory Table
CREATE TABLE Inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES Product(id) ON DELETE CASCADE,
    store_id VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    min_stock INTEGER NOT NULL CHECK (min_stock >= 0),
    UNIQUE (product_id, store_id)
);
CREATE INDEX idx_inventory_product_id ON Inventory(product_id);
CREATE INDEX idx_inventory_store_id ON Inventory(store_id);

-- Transfer Table
CREATE TABLE Transfer (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES Product(id) ON DELETE CASCADE,
    source_store_id VARCHAR(50),
    target_store_id VARCHAR(50),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    timestamp TIMESTAMPTZ DEFAULT now(),
    type VARCHAR(10) NOT NULL CHECK (type IN ('IN', 'OUT', 'TRANSFER'))
);
CREATE INDEX idx_transfer_product_id ON Transfer(product_id);
CREATE INDEX idx_transfer_source_store_id ON Transfer(source_store_id);
CREATE INDEX idx_transfer_target_store_id ON Transfer(target_store_id);
CREATE INDEX idx_transfer_timestamp ON Transfer(timestamp);
