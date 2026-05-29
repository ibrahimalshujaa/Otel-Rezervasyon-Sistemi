-- Hotel Reservation System Database Schema & Initialization
-- Project Title: Otel Rezervasyon Sistemi
-- Author: Antigravity AI

DROP DATABASE IF EXISTS hotel_reservation_db;
CREATE DATABASE hotel_reservation_db;
USE hotel_reservation_db;

-- =========================================================================
-- 1. DROP EXISTING CONSTRAINTS / TABLES / FUNCTIONS / TRIGGERS / PROCEDURES
-- =========================================================================

DROP TRIGGER IF EXISTS trg_AfterReservationInsert;
DROP TRIGGER IF EXISTS trg_AfterReservationUpdate;

DROP FUNCTION IF EXISTS fn_CalculateStayDays;
DROP FUNCTION IF EXISTS fn_CalculateReservationCost;

-- -------------------------------------------------------------------------
-- DROP EXISTING STORED PROCEDURES
-- -------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS sp_AddCustomer;
DROP PROCEDURE IF EXISTS sp_UpdateCustomer;
DROP PROCEDURE IF EXISTS sp_DeleteCustomer;
DROP PROCEDURE IF EXISTS sp_GetCustomers;
DROP PROCEDURE IF EXISTS sp_GetCustomerById;

DROP PROCEDURE IF EXISTS sp_AddRoomType;
DROP PROCEDURE IF EXISTS sp_UpdateRoomType;
DROP PROCEDURE IF EXISTS sp_DeleteRoomType;
DROP PROCEDURE IF EXISTS sp_GetRoomTypes;
DROP PROCEDURE IF EXISTS sp_GetRoomTypeById;

DROP PROCEDURE IF EXISTS sp_AddRoom;
DROP PROCEDURE IF EXISTS sp_UpdateRoom;
DROP PROCEDURE IF EXISTS sp_DeleteRoom;
DROP PROCEDURE IF EXISTS sp_GetRooms;
DROP PROCEDURE IF EXISTS sp_GetRoomById;

DROP PROCEDURE IF EXISTS sp_AddReservation;
DROP PROCEDURE IF EXISTS sp_UpdateReservation;
DROP PROCEDURE IF EXISTS sp_DeleteReservation;
DROP PROCEDURE IF EXISTS sp_GetReservations;
DROP PROCEDURE IF EXISTS sp_GetReservationById;
DROP PROCEDURE IF EXISTS sp_CancelReservation;

DROP PROCEDURE IF EXISTS sp_AddPayment;
DROP PROCEDURE IF EXISTS sp_UpdatePayment;
DROP PROCEDURE IF EXISTS sp_DeletePayment;
DROP PROCEDURE IF EXISTS sp_GetPayments;
DROP PROCEDURE IF EXISTS sp_GetPaymentById;
DROP PROCEDURE IF EXISTS sp_GetPaymentsByReservation;

DROP PROCEDURE IF EXISTS sp_AddService;
DROP PROCEDURE IF EXISTS sp_UpdateService;
DROP PROCEDURE IF EXISTS sp_DeleteService;
DROP PROCEDURE IF EXISTS sp_GetServices;
DROP PROCEDURE IF EXISTS sp_GetServiceById;

DROP PROCEDURE IF EXISTS sp_AddReservationService;
DROP PROCEDURE IF EXISTS sp_UpdateReservationService;
DROP PROCEDURE IF EXISTS sp_DeleteReservationService;
DROP PROCEDURE IF EXISTS sp_GetReservationServices;
DROP PROCEDURE IF EXISTS sp_GetReservationServicesByReservation;

DROP PROCEDURE IF EXISTS sp_AddStaff;
DROP PROCEDURE IF EXISTS sp_UpdateStaff;
DROP PROCEDURE IF EXISTS sp_DeleteStaff;
DROP PROCEDURE IF EXISTS sp_GetStaff;
DROP PROCEDURE IF EXISTS sp_GetStaffById;

