-- ============================================
-- Sales By Twilight - Seed Data
-- Sample data for the grocery store database
-- ============================================

USE sales_by_twilight;

-- ============================================
-- CATEGORIES
-- ============================================
-- Clear existing data (for re-seeding)
DELETE FROM order_item;
DELETE FROM `order`;
DELETE FROM product;
DELETE FROM customer;
DELETE FROM category;

-- Reset auto-increment counters
ALTER TABLE category AUTO_INCREMENT = 1;
ALTER TABLE product AUTO_INCREMENT = 1;
ALTER TABLE customer AUTO_INCREMENT = 1;
ALTER TABLE `order` AUTO_INCREMENT = 1;
ALTER TABLE order_item AUTO_INCREMENT = 1;

-- Insert categories
INSERT INTO category (name, description) VALUES
('Fresh Produce', 'Fresh fruits and vegetables sourced from local farms'),
('Dairy & Eggs', 'Milk, cheese, butter, yogurt, and farm-fresh eggs'),
('Beverages', 'Soft drinks, juices, water, tea, and coffee'),
('Bakery', 'Fresh bread, cakes, pastries, and baked goods'),
('Meat & Poultry', 'Fresh cuts of beef, chicken, pork, and lamb'),
('Seafood', 'Fresh and frozen fish, prawns, and shellfish'),
('Frozen Foods', 'Frozen meals, vegetables, and ice cream'),
('Pantry Staples', 'Rice, pasta, cooking oils, and canned goods'),
('Snacks & Confectionery', 'Crisps, chocolates, biscuits, and sweets'),
('Household & Cleaning', 'Cleaning supplies and household essentials');

-- ============================================
-- PRODUCTS
-- ============================================

-- Fresh Produce (category_id = 1)
INSERT INTO product (name, description, price, stock_quantity, category_id) VALUES
('Organic Bananas', 'Bundle of 5-6 organic bananas', 1.29, 150, 1),
('Red Apples', 'Pack of 6 British Gala apples', 2.49, 100, 1),
('Carrots', '1kg bag of fresh carrots', 0.89, 200, 1),
('Broccoli', 'Fresh broccoli head, approximately 350g', 1.19, 80, 1),
('Cherry Tomatoes', '250g punnet of cherry tomatoes', 1.79, 120, 1),
('Potatoes', '2.5kg bag of white potatoes', 2.29, 90, 1),
('Cucumber', 'Fresh whole cucumber', 0.69, 100, 1),
('Spinach', '200g bag of baby spinach leaves', 1.99, 60, 1),
('Avocados', 'Pack of 2 ripe avocados', 2.49, 75, 1),
('Lemons', 'Pack of 4 unwaxed lemons', 1.29, 85, 1);

-- Dairy & Eggs (category_id = 2)
INSERT INTO product (name, description, price, stock_quantity, category_id) VALUES
('Whole Milk', '2 litre bottle of whole milk', 1.89, 200, 2),
('Semi-Skimmed Milk', '2 litre bottle of semi-skimmed milk', 1.79, 250, 2),
('Free Range Eggs', 'Box of 12 large free-range eggs', 3.49, 100, 2),
('Cheddar Cheese', '400g block of mature cheddar', 4.29, 80, 2),
('Salted Butter', '250g block of British salted butter', 2.49, 120, 2),
('Greek Yogurt', '500g pot of natural Greek yogurt', 2.79, 90, 2),
('Double Cream', '300ml pot of fresh double cream', 1.69, 70, 2),
('Mozzarella', '125g ball of fresh mozzarella', 1.99, 65, 2);

-- Beverages (category_id = 3)
INSERT INTO product (name, description, price, stock_quantity, category_id) VALUES
('Orange Juice', '1 litre carton of freshly squeezed orange juice', 2.49, 100, 3),
('Apple Juice', '1 litre carton of pure apple juice', 1.99, 110, 3),
('Still Water', '6 pack of 500ml still water bottles', 2.29, 150, 3),
('Sparkling Water', '6 pack of 500ml sparkling water bottles', 2.49, 120, 3),
('English Breakfast Tea', 'Box of 80 English breakfast tea bags', 3.29, 80, 3),
('Ground Coffee', '200g bag of medium roast ground coffee', 4.49, 60, 3),
('Cola', '6 pack of 330ml cola cans', 3.99, 100, 3),
('Lemonade', '2 litre bottle of traditional lemonade', 1.49, 90, 3);

-- Bakery (category_id = 4)
INSERT INTO product (name, description, price, stock_quantity, category_id) VALUES
('White Bread', '800g loaf of soft white bread', 1.29, 80, 4),
('Wholemeal Bread', '800g loaf of wholemeal bread', 1.49, 70, 4),
('Croissants', 'Pack of 4 all-butter croissants', 2.29, 50, 4),
('Chocolate Muffins', 'Pack of 4 double chocolate muffins', 2.49, 45, 4),
('Sourdough Loaf', 'Artisan sourdough bread loaf', 2.99, 40, 4),
('Bagels', 'Pack of 5 plain bagels', 1.79, 55, 4);

