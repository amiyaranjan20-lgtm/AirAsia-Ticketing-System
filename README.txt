# AirAsia Ticketing System

## Introduction

How can Python and a relational database be used to simulate the core operations of an airline ticketing system?

This repository contains the complete development of the **AirAsia Ticketing System**, a command-line airline management application built using **Python and SQLite**. The system integrates database management, ticket booking, dynamic pricing, crew allocation, CSV data import, and operational reporting within one menu-driven application.

---

## 1. Business Context and Objective

Airline operations require coordinated management of airports, aircraft, employees, customers, flights, bookings, and crew assignments. Managing these activities through disconnected files or manual processes can result in:

- Duplicate customer bookings
- Overbooking beyond aircraft capacity
- Inconsistent flight and employee records
- Difficulty tracking passengers and flight revenue
- Inefficient crew assignment and reporting

The guiding business question for this project is:

> How can Python and SQLite be used to create a reliable, structured, and user-friendly airline ticketing and management system?

The main objectives of this project are to:

- Centralize airline operational data in a relational database
- Implement complete CRUD functionality for major airline entities
- Support ticket booking, cancellation, and rebooking
- Enforce seat-capacity and duplicate-booking rules
- Calculate ticket prices using dynamic pricing logic
- Automatically allocate employees to flights
- Generate operational and management reports
- Provide a simple command-line interface for system users

---

## 2. System Development Overview

The project follows a structured development approach that combines object-oriented programming, relational database design, file handling, and business-rule validation.

### 2.1 Database Design

The system uses SQLite as its relational database and includes seven major tables:

1. Airport
2. Aircraft
3. Employee
4. Customer
5. Flight
6. Ticket
7. FlightCrew

Primary keys and foreign keys connect these tables and maintain valid relationships between customers, flights, aircraft, employees, and ticket records.

The database includes integrity controls such as:

- Primary and foreign key constraints
- Aircraft-capacity validation
- Flight-duration validation
- Prevention of identical origin and destination airports
- Duplicate customer-flight booking prevention
- Valid relationships between tickets, customers, and flights

### 2.2 Object-Oriented Programming Design

The application follows an object-oriented structure in which each major entity is represented by a Python class.

The main classes include:

- `ProjectDB`
- `Airport`
- `Aircraft`
- `Employee`
- `Customer`
- `Flight`
- `Ticket`
- `Report`
- `CSVImporter`
- `CrewAllocator`
- `InputHelper`
- `AirAsiaProject`

Each class is responsible for specific operations, while the `AirAsiaProject` class controls the main menu and user interaction.

This structure improves:

- Code readability
- Modularity
- Reusability
- Maintainability
- Debugging efficiency

### 2.3 CSV Data Import

The application uses CSV files to populate the database with sample records.

The imported datasets include:

- Airports
- Aircraft
- Employees
- Customers
- Flights

The `CSVImporter` class reads the files, validates the values, cleans the data, and inserts the records into the SQLite database.

This process allows the system to be initialized quickly without manually entering each record.

### 2.4 Interactive Menu System

The application uses a command-line menu that guides users through the available operations.

The main menu includes:

1. Airport Management
2. Aircraft Management
3. Employee Management
4. Customer Management
5. Flight Management
6. Ticket Management
7. Flight Sales Report
8. Employee Flight Report
9. Passenger Manifest
10. Flight Crew Report
11. Reset Database
12. Import Sample CSV Data
0. Exit System

Each management section provides options to view, search, add, update, and delete records.

---

## 3. Core System Features

### 3.1 CRUD Operations

The system supports complete Create, Read, Update, and Delete operations for major airline records.

#### Airport Management

Users can manage:

- Airport codes
- Airport names
- Cities
- Countries

#### Aircraft Management

Users can manage:

- Aircraft types
- Aircraft seating capacities

#### Employee Management

Users can manage records for:

- Pilots
- Cabin crew
- Mechanics
- Ground staff

#### Customer Management

Users can manage customer profiles used during the ticket-booking process.

#### Flight Management

Users can create and manage flight schedules, routes, aircraft assignments, departure information, and employee assignments.

#### Ticket Management

Users can:

- Purchase tickets
- Search for tickets
- View bookings
- Update bookings
- Cancel tickets
- Rebook tickets

---

## 4. Flight Search and Booking Workflow

### 4.1 Flight Search

Users can search for flights by entering:

