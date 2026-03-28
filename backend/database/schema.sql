-- Hotel Management System - Full schema (MySQL / MariaDB compatible)
-- Duplicate of ../../database/schema.sql for backend/database layout.
CREATE DATABASE IF NOT EXISTS hotel_management;
USE hotel_management;

-- ---------------------------------------------------------------------------
-- Staff (referenced by users)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS staff (
  staff_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(120) NOT NULL,
  role ENUM('Waiter', 'Chef', 'Manager', 'Other') NOT NULL DEFAULT 'Waiter',
  phone VARCHAR(20) NOT NULL,
  salary DECIMAL(12, 2) NOT NULL DEFAULT 0,
  joining_date DATE NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------------
-- Application users (login)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin', 'manager', 'waiter', 'chef') NOT NULL DEFAULT 'waiter',
  staff_id INT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_users_staff FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
    ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS tables (
  table_id INT PRIMARY KEY AUTO_INCREMENT,
  table_number VARCHAR(20) NOT NULL UNIQUE,
  status ENUM('Available', 'Occupied', 'Cleaning') NOT NULL DEFAULT 'Available'
);

CREATE TABLE IF NOT EXISTS menu_items (
  item_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(120) NOT NULL UNIQUE,
  category VARCHAR(80) NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  availability BOOLEAN NOT NULL DEFAULT TRUE
);

-- order_type: table = dine-in, parcel = takeaway
-- status: Served = dine-in done; Delivered = parcel done
CREATE TABLE IF NOT EXISTS orders (
  order_id INT PRIMARY KEY AUTO_INCREMENT,
  table_id INT NULL,
  parcel_customer_name VARCHAR(120) NULL,
  parcel_phone VARCHAR(20) NULL,
  order_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  order_type ENUM('table', 'parcel') NOT NULL DEFAULT 'table',
  status ENUM('Pending', 'Preparing', 'Ready', 'Served', 'Delivered') NOT NULL DEFAULT 'Pending',
  CONSTRAINT fk_orders_table FOREIGN KEY (table_id) REFERENCES tables(table_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS order_items (
  id INT PRIMARY KEY AUTO_INCREMENT,
  order_id INT NOT NULL,
  item_id INT NOT NULL,
  quantity INT NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_order_items_menu FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS bills (
  bill_id INT PRIMARY KEY AUTO_INCREMENT,
  order_id INT NOT NULL UNIQUE,
  subtotal DECIMAL(12, 2) NOT NULL,
  gst_amount DECIMAL(12, 2) NOT NULL DEFAULT 0,
  total_amount DECIMAL(12, 2) NOT NULL,
  payment_status ENUM('Pending', 'Paid') NOT NULL DEFAULT 'Pending',
  payment_method ENUM('Cash', 'Card', 'UPI', 'Other') NOT NULL DEFAULT 'Cash',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_bills_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS attendance (
  attendance_id INT PRIMARY KEY AUTO_INCREMENT,
  staff_id INT NOT NULL,
  att_date DATE NOT NULL,
  status ENUM('present', 'absent') NOT NULL DEFAULT 'present',
  UNIQUE KEY uq_staff_date (staff_id, att_date),
  CONSTRAINT fk_att_staff FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS salary_records (
  salary_id INT PRIMARY KEY AUTO_INCREMENT,
  staff_id INT NOT NULL,
  month_year CHAR(7) NOT NULL,
  base_salary DECIMAL(12, 2) NOT NULL,
  present_days INT NOT NULL,
  working_days INT NOT NULL,
  total_salary DECIMAL(12, 2) NOT NULL,
  payment_status ENUM('Pending', 'Paid') NOT NULL DEFAULT 'Pending',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_staff_month (staff_id, month_year),
  CONSTRAINT fk_sal_staff FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);