-- Meat & Poultry (category_id = 5)
INSERT INTO product (name, description, price, stock_quantity, category_id) VALUES
('Chicken Breast', '500g pack of skinless chicken breast fillets', 5.49, 60, 5),
('Beef Mince', '500g pack of lean beef mince (5% fat)', 4.29, 70, 5),
('Pork Sausages', 'Pack of 8 premium pork sausages', 3.49, 55, 5),
('Back Bacon', '300g pack of smoked back bacon rashers', 3.99, 65, 5),
('Lamb Chops', 'Pack of 4 lamb loin chops', 7.99, 35, 5),
('Whole Chicken', '1.5kg free-range whole chicken', 6.49, 30, 5);

-- Seafood (category_id = 6)
INSERT INTO product (name, description, price, stock_quantity, category_id) VALUES
('Salmon Fillets', 'Pack of 2 Scottish salmon fillets', 6.99, 40, 6),
('Cod Fillets', 'Pack of 2 Atlantic cod fillets', 5.99, 45, 6),
('King Prawns', '200g pack of raw king prawns', 5.49, 50, 6),
('Smoked Mackerel', 'Pack of 2 smoked mackerel fillets', 3.99, 40, 6),
('Tuna Steaks', 'Pack of 2 yellowfin tuna steaks', 7.49, 30, 6);

-- Frozen Foods (category_id = 7)
INSERT INTO product (name, description, price, stock_quantity, category_id) VALUES
('Garden Peas', '1kg bag of frozen garden peas', 1.49, 100, 7),
('Fish Fingers', 'Box of 10 cod fish fingers', 2.99, 80, 7),
('Vanilla Ice Cream', '1 litre tub of vanilla ice cream', 3.49, 60, 7),
('Frozen Pizza', 'Margherita pizza, 350g', 2.99, 70, 7),
('Chips', '1kg bag of frozen oven chips', 1.99, 90, 7),
('Mixed Vegetables', '1kg bag of frozen mixed vegetables', 1.79, 85, 7);

-- Pantry Staples (category_id = 8)
INSERT INTO product (name, description, price, stock_quantity, category_id) VALUES
('Basmati Rice', '1kg bag of basmati rice', 2.29, 100, 8),
('Spaghetti', '500g pack of Italian spaghetti', 1.29, 120, 8),
('Olive Oil', '500ml bottle of extra virgin olive oil', 4.99, 60, 8),
('Chopped Tomatoes', '400g tin of chopped tomatoes', 0.79, 200, 8),
('Baked Beans', '415g tin of baked beans in tomato sauce', 0.89, 180, 8),
('Peanut Butter', '340g jar of smooth peanut butter', 2.49, 70, 8),
('Honey', '340g jar of clear honey', 3.99, 55, 8),
('Plain Flour', '1.5kg bag of plain flour', 1.29, 90, 8);

-- Snacks & Confectionery (category_id = 9)
INSERT INTO product (name, description, price, stock_quantity, category_id) VALUES
('Sea Salt Crisps', '150g bag of sea salt crisps', 1.99, 100, 9),
('Milk Chocolate Bar', '100g bar of milk chocolate', 1.49, 150, 9),
('Digestive Biscuits', '400g pack of milk chocolate digestives', 1.79, 80, 9),
('Mixed Nuts', '200g bag of roasted mixed nuts', 2.99, 60, 9),
('Fruit & Nut Mix', '150g bag of dried fruit and nut mix', 2.49, 70, 9);

-- Household & Cleaning (category_id = 10)
INSERT INTO product (name, description, price, stock_quantity, category_id) VALUES
('Washing Up Liquid', '500ml bottle of washing up liquid', 1.29, 100, 10),
('Kitchen Roll', 'Pack of 2 kitchen roll', 2.49, 80, 10),
('Bin Bags', 'Roll of 20 black bin bags', 1.99, 90, 10),
('All-Purpose Cleaner', '750ml spray bottle of all-purpose cleaner', 2.29, 70, 10),
('Laundry Detergent', '1.5 litre bottle of laundry liquid', 4.99, 50, 10);

-- ============================================
-- CUSTOMERS
-- ============================================

INSERT INTO customer (first_name, last_name, email, phone) VALUES
('Emma', 'Thompson', 'emma.thompson@email.co.uk', '07700900001'),
('James', 'Wilson', 'james.wilson@email.co.uk', '07700900002'),
('Sophie', 'Brown', 'sophie.brown@email.co.uk', '07700900003'),
('Oliver', 'Taylor', 'oliver.taylor@email.co.uk', '07700900004'),
('Charlotte', 'Davies', 'charlotte.davies@email.co.uk', '07700900005'),
('William', 'Evans', 'william.evans@email.co.uk', '07700900006'),
('Amelia', 'Roberts', 'amelia.roberts@email.co.uk', '07700900007'),
('George', 'Johnson', 'george.johnson@email.co.uk', '07700900008'),
('Isla', 'Walker', 'isla.walker@email.co.uk', '07700900009'),
('Harry', 'Wright', 'harry.wright@email.co.uk', '07700900010');

