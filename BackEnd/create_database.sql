-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS network_analysis;

-- Switch to the newly created database
USE network_analysis;

-- Create a table to store high traffic IP addresses
CREATE TABLE IF NOT EXISTS high_traffic_ips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ipv4_src_addr VARCHAR(45) NOT NULL,
    total_in_bytes BIGINT NOT NULL,
    total_out_bytes BIGINT NOT NULL,
    total_in_pkts BIGINT NOT NULL,
    total_out_pkts BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table to store protocol usage analysis
CREATE TABLE IF NOT EXISTS protocol_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    protocol VARCHAR(10) NOT NULL,
    count INT NOT NULL,
    total_in_bytes BIGINT NOT NULL,
    total_out_bytes BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table to store detected anomalies
CREATE TABLE IF NOT EXISTS anomalies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ipv4_src_addr VARCHAR(45) NOT NULL,
    in_bytes BIGINT NOT NULL,
    out_bytes BIGINT NOT NULL,
    anomaly INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);