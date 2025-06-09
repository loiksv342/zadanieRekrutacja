
CREATE DATABASE fleet_management;
USE fleet_management;

-- Table Vehicles
CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registration_number VARCHAR(10) NOT NULL UNIQUE,
    brand VARCHAR(30) NOT NULL,
    model VARCHAR(30) NOT NULL,
    tech_inspection_date DATE NOT NULL,
    tech_inspection_expiry DATE NOT NULL,
    oc_insurance_expiry DATE NOT NULL,
    last_service_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Table notifications
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    notification_type ENUM('TECH_INSPECTION', 'OC_INSURANCE') NOT NULL,
    notification_date DATE NOT NULL,
    days_prior INT NOT NULL,
    is_sent BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- Table recipients
CREATE TABLE recipients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(15)
);

-- Inserting example data
INSERT INTO vehicles (registration_number, brand, model, tech_inspection_date, tech_inspection_expiry, oc_insurance_expiry)
VALUES
    ('WWA12345', 'Toyota', 'Corolla', '2023-06-01', '2024-06-01', '2024-05-15'),
    ('KR789XYZ', 'Ford', 'Focus', '2023-09-15', '2024-09-15', '2024-08-30'),
    ('GD5678AB', 'Volkswagen', 'Golf', '2023-12-10', '2024-12-10', '2024-11-25');

INSERT INTO recipients (email, phone)
VALUES ('fleet.manager@example.com', '+48111222333');