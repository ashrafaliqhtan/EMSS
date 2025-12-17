CREATE TABLE requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    city VARCHAR(255),
    latitude DOUBLE,
    longitude DOUBLE
);



INSERT INTO requests (customer_name, city, latitude, longitude)
VALUES
('أحمد محمد', 'الرياض', 24.7136, 46.6753),
('سارة علي', 'مكة المكرمة', 21.3891, 39.8579);