- Departure airport
- Destination airport
- Optional departure date

The system displays matching flights with:

- Flight ID
- Departure date
- Departure time
- Origin airport
- Destination airport
- Aircraft type
- Flight duration

### 4.2 Ticket Booking

The booking process follows these steps:

1. Search for an available flight
2. Select a flight
3. Select a registered customer
4. Calculate the ticket price
5. Confirm the booking
6. Store the ticket in the database

Before completing a booking, the system checks:

- Whether the flight exists
- Whether the customer exists
- Whether seats are available
- Whether the customer already has a ticket for the selected flight

If all validations pass, the ticket is successfully recorded in the database.

---

## 5. Dynamic Ticket Pricing

The system includes a dynamic pricing engine that calculates ticket prices using several operational factors.

Pricing factors include:

- Aircraft type
- Flight duration
- Departure time
- Weekend travel
- Peak-hour travel

This feature creates a more realistic airline pricing process than using a single fixed ticket price.

The dynamic pricing logic is stored in:

- `pricing_engine.py`

---

## 6. Automated Crew Allocation

The project includes a `CrewAllocator` class that automatically assigns employees when a flight is created.

Crew assignments may include:

- Pilots
- Cabin crew
- Mechanics
- Ground staff

The number and type of assigned employees can depend on the aircraft and flight requirements.

This feature extends the system beyond a basic ticket-booking application by incorporating airline operational planning.

---

## 7. Business Rules Implemented

### Direct Flights Only

The system currently supports direct flights rather than connecting itineraries.

### Individual Passenger Bookings

Each passenger must have an individual ticket record.

### Round Trips as Separate Bookings

A round trip must be created as two separate ticket bookings.

### Aircraft Capacity Management

A ticket cannot be purchased when the number of booked passengers reaches the aircraft seating capacity.

### Duplicate Booking Prevention

The same customer cannot purchase more than one ticket for the same flight.

### Database Integrity

Foreign keys and database constraints prevent invalid or disconnected records.

---

## 8. Reports and Operational Outputs

The application provides several reports for monitoring airline activity.

### 8.1 Flight Sales Report

Displays:

- Flight ID
- Flight route
- Departure date
- Number of tickets sold
- Total ticket revenue

### 8.2 Employee Flight Report

Displays:

- Employee ID
- Employee name
- Job title
- Number of assigned flights

### 8.3 Passenger Manifest

Displays passengers booked on a selected flight, including:

- Ticket number
- Customer ID
- Passenger name
- Email address
- Flight information

### 8.4 Flight Crew Report

Displays all employees assigned to a selected flight.

These reports demonstrate how the stored data can support operational monitoring and management decisions.

---

## 9. Error Handling and Validation

The application includes validation and exception handling across the main system modules.

Validation features include:

- Non-empty input checks
- Integer and decimal validation
- Customer existence verification
- Flight existence verification
- Seat-availability checks
- Duplicate-booking checks
- Date and time formatting
- CSV import validation

Error handling is also included for:

- Invalid menu selections
- Missing records
- Database reset failures
- CSV file-loading failures
- Invalid ticket or flight searches
- Failed database operations

These controls improve reliability and prevent the application from terminating unexpectedly.

---

## 10. Ethical and Operational Considerations

### 10.1 Customer Data Protection

Customer information is stored in a structured database and accessed through defined system operations.

### 10.2 Transparent Pricing

The pricing model uses clear operational factors such as flight duration, aircraft type, departure time, and weekend conditions.

### 10.3 Prevention of Overbooking

Seat availability is checked before each ticket purchase, reducing the risk of selling more tickets than the aircraft can accommodate.

### 10.4 Data Integrity

Foreign key relationships and database constraints help prevent inconsistent or orphaned records.

---

## 11. Technologies and Skills Used

### Technologies

- Python
- SQLite
- SQL
- CSV files
- Command-line interface

### Programming Concepts

- Object-Oriented Programming
- Classes and inheritance
- Functions and methods
- Exception handling
- Input validation
- File input and output
- Database connectivity
- SQL queries
- Relational database design
- CRUD operations

---

## 12. Project Setup and User Guide

### 12.1 Files Included

1. **`airasia_project.py`**  
   Main program containing the menu system, CRUD classes, ticket-booking logic, reports, and CSV file-loading support.

2. **`db_base.py`**  
   Base SQLite helper class used for managing database connections and executing SQL queries.

