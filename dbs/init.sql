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
    productId UUID REFERENCES Product(id) ON DELETE CASCADE,
    storeId VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    minStock INTEGER NOT NULL CHECK (minStock >= 0),
    UNIQUE (productId, storeId)
);
CREATE INDEX idx_inventory_productId ON Inventory(productId);
CREATE INDEX idx_inventory_storeId ON Inventory(storeId);

-- Transfer Table
CREATE TABLE Transfer (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    productId UUID REFERENCES Product(id) ON DELETE CASCADE,
    sourceStoreId VARCHAR(50),
    targetStoreId VARCHAR(50),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    timestamp TIMESTAMPTZ DEFAULT now(),
    type VARCHAR(10) NOT NULL CHECK (type IN ('IN', 'OUT', 'TRANSFER'))
);
CREATE INDEX idx_transfer_productId ON Transfer(productId);
CREATE INDEX idx_transfer_sourceStoreId ON Transfer(sourceStoreId);
CREATE INDEX idx_transfer_targetStoreId ON Transfer(targetStoreId);
CREATE INDEX idx_transfer_timestamp ON Transfer(timestamp);
