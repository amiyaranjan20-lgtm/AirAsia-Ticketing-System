PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS FlightCrew;
DROP TABLE IF EXISTS Ticket;
DROP TABLE IF EXISTS Flight;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Aircraft;
DROP TABLE IF EXISTS Airport;


PRAGMA foreign_keys = ON;



CREATE TABLE Airport (
    Airport_code TEXT NOT NULL PRIMARY KEY,
    Name TEXT NOT NULL,
    City TEXT NOT NULL,
    Country TEXT NOT NULL
);

CREATE TABLE Aircraft (
    Aircraft_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    Capacity INTEGER NOT NULL CHECK (Capacity > 0)
);

CREATE TABLE Employee (
    Employee_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    First_name TEXT NOT NULL,
    Last_name TEXT NOT NULL,
    Job_title TEXT NOT NULL
);

CREATE TABLE Customer (
    Customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    First_name TEXT,
    Last_name TEXT,
    Gender TEXT,
    Dob TEXT,
    Citizenship TEXT,
    Phone TEXT,
    email TEXT,
    Passport_number TEXT,
    Passport_expiry TEXT
);

CREATE TABLE Flight (
    Flight_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Airport_from TEXT NOT NULL,
    Airport_to TEXT NOT NULL,
    Aircraft_Id INTEGER NOT NULL,
    Departure_date TEXT NOT NULL,
    Departure_time TEXT NOT NULL,
    Departure_gate TEXT,
    Arrival_gate TEXT,
    Duration INTEGER NOT NULL CHECK (Duration > 0),
    Employee_Id INTEGER NOT NULL,
    FOREIGN KEY (Airport_from) REFERENCES Airport(Airport_code),
    FOREIGN KEY (Airport_to) REFERENCES Airport(Airport_code),
    FOREIGN KEY (Aircraft_Id) REFERENCES Aircraft(Aircraft_Id),
    FOREIGN KEY (Employee_Id) REFERENCES Employee(Employee_Id),
    CHECK (Airport_from <> Airport_to)
);

CREATE TABLE FlightCrew
(
    Flight_Id INTEGER NOT NULL,
    Employee_Id INTEGER NOT NULL,
    Role TEXT,
    PRIMARY KEY (Flight_Id, Employee_Id),

    FOREIGN KEY (Flight_Id) REFERENCES Flight(Flight_Id),
    FOREIGN KEY (Employee_Id) REFERENCES Employee(Employee_Id)
);



CREATE TABLE Ticket (
    Ticket_number INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Customer_Id INTEGER NOT NULL,
    Flight_Id INTEGER NOT NULL,
    Cost REAL NOT NULL CHECK (Cost >= 0),
    purchaseDate TEXT NOT NULL,
    FOREIGN KEY (Customer_Id) REFERENCES Customer(Customer_id),
    FOREIGN KEY (Flight_Id) REFERENCES Flight(Flight_Id),
    UNIQUE (Customer_Id, Flight_Id)
);