3. **`create_database.sql`**  
   SQL script used to create the required database tables.

4. **`import_sample_data.py`**  
   Script used to reset the database and load sample records from the CSV files.

5. **`pricing_engine.py`**  
   Contains the dynamic ticket-pricing logic.

6. **`data/airports.csv`**

7. **`data/aircraft.csv`**

8. **`data/employees.csv`**

9. **`data/customers.csv`**

10. **`data/flights.csv`**

11. **`airasia.sqlite`**  
    Sample SQLite database populated with data from the CSV files.

---

## 13. How to Run the System

### Step 1: Import the Sample Data

Before using the application, populate the database by running:

```bash
python import_sample_data.py
```

This command will:

- Reset the existing database
- Recreate all required database tables
- Import sample records from the CSV files

### Step 2: Start the Application

Run the main program:

```bash
python airasia_project.py
```

This starts the interactive menu for the AirAsia Ticketing System.

### Step 3: Import CSV Data from the Main Menu

When the application starts, select:

```text
12 - Import Sample CSV Data
```

This option loads:

- Airports
- Aircraft
- Employees
- Customers
- Flights

After the CSV files are imported successfully, all CRUD, booking, and reporting features can be used.

---

## 14. Interactive Menu Walkthrough

The system uses a menu-driven interface in which each option performs a specific operation.

```text
1  - Airport Management
2  - Aircraft Management
3  - Employee Management
4  - Customer Management
5  - Flight Management
6  - Ticket Management
7  - Flight Sales Report
8  - Employee Flight Report
9  - Passenger Manifest
10 - Flight Crew Report
11 - Reset Database
12 - Import Sample CSV Data
0  - Exit System
```

---

## 15. Using CRUD Operations

After importing the CSV data, users can perform CRUD operations for the major airline entities.

Each management section provides options to:

- View records
- Search records
- Add new records
- Update existing records
- Delete records

### Airport Management

Manage airport information such as airport code, city, and country.

### Aircraft Management

Manage aircraft types and seating capacities.

### Employee Management

Manage staff records, including pilots, cabin crew, mechanics, and ground staff.

### Customer Management

Manage customer profiles used for ticket booking.

### Flight Management

Create and manage flight schedules between airports.

---

## 16. How to Search for Flights

1. From the main menu, select:

```text
5 - Flight Management
```

2. Choose the option to search for flights.

3. Enter the required information:

- Departure airport
- Destination airport
- Optional departure date

4. The system displays matching flights with:

- Flight ID
- Departure date
- Departure time
- Origin airport
- Destination airport
- Aircraft type
- Duration

---

## 17. How to Book a Flight Ticket

1. Return to the main menu.

2. Select:

```text
6 - Ticket Management
```

3. Choose:

```text
Purchase Ticket
```

4. Enter the following information:

- Customer ID
- Flight ID
- Ticket cost

5. The system automatically checks:

- Whether the flight exists
- Whether seats are available
- Whether the customer already has a ticket for the flight

6. If all validations pass, the ticket is stored in the database and the following confirmation appears:

```text
Ticket purchased successfully
```

---

## 18. Report Features

The system provides several reports for analyzing airline operations.

### 18.1 Flight Sales Report

Shows the number of tickets sold and the total revenue for each flight.

### 18.2 Employee Flight Report

Displays employees and the number of flights to which they are assigned.

### 18.3 Passenger Manifest

Lists all passengers booked on a selected flight.

### 18.4 Flight Crew Report

Shows all crew members assigned to a specific flight.

---

## 19. Notes

- Dates are stored in `YYYY-MM-DD` format.
- Times are stored in `HH:MM` format.
- The system prevents duplicate bookings for the same customer and flight.
- Aircraft capacity is checked before a ticket purchase.
- Crew members are automatically assigned when flights are created.

---

## 20. Future Improvements

Possible future enhancements include:

- A graphical or web-based interface
- User authentication and role-based access
- Payment processing
- A loyalty and rewards program
- Connecting-flight support
- Advanced flight-schedule validation
- Automated booking-confirmation emails
- Dashboard-style reporting
- Cloud database deployment

---

## 21. Conclusion

The AirAsia Ticketing System demonstrates how Python and SQLite can be combined to build a practical airline management application. The project integrates relational database design, CRUD operations, CSV data import, booking validation, dynamic pricing, automated crew allocation, reporting, and error handling within one structured command-line system.




