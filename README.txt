AIRASIA TICKETING SYSTEM - PYTHON + SQLITE CAPSTONE

  ----------------
  FILES INCLUDED
  ----------------

1.  airasia_project.py Main program with the menu system, CRUD classes,
    ticket booking logic, reports, and CSV file loading support.

2.  db_base.py Base SQLite helper class used for managing database
    connections and executing SQL queries.

3.  create_database.sql SQL script that creates all the required
    database tables.

4.  import_sample_data.py Script that resets the database and loads
    sample data from CSV files.

5.  data/airports.csv

6.  data/aircraft.csv

7.  data/employees.csv

8.  data/customers.csv

9.  data/flights.csv

10. airasia.sqlite Sample SQLite database populated using the CSV files.

  -----------------------
  HOW TO RUN THE SYSTEM
  -----------------------

Step 1 – Import Sample Data

Before using the system, the database must be populated with sample
data.

Run the following command:

python import_sample_data.py

This will: - Reset the database - Recreate all tables - Import data from
the CSV files

Step 2 – Start the Application

Run the main program:

python airasia_project.py

This will start the interactive menu for the AirAsia Ticketing System.

  -----------------------------------------
  IMPORTANT FIRST STEP IN THE APPLICATION
  -----------------------------------------

When the application starts, you will see the Main Menu.

Before using the system features, you must import the CSV data.

Choose the following option:

12 - Import Sample CSV Data

Once this option runs successfully, the system loads: - Airports -
Aircraft - Employees - Customers - Flights

After the CSV files are imported successfully, you can begin using all
CRUD and booking features of the system.

  ------------------------------
  INTERACTIVE MENU WALKTHROUGH
  ------------------------------

The system uses a menu-driven interface where each option performs
specific operations.

Main Menu Options:

1 - Airport Management 2 - Aircraft Management 3 - Employee Management
4 - Customer Management 5 - Flight Management 6 - Ticket Management 7 -
Flight Sales Report 8 - Employee Flight Report 9 - Passenger Manifest
10 - Flight Crew Report 11 - Reset Database 12 - Import Sample CSV Data
0 - Exit System

  -----------------------
  USING CRUD OPERATIONS
  -----------------------

After importing the CSV data, you can use the CRUD features of the
system.

Each entity has options to:

-   View records
-   Search records
-   Add new records
-   Update existing records
-   Delete records

CRUD sections include:

Airport Management Manage airport information such as code, city, and
country.

Aircraft Management Manage aircraft types and seating capacities.

Employee Management Manage staff records including pilots, cabin crew,
mechanics, and ground staff.

Customer Management Manage customer profiles used for ticket booking.

Flight Management Create and manage flight schedules between airports.

  ---------------------------
  HOW TO SEARCH FOR FLIGHTS
  ---------------------------

Step 1 From the Main Menu choose:

5 - Flight Management

Step 2 Choose the option to search flights.

Step 3 Enter the required information:

-   Departure airport
-   Destination airport
-   Optional departure date

Step 4 The system will display matching flights with details including:

-   Flight ID
-   Departure date
-   Departure time
-   Origin airport
-   Destination airport
-   Aircraft type
-   Duration

  -----------------------------
  HOW TO BOOK A FLIGHT TICKET
  -----------------------------

Step 1 Return to the Main Menu.

Step 2 Choose:

6 - Ticket Management

Step 3 Select:

Purchase Ticket

Step 4 Enter the following information:

-   Customer ID
-   Flight ID
-   Ticket cost

Step 5 The system will automatically check:

-   Whether the flight exists
-   Whether seats are available
-   Whether the customer already has a ticket for the flight

Step 6 If all validations pass, the ticket will be stored in the
database and the following confirmation message will appear:

Ticket purchased successfully

  -----------------
  REPORT FEATURES
  -----------------

The system provides several reports to analyze airline operations.

7 - Flight Sales Report Shows the number of tickets sold and total
revenue for each flight.

8 - Employee Flight Report Displays employees and the number of flights
they are assigned to.

9 - Passenger Manifest Lists all passengers booked on a selected flight.

10 - Flight Crew Report Shows all crew members assigned to a specific
flight.

  -------
  NOTES
  -------

-   Dates are stored in YYYY-MM-DD format
-   Times are stored in HH:MM format
-   The system prevents duplicate bookings for the same customer and
    flight
-   Aircraft capacity is checked before a ticket purchase
-   Crew members are automatically assigned when flights are created
