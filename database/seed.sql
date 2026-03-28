USE hotel_management;

INSERT IGNORE INTO tables (table_number, status) VALUES
('Table 1', 'Available'),
('Table 2', 'Available'),
('Table 3', 'Available'),
('Table 4', 'Available'),
('Table 5', 'Available');

-- Swagat Corner menu (matches printed card). Re-run safe: updates price/category on duplicate name.
INSERT INTO menu_items (name, category, price, availability) VALUES
-- Punjabi
('Kaju Almond Mastana', 'Punjabi', 270.00, TRUE),
('Fried Kaju Handi', 'Punjabi', 240.00, TRUE),
('Mushrrom Masala', 'Punjabi', 240.00, TRUE),
('Cheese Paneer Masala', 'Punjabi', 200.00, TRUE),
('Cheese Butter Masala', 'Punjabi', 190.00, TRUE),
('Cheese Panner Butter Masala', 'Punjabi', 220.00, TRUE),
('Kaju Paneer Masala', 'Punjabi', 210.00, TRUE),
('Baby Corn Butter Masala', 'Punjabi', 210.00, TRUE),
('Paneer Swagat', 'Punjabi', 220.00, TRUE),
('Paneer Rasila', 'Punjabi', 220.00, TRUE),
('Paneer Peshawari', 'Punjabi', 210.00, TRUE),
('Paneer Patiyala', 'Punjabi', 200.00, TRUE),
('Paneer Basanti', 'Punjabi', 210.00, TRUE),
('Paneer Rajwadi', 'Punjabi', 200.00, TRUE),
('Paneer Kohinoor', 'Punjabi', 200.00, TRUE),
('Paneer Handi', 'Punjabi', 190.00, TRUE),
('Paneer Toofani', 'Punjabi', 200.00, TRUE),
('Paneer Chatpata', 'Punjabi', 190.00, TRUE),
('Paneer Kadhai', 'Punjabi', 190.00, TRUE),
('Paneer Corn Palak', 'Punjabi', 210.00, TRUE),
('Paneer Corn Masala', 'Punjabi', 210.00, TRUE),
('Paneer Butter Masala', 'Punjabi', 190.00, TRUE),
('Paneer Bhurji Masala', 'Punjabi', 200.00, TRUE),
('Paneer Tikka Masala', 'Punjabi', 170.00, TRUE),
('Paneer Tawa', 'Punjabi', 210.00, TRUE),
('Paneer Kofta', 'Punjabi', 170.00, TRUE),
('Mutter Paneer', 'Punjabi', 160.00, TRUE),
('Palak Paneer', 'Punjabi', 160.00, TRUE),
('Kaju Masala', 'Punjabi', 190.00, TRUE),
('Kaju Lasaniya', 'Punjabi', 230.00, TRUE),
('Kaju Khoya (Sweet)', 'Punjabi', 220.00, TRUE),
('Veg. Tawa', 'Punjabi', 210.00, TRUE),
('Veg. Aflatun', 'Punjabi', 210.00, TRUE),
('Veg. Maharaja', 'Punjabi', 210.00, TRUE),
('Veg. Makhanwala', 'Punjabi', 190.00, TRUE),
('Veg. Handi', 'Punjabi', 190.00, TRUE),
('Veg. Kolhapuri', 'Punjabi', 190.00, TRUE),
('Veg. Kadhai', 'Punjabi', 190.00, TRUE),
('Chole Chana Masala', 'Punjabi', 150.00, TRUE),
('Dal Fry', 'Punjabi', 125.00, TRUE),
('Dal Fry Butter', 'Punjabi', 140.00, TRUE),
('Dal Tadka', 'Punjabi', 140.00, TRUE),
-- Rice / Pulav
('Kaju Pulav', 'Rice/Pulav', 160.00, TRUE),
('Cheese Pulav', 'Rice/Pulav', 160.00, TRUE),
('Kashmiri Pulav (Sweet)', 'Rice/Pulav', 160.00, TRUE),
('Paneer Pulav', 'Rice/Pulav', 150.00, TRUE),
('Cheese Matka Biryani', 'Rice/Pulav', 240.00, TRUE),
('Veg. Pulav', 'Rice/Pulav', 140.00, TRUE),
('Afgani Biryani', 'Rice/Pulav', 240.00, TRUE),
('Dum Biryani', 'Rice/Pulav', 190.00, TRUE),
('Hydrabadi Biryani', 'Rice/Pulav', 180.00, TRUE),
('Veg. Biryani', 'Rice/Pulav', 170.00, TRUE),
('Masala Rice', 'Rice/Pulav', 140.00, TRUE),
('Jeera Rice', 'Rice/Pulav', 120.00, TRUE),
-- Roti / Papad
('Butter Naan', 'Roti / Papad', 40.00, TRUE),
('Plain Naan', 'Roti / Papad', 35.00, TRUE),
('Butter Paratha', 'Roti / Papad', 40.00, TRUE),
('Plain Paratha', 'Roti / Papad', 30.00, TRUE),
('Tandoori Butter Roti', 'Roti / Papad', 22.00, TRUE),
('Tandoori Plain Roti', 'Roti / Papad', 18.00, TRUE),
('Roomali Plain Roti', 'Roti / Papad', 30.00, TRUE),
('Roomali Butter Roti', 'Roti / Papad', 35.00, TRUE),
('Tawa Butter Roti', 'Roti / Papad', 15.00, TRUE),
('Tawa Plain Roti', 'Roti / Papad', 13.00, TRUE),
('Roasted Papad (Lijjat)', 'Roti / Papad', 22.00, TRUE),
('Fried Papad (Lijjat)', 'Roti / Papad', 30.00, TRUE),
('Masala Papad (Lijjat)', 'Roti / Papad', 50.00, TRUE),
-- Chinese
('Paneer Chilly (Dry)', 'Chinese', 210.00, TRUE),
('Veg. Manchurian (Dry)', 'Chinese', 150.00, TRUE),
('Veg. Manchurian (Gravy)', 'Chinese', 140.00, TRUE),
('Veg. Schezwan Noodles (Spicy)', 'Chinese', 130.00, TRUE),
('Veg. Manchurain Noodles', 'Chinese', 130.00, TRUE),
('Veg. Hakka Noodles', 'Chinese', 130.00, TRUE),
('Schezwan Fried Rice (Spicy)', 'Chinese', 140.00, TRUE),
('Manchurian Fried Rice', 'Chinese', 150.00, TRUE),
('Veg. Fried Rice', 'Chinese', 140.00, TRUE),
('Bombay Bhel', 'Chinese', 150.00, TRUE),
('Veg. Chinese Bhel', 'Chinese', 140.00, TRUE),
-- Pav-Bhaji
('Cheese Pav Bhaji', 'Pav-Bhaji', 130.00, TRUE),
('Amul Butter Pav Bhaji', 'Pav-Bhaji', 120.00, TRUE),
('Plain Pav Bhaji', 'Pav-Bhaji', 110.00, TRUE),
('Extra Pav', 'Pav-Bhaji', 10.00, TRUE),
('Amul Butter Pav', 'Pav-Bhaji', 12.00, TRUE),
-- Butter Milk / Water (MRP items priced at 0 — settle at counter)
('Butter Milk (Chhas)', 'Butter Milk / Water', 25.00, TRUE),
('Cold Drinks (MRP)', 'Butter Milk / Water', 0.00, TRUE)
ON DUPLICATE KEY UPDATE
  category = VALUES(category),
  price = VALUES(price),
  availability = VALUES(availability);

INSERT INTO staff (name, role, phone, salary, joining_date) VALUES
('Demo Waiter', 'Waiter', '9000000001', 15000.00, '2024-01-15'),
('Demo Chef', 'Chef', '9000000002', 20000.00, '2024-02-01'),
('Demo Manager', 'Manager', '9000000003', 35000.00, '2023-06-01');

-- Login: admin / admin123
INSERT IGNORE INTO users (username, password_hash, role, staff_id) VALUES
('admin', 'pbkdf2:sha256:600000$wnS3zS5okMISFNJK$d09fac34ba5b20c5131673b65bdb4b71283a9af654a577ca824a8b51ec9c31bd', 'admin', NULL);
