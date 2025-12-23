-- Enable pgcrypto for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================
-- 1. Tables Creation
-- ============================================

-- Table: phone_numbers
CREATE TABLE phone_numbers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: otps
CREATE TABLE otps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number_id UUID REFERENCES phone_numbers(id) ON DELETE CASCADE,
    otp_code CHAR(5) NOT NULL,
    is_valid BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Table: contacts
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    type VARCHAR(50) NOT NULL
);

-- Table: prospects
CREATE TABLE prospects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entreprise VARCHAR(255) NOT NULL,
    adresse VARCHAR(255),
    wilaya VARCHAR(100),
    commune VARCHAR(100),
    phone_number VARCHAR(50),
    email VARCHAR(255),
    categorie VARCHAR(100),
    forme_legale VARCHAR(100),
    secteur VARCHAR(100),
    sous_secteur VARCHAR(100),
    nif VARCHAR(50),
    registre_commerce VARCHAR(50),
    status VARCHAR(50) NOT NULL
);

-- ============================================
-- 2. Seed Data
-- ============================================

-- Seed: phone_numbers
INSERT INTO phone_numbers (phone_number) VALUES
('0661123456'),
('0550123456'),
('0770123456'),
('0662987654'),
('0551987654');

-- Seed: otps
-- Using subqueries to link to the created phone numbers dynamically
INSERT INTO otps (phone_number_id, otp_code, expires_at)
SELECT id, '12345', NOW() + INTERVAL '10 minutes' FROM phone_numbers WHERE phone_number = '0661123456';

INSERT INTO otps (phone_number_id, otp_code, expires_at)
SELECT id, '67890', NOW() + INTERVAL '10 minutes' FROM phone_numbers WHERE phone_number = '0550123456';

INSERT INTO otps (phone_number_id, otp_code, expires_at)
SELECT id, '11223', NOW() + INTERVAL '10 minutes' FROM phone_numbers WHERE phone_number = '0770123456';

INSERT INTO otps (phone_number_id, otp_code, expires_at)
SELECT id, '44556', NOW() + INTERVAL '10 minutes' FROM phone_numbers WHERE phone_number = '0662987654';

INSERT INTO otps (phone_number_id, otp_code, expires_at)
SELECT id, '77889', NOW() + INTERVAL '10 minutes' FROM phone_numbers WHERE phone_number = '0551987654';

-- Seed: contacts
INSERT INTO contacts (name, phone_number, email, company, type) VALUES
('Ahmed Benali', '0661123456', 'ahmed.benali@example.com', 'Tech Solutions', 'Client'),
('Sarah Amrani', '0550123456', 'sarah.amrani@example.com', 'Design Co', 'Prospect'),
('Mohamed Khelif', '0770123456', 'mohamed.khelif@example.com', 'BuildIt', 'Partner'),
('Fatima Zohra', '0662987654', 'fatima.z@example.com', 'SoftDev', 'Client'),
('Yacine Brahimi', '0551987654', 'yacine.b@example.com', NULL, 'Lead');

-- Seed: prospects
INSERT INTO prospects (entreprise, adresse, wilaya, commune, phone_number, email, categorie, forme_legale, secteur, sous_secteur, nif, registre_commerce, status) VALUES
('Global Tech', '123 Rue de la Liberté', 'Alger', 'Alger Centre', '021234567', 'contact@globaltech.dz', 'B2B', 'SARL', 'Technology', 'Software', '000111222333444', '16/00-1234567B12', 'New'),
('Eco Distrib', '45 Ave des Martyrs', 'Oran', 'Es Senia', '041987654', 'info@ecodistrib.dz', 'Retail', 'EURL', 'Commerce', 'Distribution', '999888777666555', '31/00-7654321A11', 'Contacted'),
('Build Smart', '88 Bd Boumedienne', 'Constantine', 'El Khroub', '031555666', 'sales@buildsmart.dz', 'Construction', 'SPA', 'BTP', 'Gros Oeuvre', '555444333222111', '25/00-1122334C22', 'Negotiation'),
('Agro Food', 'Zone Industrielle', 'Blida', 'Beni Mered', '025444333', 'contact@agrofood.dz', 'Industry', 'SARL', 'Agriculture', 'Transformation', '111222333444555', '09/00-9988776D33', 'Converted'),
('Media Pro', '10 Rue Didouche', 'Annaba', 'Annaba', '038111222', 'hello@mediapro.dz', 'Services', 'EURL', 'Communication', 'Marketing', '777666555444333', '23/00-5544332E44', 'Lost');