DROP PROCEDURE IF EXISTS sp_GetDashboardStats;
DROP PROCEDURE IF EXISTS sp_GetCalculatedCost;
DROP PROCEDURE IF EXISTS sp_CheckRoomAvailability;

DROP TABLE IF EXISTS ReservationServices;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Reservations;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Services;
DROP TABLE IF EXISTS Rooms;
DROP TABLE IF EXISTS RoomTypes;
DROP TABLE IF EXISTS Customers;

-- =========================================================================
-- 2. CREATE TABLES
-- =========================================================================

-- 1. Customers Table
CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    passport_no VARCHAR(50) NOT NULL UNIQUE,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. RoomTypes Table
CREATE TABLE RoomTypes (
    room_type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    price_per_night DECIMAL(10, 2) NOT NULL CHECK (price_per_night >= 0),
    capacity INT NOT NULL CHECK (capacity > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Rooms Table
CREATE TABLE Rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10) NOT NULL UNIQUE,
    room_type_id INT NOT NULL,
    floor_number INT NOT NULL,
    room_status VARCHAR(20) NOT NULL DEFAULT 'Available',
    CONSTRAINT fk_room_type FOREIGN KEY (room_type_id) REFERENCES RoomTypes(room_type_id) ON DELETE RESTRICT,
    CONSTRAINT chk_room_status CHECK (room_status IN ('Available', 'Reserved', 'Occupied', 'Maintenance'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Reservations Table
CREATE TABLE Reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    room_id INT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    reservation_status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    total_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (total_price >= 0),
    CONSTRAINT fk_reservation_customer FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT fk_reservation_room FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE RESTRICT,
    CONSTRAINT chk_reservation_status CHECK (reservation_status IN ('Pending', 'Confirmed', 'Cancelled')),
    CONSTRAINT chk_dates CHECK (check_out_date > check_in_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Payments Table
CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_amount DECIMAL(10, 2) NOT NULL CHECK (payment_amount >= 0),
    payment_method VARCHAR(20) NOT NULL,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    CONSTRAINT fk_payment_reservation FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id) ON DELETE CASCADE,
    CONSTRAINT chk_payment_method CHECK (payment_method IN ('Cash', 'Credit Card', 'Bank Transfer')),
    CONSTRAINT chk_payment_status CHECK (payment_status IN ('Pending', 'Completed', 'Failed'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Services Table
CREATE TABLE Services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL UNIQUE,
    service_price DECIMAL(10, 2) NOT NULL CHECK (service_price >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. ReservationServices Table
CREATE TABLE ReservationServices (
    reservation_service_id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    service_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    CONSTRAINT fk_res_service_reservation FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id) ON DELETE CASCADE,
    CONSTRAINT fk_res_service_service FOREIGN KEY (service_id) REFERENCES Services(service_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Staff Table
CREATE TABLE Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    salary DECIMAL(10, 2) NOT NULL CHECK (salary >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================================================
-- 3. INSERT SEED DATA
-- =========================================================================

-- Insert Room Types
INSERT INTO RoomTypes (type_name, price_per_night, capacity) VALUES
('Single Room', 2750.00, 1),
('Double Room', 5450.00, 2),
('Suite', 6500.00, 4);

-- Insert Rooms
INSERT INTO Rooms (room_number, room_type_id, floor_number, room_status) VALUES
('101', 1, 1, 'Available'),
('102', 1, 1, 'Available'),
('201', 2, 2, 'Available'),
('202', 2, 2, 'Available'),
('301', 3, 3, 'Available');

-- Insert Customers
INSERT INTO Customers (first_name, last_name, phone, email, passport_no) VALUES
('Ahmet', 'Yılmaz', '+905551112233', 'ahmet.yilmaz@email.com', 'TR1234567'),
('Mehmet', 'Kaya', '+905554445566', 'mehmet.kaya@email.com', 'TR9876543'),
('Elif', 'Demir', '+905557778899', 'elif.demir@email.com', 'TR5556667');

-- Insert Services
INSERT INTO Services (service_name, service_price) VALUES
('Breakfast', 750.00),
('Laundry', 1250.00),
('Airport Transfer', 700.00);

-- Insert Staff
INSERT INTO Staff (first_name, last_name, position, phone, salary) VALUES
('Can', 'Öztürk', 'Receptionist', '+905553332211', 15000.00),
('Zeynep', 'Şahin', 'Manager', '+905559998877', 28000.00),
('Ali', 'Yıldız', 'Housekeeping', '+905556667788', 12000.00);

-- =========================================================================
-- 4. SQL FUNCTIONS
-- =========================================================================

DELIMITER //

-- Function 1: Calculate total stay duration
CREATE FUNCTION fn_CalculateStayDays(check_in DATE, check_out DATE)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN DATEDIFF(check_out, check_in);
END//

-- Function 2: Calculate reservation total cost based on room price
CREATE FUNCTION fn_CalculateReservationCost(r_id INT, check_in DATE, check_out DATE)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE price DECIMAL(10,2);
    DECLARE days INT;
    
    SELECT rt.price_per_night INTO price
    FROM Rooms r
    JOIN RoomTypes rt ON r.room_type_id = rt.room_type_id
    WHERE r.room_id = r_id;
    
    SET days = fn_CalculateStayDays(check_in, check_out);
    RETURN IFNULL(price * days, 0.00);
END//

DELIMITER ;

-- =========================================================================
-- 5. TRIGGERS
-- =========================================================================

DELIMITER //

-- Trigger 1: Automatically change room status to 'Reserved' after creating reservation
CREATE TRIGGER trg_AfterReservationInsert
AFTER INSERT ON Reservations
FOR EACH ROW
BEGIN
    -- Update room status to Reserved
    UPDATE Rooms
    SET room_status = 'Reserved'
    WHERE room_id = NEW.room_id;
END//

-- Trigger 2: Automatically change room status to 'Available' after reservation cancellation
CREATE TRIGGER trg_AfterReservationUpdate
AFTER UPDATE ON Reservations
FOR EACH ROW
BEGIN
    -- If reservation status changes to Cancelled, set room status to Available
    IF NEW.reservation_status = 'Cancelled' AND OLD.reservation_status != 'Cancelled' THEN
        UPDATE Rooms
        SET room_status = 'Available'
        WHERE room_id = NEW.room_id;
    -- If reservation status changes from Cancelled back to Confirmed or Pending, set it back to Reserved
    ELSEIF NEW.reservation_status IN ('Confirmed', 'Pending') AND OLD.reservation_status = 'Cancelled' THEN
        UPDATE Rooms
        SET room_status = 'Reserved'
        WHERE room_id = NEW.room_id;
    END IF;
END//

DELIMITER ;

-- =========================================================================
-- 6. STORED PROCEDURES (CRUD operations for each table and additional helper SPs)
-- =========================================================================

DELIMITER //

-- -------------------------------------------------------------------------
-- CUSTOMERS PROCEDURES
-- -------------------------------------------------------------------------
CREATE PROCEDURE sp_AddCustomer(
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_phone VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_passport_no VARCHAR(50)
)
BEGIN
    INSERT INTO Customers (first_name, last_name, phone, email, passport_no)
    VALUES (p_first_name, p_last_name, p_phone, p_email, p_passport_no);
    SELECT LAST_INSERT_ID() AS customer_id;
END//

CREATE PROCEDURE sp_UpdateCustomer(
    IN p_customer_id INT,
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_phone VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_passport_no VARCHAR(50)
)
BEGIN
    UPDATE Customers
    SET first_name = p_first_name,
        last_name = p_last_name,
        phone = p_phone,
        email = p_email,
        passport_no = p_passport_no
    WHERE customer_id = p_customer_id;
END//

CREATE PROCEDURE sp_DeleteCustomer(
    IN p_customer_id INT
)
BEGIN
    DELETE FROM Customers WHERE customer_id = p_customer_id;
END//

CREATE PROCEDURE sp_GetCustomers()
BEGIN
    SELECT customer_id, first_name, last_name, phone, email, passport_no, registration_date 
    FROM Customers
    ORDER BY customer_id DESC;
END//

CREATE PROCEDURE sp_GetCustomerById(
    IN p_customer_id INT
)
BEGIN
    SELECT customer_id, first_name, last_name, phone, email, passport_no, registration_date 
    FROM Customers
    WHERE customer_id = p_customer_id;
END//


-- -------------------------------------------------------------------------
-- ROOMTYPES PROCEDURES
-- -------------------------------------------------------------------------
CREATE PROCEDURE sp_AddRoomType(
    IN p_type_name VARCHAR(50),
    IN p_price_per_night DECIMAL(10, 2),
    IN p_capacity INT
)
BEGIN
    INSERT INTO RoomTypes (type_name, price_per_night, capacity)
    VALUES (p_type_name, p_price_per_night, p_capacity);
    SELECT LAST_INSERT_ID() AS room_type_id;
END//

CREATE PROCEDURE sp_UpdateRoomType(
    IN p_room_type_id INT,
    IN p_type_name VARCHAR(50),
    IN p_price_per_night DECIMAL(10, 2),
    IN p_capacity INT
)
BEGIN
    UPDATE RoomTypes
    SET type_name = p_type_name,
        price_per_night = p_price_per_night,
        capacity = p_capacity
    WHERE room_type_id = p_room_type_id;
END//

CREATE PROCEDURE sp_DeleteRoomType(
    IN p_room_type_id INT
)
BEGIN
    DELETE FROM RoomTypes WHERE room_type_id = p_room_type_id;
END//

CREATE PROCEDURE sp_GetRoomTypes()
BEGIN
    SELECT room_type_id, type_name, price_per_night, capacity 
    FROM RoomTypes
    ORDER BY room_type_id ASC;
END//

CREATE PROCEDURE sp_GetRoomTypeById(
    IN p_room_type_id INT
)
BEGIN
    SELECT room_type_id, type_name, price_per_night, capacity 
    FROM RoomTypes
    WHERE room_type_id = p_room_type_id;
END//


-- -------------------------------------------------------------------------
-- ROOMS PROCEDURES
-- -------------------------------------------------------------------------
CREATE PROCEDURE sp_AddRoom(
    IN p_room_number VARCHAR(10),
    IN p_room_type_id INT,
    IN p_floor_number INT,
    IN p_room_status VARCHAR(20)
)
BEGIN
    INSERT INTO Rooms (room_number, room_type_id, floor_number, room_status)
    VALUES (p_room_number, p_room_type_id, p_floor_number, p_room_status);
    SELECT LAST_INSERT_ID() AS room_id;
END//

CREATE PROCEDURE sp_UpdateRoom(
    IN p_room_id INT,
    IN p_room_number VARCHAR(10),
    IN p_room_type_id INT,
    IN p_floor_number INT,
    IN p_room_status VARCHAR(20)
)
BEGIN
    UPDATE Rooms
    SET room_number = p_room_number,
        room_type_id = p_room_type_id,
        floor_number = p_floor_number,
        room_status = p_room_status
    WHERE room_id = p_room_id;
END//

CREATE PROCEDURE sp_DeleteRoom(
    IN p_room_id INT
)
BEGIN
    DELETE FROM Rooms WHERE room_id = p_room_id;
END//

CREATE PROCEDURE sp_GetRooms()
BEGIN
    SELECT r.room_id, r.room_number, r.room_type_id, rt.type_name, rt.price_per_night, r.floor_number, r.room_status 
    FROM Rooms r
    JOIN RoomTypes rt ON r.room_type_id = rt.room_type_id
    ORDER BY r.room_number ASC;
END//

CREATE PROCEDURE sp_GetRoomById(
    IN p_room_id INT
)
BEGIN
    SELECT r.room_id, r.room_number, r.room_type_id, rt.type_name, rt.price_per_night, r.floor_number, r.room_status 
    FROM Rooms r
    JOIN RoomTypes rt ON r.room_type_id = rt.room_type_id
    WHERE r.room_id = p_room_id;
END//


-- -------------------------------------------------------------------------
-- RESERVATIONS PROCEDURES
-- -------------------------------------------------------------------------
CREATE PROCEDURE sp_AddReservation(
    IN p_customer_id INT,
    IN p_room_id INT,
    IN p_check_in_date DATE,
    IN p_check_out_date DATE,
    IN p_reservation_status VARCHAR(20),
    IN p_total_price DECIMAL(10, 2)
)
BEGIN
    INSERT INTO Reservations (customer_id, room_id, check_in_date, check_out_date, reservation_status, total_price)
    VALUES (p_customer_id, p_room_id, p_check_in_date, p_check_out_date, p_reservation_status, p_total_price);
    SELECT LAST_INSERT_ID() AS reservation_id;
END//

CREATE PROCEDURE sp_UpdateReservation(
    IN p_reservation_id INT,
    IN p_customer_id INT,
    IN p_room_id INT,
    IN p_check_in_date DATE,
    IN p_check_out_date DATE,
    IN p_reservation_status VARCHAR(20),
    IN p_total_price DECIMAL(10, 2)
)
BEGIN
    UPDATE Reservations
    SET customer_id = p_customer_id,
        room_id = p_room_id,
        check_in_date = p_check_in_date,
        check_out_date = p_check_out_date,
        reservation_status = p_reservation_status,
        total_price = p_total_price
    WHERE reservation_id = p_reservation_id;
END//

CREATE PROCEDURE sp_DeleteReservation(
    IN p_reservation_id INT
)
BEGIN
    -- Retrieve the room_id before deleting so we can free the room
    DECLARE r_id INT;
    SELECT room_id INTO r_id FROM Reservations WHERE reservation_id = p_reservation_id;
    
    DELETE FROM Reservations WHERE reservation_id = p_reservation_id;
    
    -- Change the status of the room back to Available if no other active reservation occupies it
    UPDATE Rooms SET room_status = 'Available' WHERE room_id = r_id;
END//

CREATE PROCEDURE sp_GetReservations()
BEGIN
    SELECT res.reservation_id, res.customer_id, c.first_name, c.last_name, c.phone, c.email,
           res.room_id, r.room_number, rt.type_name AS room_type_name,
           res.check_in_date, res.check_out_date, res.reservation_status, res.total_price 
    FROM Reservations res
    JOIN Customers c ON res.customer_id = c.customer_id
    JOIN Rooms r ON res.room_id = r.room_id
    JOIN RoomTypes rt ON r.room_type_id = rt.room_type_id
    ORDER BY res.reservation_id DESC;
END//

CREATE PROCEDURE sp_GetReservationById(
    IN p_reservation_id INT
)
BEGIN
    SELECT res.reservation_id, res.customer_id, c.first_name, c.last_name, c.phone, c.email,
           res.room_id, r.room_number, rt.type_name AS room_type_name,
           res.check_in_date, res.check_out_date, res.reservation_status, res.total_price 
    FROM Reservations res
    JOIN Customers c ON res.customer_id = c.customer_id
    JOIN Rooms r ON res.room_id = r.room_id
    JOIN RoomTypes rt ON r.room_type_id = rt.room_type_id
    WHERE res.reservation_id = p_reservation_id;
END//

CREATE PROCEDURE sp_CancelReservation(
    IN p_reservation_id INT
)
BEGIN
    UPDATE Reservations
    SET reservation_status = 'Cancelled'
    WHERE reservation_id = p_reservation_id;
END//


-- -------------------------------------------------------------------------
-- PAYMENTS PROCEDURES
-- -------------------------------------------------------------------------
CREATE PROCEDURE sp_AddPayment(
    IN p_reservation_id INT,
    IN p_payment_amount DECIMAL(10, 2),
    IN p_payment_method VARCHAR(20),
    IN p_payment_status VARCHAR(20)
)
BEGIN
    INSERT INTO Payments (reservation_id, payment_amount, payment_method, payment_status)
    VALUES (p_reservation_id, p_payment_amount, p_payment_method, p_payment_status);
    SELECT LAST_INSERT_ID() AS payment_id;
END//

CREATE PROCEDURE sp_UpdatePayment(
    IN p_payment_id INT,
    IN p_reservation_id INT,
    IN p_payment_amount DECIMAL(10, 2),
    IN p_payment_method VARCHAR(20),
    IN p_payment_status VARCHAR(20)
)
BEGIN
    UPDATE Payments
    SET reservation_id = p_reservation_id,
        payment_amount = p_payment_amount,
        payment_method = p_payment_method,
        payment_status = p_payment_status
    WHERE payment_id = p_payment_id;
END//

CREATE PROCEDURE sp_DeletePayment(
    IN p_payment_id INT
)
BEGIN
    DELETE FROM Payments WHERE payment_id = p_payment_id;
END//

CREATE PROCEDURE sp_GetPayments()
BEGIN
    SELECT p.payment_id, p.reservation_id, c.first_name, c.last_name, r.room_number,
           p.payment_date, p.payment_amount, p.payment_method, p.payment_status 
    FROM Payments p
    JOIN Reservations res ON p.reservation_id = res.reservation_id
    JOIN Customers c ON res.customer_id = c.customer_id
    JOIN Rooms r ON res.room_id = r.room_id
    ORDER BY p.payment_id DESC;
END//

CREATE PROCEDURE sp_GetPaymentById(
    IN p_payment_id INT
)
BEGIN
    SELECT p.payment_id, p.reservation_id, c.first_name, c.last_name, r.room_number,
           p.payment_date, p.payment_amount, p.payment_method, p.payment_status 
    FROM Payments p
    JOIN Reservations res ON p.reservation_id = res.reservation_id
    JOIN Customers c ON res.customer_id = c.customer_id
    JOIN Rooms r ON res.room_id = r.room_id
    WHERE p.payment_id = p_payment_id;
END//

CREATE PROCEDURE sp_GetPaymentsByReservation(
    IN p_reservation_id INT
)
BEGIN
    SELECT payment_id, reservation_id, payment_date, payment_amount, payment_method, payment_status 
    FROM Payments
    WHERE reservation_id = p_reservation_id
    ORDER BY payment_date DESC;
END//


-- -------------------------------------------------------------------------
-- SERVICES PROCEDURES
-- -------------------------------------------------------------------------
CREATE PROCEDURE sp_AddService(
    IN p_service_name VARCHAR(50),
    IN p_service_price DECIMAL(10, 2)
)
BEGIN
    INSERT INTO Services (service_name, service_price)
    VALUES (p_service_name, p_service_price);
    SELECT LAST_INSERT_ID() AS service_id;
END//

CREATE PROCEDURE sp_UpdateService(
    IN p_service_id INT,
    IN p_service_name VARCHAR(50),
    IN p_service_price DECIMAL(10, 2)
)
BEGIN
    UPDATE Services
    SET service_name = p_service_name,
        service_price = p_service_price
    WHERE service_id = p_service_id;
END//

CREATE PROCEDURE sp_DeleteService(
    IN p_service_id INT
)
BEGIN
    DELETE FROM Services WHERE service_id = p_service_id;
END//

CREATE PROCEDURE sp_GetServices()
BEGIN
    SELECT service_id, service_name, service_price 
    FROM Services
    ORDER BY service_id ASC;
END//

CREATE PROCEDURE sp_GetServiceById(
    IN p_service_id INT
)
BEGIN
    SELECT service_id, service_name, service_price 
    FROM Services
    WHERE service_id = p_service_id;
END//


-- -------------------------------------------------------------------------
-- RESERVATION SERVICES PROCEDURES
-- -------------------------------------------------------------------------
CREATE PROCEDURE sp_AddReservationService(
    IN p_reservation_id INT,
    IN p_service_id INT,
    IN p_quantity INT
)
BEGIN
    -- Insert or update if service is already added for this reservation
    DECLARE existing_id INT DEFAULT NULL;
    DECLARE service_price_val DECIMAL(10,2);
    
    SELECT reservation_service_id INTO existing_id 
    FROM ReservationServices 
    WHERE reservation_id = p_reservation_id AND service_id = p_service_id;
    
    IF existing_id IS NOT NULL THEN
        UPDATE ReservationServices 
        SET quantity = quantity + p_quantity 
        WHERE reservation_service_id = existing_id;
    ELSE
        INSERT INTO ReservationServices (reservation_id, service_id, quantity)
        VALUES (p_reservation_id, p_service_id, p_quantity);
    END IF;
    
    -- Recalculate and update the reservation total price
    SELECT service_price INTO service_price_val FROM Services WHERE service_id = p_service_id;
    UPDATE Reservations 
    SET total_price = total_price + (service_price_val * p_quantity)
    WHERE reservation_id = p_reservation_id;
END//

CREATE PROCEDURE sp_UpdateReservationService(
    IN p_reservation_service_id INT,
    IN p_reservation_id INT,
    IN p_service_id INT,
    IN p_quantity INT
)
BEGIN
    -- Recalculate entire reservation total price before updating
    DECLARE diff_qty INT;
    DECLARE old_qty INT;
    DECLARE s_price DECIMAL(10,2);
    
    SELECT quantity INTO old_qty FROM ReservationServices WHERE reservation_service_id = p_reservation_service_id;
    SELECT service_price INTO s_price FROM Services WHERE service_id = p_service_id;
    
    SET diff_qty = p_quantity - old_qty;
    
    UPDATE ReservationServices
    SET reservation_id = p_reservation_id,
        service_id = p_service_id,
        quantity = p_quantity
    WHERE reservation_service_id = p_reservation_service_id;
    
    UPDATE Reservations 
    SET total_price = total_price + (s_price * diff_qty)
    WHERE reservation_id = p_reservation_id;
END//

CREATE PROCEDURE sp_DeleteReservationService(
    IN p_reservation_service_id INT
)
BEGIN
    DECLARE res_id INT;
    DECLARE s_id INT;
    DECLARE qty INT;
    DECLARE s_price DECIMAL(10,2);
    
    SELECT reservation_id, service_id, quantity INTO res_id, s_id, qty 
    FROM ReservationServices 
    WHERE reservation_service_id = p_reservation_service_id;
    
    SELECT service_price INTO s_price FROM Services WHERE service_id = s_id;
    
    DELETE FROM ReservationServices WHERE reservation_service_id = p_reservation_service_id;
    
    -- Deduct from reservation price
    UPDATE Reservations 
    SET total_price = total_price - (s_price * qty)
    WHERE reservation_id = res_id;
END//

CREATE PROCEDURE sp_GetReservationServices()
BEGIN
    SELECT rs.reservation_service_id, rs.reservation_id, rs.service_id, s.service_name, s.service_price, rs.quantity 
    FROM ReservationServices rs
    JOIN Services s ON rs.service_id = s.service_id
    ORDER BY rs.reservation_service_id DESC;
END//

CREATE PROCEDURE sp_GetReservationServicesByReservation(
    IN p_reservation_id INT
)
BEGIN
    SELECT rs.reservation_service_id, rs.reservation_id, rs.service_id, s.service_name, s.service_price, rs.quantity 
    FROM ReservationServices rs
    JOIN Services s ON rs.service_id = s.service_id
    WHERE rs.reservation_id = p_reservation_id
    ORDER BY rs.reservation_service_id ASC;
END//


-- -------------------------------------------------------------------------
-- STAFF PROCEDURES
-- -------------------------------------------------------------------------
CREATE PROCEDURE sp_AddStaff(
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_position VARCHAR(50),
    IN p_phone VARCHAR(20),
    IN p_salary DECIMAL(10, 2)
)
BEGIN
    INSERT INTO Staff (first_name, last_name, position, phone, salary)
    VALUES (p_first_name, p_last_name, p_position, p_phone, p_salary);
    SELECT LAST_INSERT_ID() AS staff_id;
END//

CREATE PROCEDURE sp_UpdateStaff(
    IN p_staff_id INT,
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_position VARCHAR(50),
    IN p_phone VARCHAR(20),
    IN p_salary DECIMAL(10, 2)
)
BEGIN
    UPDATE Staff
    SET first_name = p_first_name,
        last_name = p_last_name,
        position = p_position,
        phone = p_phone,
        salary = p_salary
    WHERE staff_id = p_staff_id;
END//

CREATE PROCEDURE sp_DeleteStaff(
    IN p_staff_id INT
)
BEGIN
    DELETE FROM Staff WHERE staff_id = p_staff_id;
END//

CREATE PROCEDURE sp_GetStaff()
BEGIN
    SELECT staff_id, first_name, last_name, position, phone, salary 
    FROM Staff
    ORDER BY staff_id DESC;
END//

CREATE PROCEDURE sp_GetStaffById(
    IN p_staff_id INT
)
BEGIN
    SELECT staff_id, first_name, last_name, position, phone, salary 
    FROM Staff
    WHERE staff_id = p_staff_id;
END//


-- -------------------------------------------------------------------------
-- DASHBOARD / STATISTICS PROCEDURES
-- -------------------------------------------------------------------------
CREATE PROCEDURE sp_GetDashboardStats()
BEGIN
    DECLARE total_cust INT;
    DECLARE total_rms INT;
    DECLARE total_res INT;
    DECLARE avail_rms INT;
    DECLARE total_rev DECIMAL(10,2);
    
    SELECT COUNT(*) INTO total_cust FROM Customers;
    SELECT COUNT(*) INTO total_rms FROM Rooms;
    SELECT COUNT(*) INTO total_res FROM Reservations;
    SELECT COUNT(*) INTO avail_rms FROM Rooms WHERE room_status = 'Available';
    
    -- Total Revenue is calculated from successfully Completed Payments
    SELECT IFNULL(SUM(payment_amount), 0.00) INTO total_rev FROM Payments WHERE payment_status = 'Completed';
    
    SELECT total_cust AS TotalCustomers, 
           total_rms AS TotalRooms, 
           total_res AS TotalReservations, 
           avail_rms AS AvailableRooms, 
           total_rev AS TotalRevenue;
END//

-- Helper procedure to calculate cost using functions
CREATE PROCEDURE sp_GetCalculatedCost(
    IN p_room_id INT,
    IN p_check_in DATE,
    IN p_check_out DATE
)
BEGIN
    SELECT fn_CalculateStayDays(p_check_in, p_check_out) AS stay_days,
           fn_CalculateReservationCost(p_room_id, p_check_in, p_check_out) AS total_cost;
END//

-- Helper procedure to check room availability (prevent double-booking)
CREATE PROCEDURE sp_CheckRoomAvailability(
    IN p_room_id INT,
    IN p_check_in DATE,
    IN p_check_out DATE
)
BEGIN
    SELECT COUNT(*) AS active_reservations
    FROM Reservations
    WHERE room_id = p_room_id
      AND reservation_status != 'Cancelled'
      AND (
          (p_check_in >= check_in_date AND p_check_in < check_out_date)
          OR (p_check_out > check_in_date AND p_check_out <= check_out_date)
          OR (check_in_date >= p_check_in AND check_in_date < p_check_out)
      );
END//

DELIMITER ;