-- ============================================
-- ORDERS
-- ============================================

-- Order 1: Emma's weekly shop
INSERT INTO `order` (customer_id, total_amount, status) VALUES
(1, 23.45, 'delivered');

-- Order 2: James's quick shop
INSERT INTO `order` (customer_id, total_amount, status) VALUES
(2, 12.67, 'delivered');

-- Order 3: Sophie's order (being prepared)
INSERT INTO `order` (customer_id, total_amount, status) VALUES
(3, 34.89, 'processing');

-- Order 4: Oliver's order (just placed)
INSERT INTO `order` (customer_id, total_amount, status) VALUES
(4, 18.99, 'pending');

-- Order 5: Charlotte's order (on the way)
INSERT INTO `order` (customer_id, total_amount, status) VALUES
(5, 45.67, 'shipped');

-- ============================================
-- ORDER ITEMS
-- ============================================

-- Order 1 items (Emma)
INSERT INTO order_item (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 2, 1.29),   -- 2x Organic Bananas
(1, 11, 1, 1.89),  -- 1x Whole Milk
(1, 13, 1, 3.49),  -- 1x Free Range Eggs
(1, 21, 2, 2.49),  -- 2x Orange Juice
(1, 31, 1, 1.29),  -- 1x White Bread
(1, 45, 1, 2.29);  -- 1x Basmati Rice

-- Order 2 items (James)
INSERT INTO order_item (order_id, product_id, quantity, unit_price) VALUES
(2, 37, 1, 5.49),  -- 1x Chicken Breast
(2, 3, 1, 0.89),   -- 1x Carrots
(2, 4, 1, 1.19),   -- 1x Broccoli
(2, 46, 2, 1.29);  -- 2x Spaghetti

-- Order 3 items (Sophie)
INSERT INTO order_item (order_id, product_id, quantity, unit_price) VALUES
(3, 43, 1, 6.99),  -- 1x Salmon Fillets
(3, 8, 2, 1.99),   -- 2x Spinach
(3, 9, 1, 2.49),   -- 1x Avocados
(3, 47, 1, 4.99),  -- 1x Olive Oil
(3, 16, 1, 2.79),  -- 1x Greek Yogurt
(3, 25, 1, 3.29),  -- 1x English Breakfast Tea
(3, 10, 1, 1.29);  -- 1x Lemons

-- Order 4 items (Oliver)
INSERT INTO order_item (order_id, product_id, quantity, unit_price) VALUES
(4, 39, 1, 3.49),  -- 1x Pork Sausages
(4, 40, 1, 3.99),  -- 1x Back Bacon
(4, 13, 1, 3.49),  -- 1x Free Range Eggs
(4, 31, 1, 1.29),  -- 1x White Bread
(4, 27, 1, 3.99);  -- 1x Cola

-- Order 5 items (Charlotte)
INSERT INTO order_item (order_id, product_id, quantity, unit_price) VALUES
(5, 42, 1, 6.49),  -- 1x Whole Chicken
(5, 6, 1, 2.29),   -- 1x Potatoes
(5, 3, 2, 0.89),   -- 2x Carrots
(5, 4, 1, 1.19),   -- 1x Broccoli
(5, 14, 1, 4.29),  -- 1x Cheddar Cheese
(5, 11, 2, 1.89),  -- 2x Whole Milk
(5, 55, 1, 1.99),  -- 1x Mixed Nuts
(5, 53, 1, 1.79),  -- 1x Digestive Biscuits
(5, 51, 1, 3.49),  -- 1x Vanilla Ice Cream
(5, 58, 1, 2.49);  -- 1x Kitchen Roll

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Uncomment to verify data was inserted correctly:

-- SELECT 'Categories:' AS '';
-- SELECT COUNT(*) AS total_categories FROM category;

-- SELECT 'Products by Category:' AS '';
-- SELECT c.name AS category, COUNT(p.id) AS product_count 
-- FROM category c 
-- LEFT JOIN product p ON c.id = p.category_id 
-- GROUP BY c.id, c.name 
-- ORDER BY c.id;

-- SELECT 'Customers:' AS '';
-- SELECT COUNT(*) AS total_customers FROM customer;

-- SELECT 'Orders by Status:' AS '';
-- SELECT status, COUNT(*) AS order_count FROM `order` GROUP BY status;

-- SELECT 'Total Order Items:' AS '';
-- SELECT COUNT(*) AS total_order_items FROM order_item;
