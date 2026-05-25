CREATE DATABASE IF NOT EXISTS vehicle_service_db;
USE vehicle_service_db;

CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(30),
    Last_Name VARCHAR(30),
    Phone VARCHAR(15),
    Email VARCHAR(80),
    Address VARCHAR(100)
);

CREATE TABLE Vehicle (
    VehicleID INT AUTO_INCREMENT PRIMARY KEY,
    Reg_No VARCHAR(20) UNIQUE,
    Brand VARCHAR(50),
    Model VARCHAR(50),
    Year INT,
    FuelType VARCHAR(20),
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE Mechanic (
    MechanicID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    Speciality VARCHAR(60),
    Experience INT,
    Phone VARCHAR(15)
);

CREATE TABLE Service (
    ServiceID INT AUTO_INCREMENT PRIMARY KEY,
    VehicleID INT,
    MechanicID INT,
    Service_Date DATE,
    Mileage INT,
    Service_Type VARCHAR(60),
    Status VARCHAR(20),
    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID),
    FOREIGN KEY (MechanicID) REFERENCES Mechanic(MechanicID)
);

CREATE TABLE Service_Details (
    DetailID INT AUTO_INCREMENT PRIMARY KEY,
    ServiceID INT,
    Parts_Changed VARCHAR(150),
    Labour_Cost DECIMAL(10,2),
    Parts_Cost DECIMAL(10,2),
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID)
);

CREATE TABLE Bill (
    BillID INT AUTO_INCREMENT PRIMARY KEY,
    ServiceID INT UNIQUE,
    Amount DECIMAL(10,2),
    Bill_Date DATE,
    Payment_Mode VARCHAR(20),
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID)
);

INSERT INTO Customer VALUES
(1,'Rohith','Kumar','9876543210','rohith@email.com','Bangalore'),
(2,'Arjun','R','9123456780','arjun@email.com','Mysore'),
(3,'Sneha','P','9988776655','sneha@email.com','Chennai'),
(4,'Kiran','S','9012345678','kiran@email.com','Tumkur'),
(5,'Meera','Nair','9871234560','meera@email.com','Kochi');

INSERT INTO Vehicle VALUES
(1,'KA01AB1234','Maruti','Swift',2021,'Petrol',1),
(2,'KA05CD5678','Hyundai','i20',2020,'Petrol',2),
(3,'TN10EF4321','Honda','City',2019,'Petrol',3),
(4,'KA03GH8888','Toyota','Innova',2022,'Diesel',4),
(5,'KL07IJ2222','Maruti','Baleno',2023,'Petrol',5),
(6,'TN22KL9900','Hyundai','Creta',2021,'Diesel',1);

INSERT INTO Mechanic VALUES
(1,'Ramesh','Engine Specialist',5,'9001112233'),
(2,'Suresh','Electricals & AC',7,'9011122233'),
(3,'Mahesh','Suspension & Tyres',4,'9022233344'),
(4,'Dinesh','General Maintenance',3,'9033344455');

INSERT INTO Service VALUES
(1,1,1,'2026-04-01',15000,'General Service','Completed'),
(2,2,2,'2026-04-03',20000,'Oil Change','Completed'),
(3,3,1,'2026-04-05',18000,'Full Service','Completed'),
(4,4,3,'2026-04-10',32000,'Suspension Check','Completed'),
(5,5,4,'2026-04-18',9000,'General Service','In Progress'),
(6,6,2,'2026-04-25',22000,'AC Service','Pending');

INSERT INTO Service_Details VALUES
(1,1,'Oil Filter, Air Filter',500.00,1000.00),
(2,2,'Engine Oil 5L',300.00,900.00),
(3,3,'Spark Plugs, Brake Pads',800.00,2200.00),
(4,4,'Shock Absorbers Rear',700.00,3500.00),
(5,5,'Coolant, Wipers',400.00,600.00),
(6,6,'AC Gas Refill',500.00,1200.00);

INSERT INTO Bill VALUES
(1,1,1500.00,'2026-04-01','Cash'),
(2,2,1200.00,'2026-04-03','UPI'),
(3,3,3000.00,'2026-04-05','Card'),
(4,4,4200.00,'2026-04-10','UPI'),
(5,5,1000.00,'2026-04-18','Cash'),
(6,6,1700.00,'2026-04-25','Card');