-- Enable pgcrypto extension to generate UUID
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Insert dummy data into the Product table
INSERT INTO Product (name, description, category, price, sku)
VALUES
  ('Product 1', 'Description of Product 1', 'Category A', 10.99, 'SKU001'),
  ('Product 2', 'Description of Product 2', 'Category B', 15.50, 'SKU002'),
  ('Product 3', 'Description of Product 3', 'Category A', 7.00, 'SKU003'),
  ('Product 4', 'Description of Product 4', 'Category C', 25.75, 'SKU004'),
  ('Product 5', 'Description of Product 5', 'Category B', 9.99, 'SKU005'),
  ('Product 6', 'Description of Product 6', 'Category A', 30.00, 'SKU006'),
  ('Product 7', 'Description of Product 7', 'Category C', 45.00, 'SKU007'),
  ('Product 8', 'Description of Product 8', 'Category B', 19.99, 'SKU008'),
  ('Product 9', 'Description of Product 9', 'Category A', 12.49, 'SKU009'),
  ('Product 10', 'Description of Product 10', 'Category C', 5.99, 'SKU010'),
  ('Product 11', 'Description of Product 11', 'Category B', 8.99, 'SKU011'),
  ('Product 12', 'Description of Product 12', 'Category A', 18.50, 'SKU012'),
  ('Product 13', 'Description of Product 13', 'Category C', 22.30, 'SKU013'),
  ('Product 14', 'Description of Product 14', 'Category A', 14.75, 'SKU014'),
  ('Product 15', 'Description of Product 15', 'Category B', 16.99, 'SKU015'),
  ('Product 16', 'Description of Product 16', 'Category C', 28.60, 'SKU016'),
  ('Product 17', 'Description of Product 17', 'Category A', 11.25, 'SKU017'),
  ('Product 18', 'Description of Product 18', 'Category B', 35.00, 'SKU018'),
  ('Product 19', 'Description of Product 19', 'Category A', 20.10, 'SKU019'),
  ('Product 20', 'Description of Product 20', 'Category C', 40.00, 'SKU020');

-- Insert dummy data into the Inventory table
INSERT INTO Inventory (product_id, store_id, quantity, min_stock)
VALUES
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU001'), '<UUID_FOR_STORE_1>', 200, 15),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU002'), '<UUID_FOR_STORE_1>', 100, 10),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU003'), '<UUID_FOR_STORE_2>', 50, 5),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU004'), '<UUID_FOR_STORE_2>', 120, 10),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU005'), '<UUID_FOR_STORE_3>', 150, 20),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU006'), '<UUID_FOR_STORE_3>', 80, 8),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU007'), '<UUID_FOR_STORE_4>', 90, 9),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU008'), '<UUID_FOR_STORE_4>', 250, 25),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU009'), '<UUID_FOR_STORE_5>', 300, 30),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU010'), '<UUID_FOR_STORE_5>', 60, 6),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU011'), '<UUID_FOR_STORE_1>', 70, 7),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU012'), '<UUID_FOR_STORE_1>', 110, 10),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU018'), '<UUID_FOR_STORE_2>', 140, 14),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU014'), '<UUID_FOR_STORE_2>', 180, 18),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU015'), '<UUID_FOR_STORE_3>', 75, 7),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU016'), '<UUID_FOR_STORE_3>', 210, 21),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU017'), '<UUID_FOR_STORE_4>', 95, 9),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU018'), '<UUID_FOR_STORE_4>', 130, 13),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU019'), '<UUID_FOR_STORE_5>', 85, 8),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU020'), '<UUID_FOR_STORE_5>', 100, 10);

-- Insert dummy data into the Transfer table
INSERT INTO Transfer (product_id, source_store_id, target_store_id, quantity, type)
VALUES
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU001'), '<UUID_FOR_STORE_1>', '<UUID_FOR_STORE_2>', 50, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU002'), '<UUID_FOR_STORE_1>', '<UUID_FOR_STORE_3>', 30, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU003'), '<UUID_FOR_STORE_2>', '<UUID_FOR_STORE_4>', 25, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU004'), '<UUID_FOR_STORE_2>', '<UUID_FOR_STORE_5>', 70, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU005'), '<UUID_FOR_STORE_3>', '<UUID_FOR_STORE_4>', 100, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU006'), '<UUID_FOR_STORE_3>', '<UUID_FOR_STORE_5>', 50, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU007'), '<UUID_FOR_STORE_4>', '<UUID_FOR_STORE_1>', 40, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU008'), '<UUID_FOR_STORE_4>', '<UUID_FOR_STORE_2>', 60, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU009'), '<UUID_FOR_STORE_5>', '<UUID_FOR_STORE_3>', 90, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU010'), '<UUID_FOR_STORE_5>', '<UUID_FOR_STORE_4>', 45, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU011'), '<UUID_FOR_STORE_1>', '<UUID_FOR_STORE_2>', 25, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU012'), '<UUID_FOR_STORE_1>', '<UUID_FOR_STORE_3>', 60, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU013'), '<UUID_FOR_STORE_2>', '<UUID_FOR_STORE_4>', 35, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU014'), '<UUID_FOR_STORE_2>', '<UUID_FOR_STORE_5>', 80, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU015'), '<UUID_FOR_STORE_3>', '<UUID_FOR_STORE_1>', 55, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU016'), '<UUID_FOR_STORE_3>', '<UUID_FOR_STORE_2>', 120, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU017'), '<UUID_FOR_STORE_4>', '<UUID_FOR_STORE_3>', 40, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU018'), '<UUID_FOR_STORE_4>', '<UUID_FOR_STORE_5>', 60, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU019'), '<UUID_FOR_STORE_5>', '<UUID_FOR_STORE_1>', 80, 'TRANSFER'),
  ((SELECT p.id FROM Product p WHERE p.sku = 'SKU020'), '<UUID_FOR_STORE_5>', '<UUID_FOR_STORE_2>', 100, 'TRANSFER');
