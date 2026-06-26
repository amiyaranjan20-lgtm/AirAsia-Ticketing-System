


"""
AirAsia Ticketing System
----------------------------------------
This program implements a command-line airline ticketing system
for managing airports, aircraft, employees, customers, flights,
tickets, and reports.

The system uses an SQLite database to store operational data
and provides CRUD functionality for all major airline entities.

Key Features:
• Airport management
• Aircraft management
• Employee management
• Customer management
• Flight scheduling
• Ticket purchasing and cancellation
• Operational reports
• CSV data import
• Automated crew assignment

Group 1, Members:
Amiya Ranjan Sahoo
Tate Harris
Zachary Hancock
"""


# ------------------------------------------------------------
# Import Required Python Libraries
# ------------------------------------------------------------
# datetime  -> used for recording ticket purchase dates
# csv       -> used to import sample data from CSV files
# os        -> used for file handling and system commands
# db_base   -> base database class used for SQLite connection
# random    -> used for automated crew assignment
# ------------------------------------------------------------



from datetime import datetime
import csv
import os

import db_base as db

import os

DB_NAME = "airasia.sqlite"


# ------------------------------------------------------------
# Project Database Base Class
# ------------------------------------------------------------
# This class establishes a shared connection to the SQLite
# database used by the AirAsia Ticketing System.
#
# All entity classes (Airport, Aircraft, Employee, etc.)
# inherit from this class so they use the same database
# connection and cursor.
#
# The reset_database() function reloads the schema using
# the SQL script file "create_database.sql".
# ------------------------------------------------------------





class ProjectDB(db.DBbase):
    """
    Common project database class.
    All entity classes inherit from this class so they connect to the same DB.
    """

    def __init__(self):
        super().__init__(DB_NAME)

    def reset_database(self):
        try:
            with open("create_database.sql", "r", encoding="utf-8") as file:
                sql = file.read()
            super().execute_script(sql)
            print("Database reset completed successfully.")
        except Exception as e:
            print("An error has occurred while resetting the database.", e)



# ------------------------------------------------------------
# Airport Management Class
# ------------------------------------------------------------
# Handles all airport-related database operations including:
#   • Adding new airports
#   • Searching airports by code, city, or country
#   • Viewing airport records
#   • Updating airport details
#   • Deleting airports
#
# Each method executes SQL commands on the Airport table.
# ------------------------------------------------------------


class Airport(ProjectDB):

    def add(self, airport_code, name, city, country):
        try:
            self.get_cursor.execute("""
                INSERT INTO Airport (Airport_code, Name, City, Country)
                VALUES (?, ?, ?, ?);
            """, (airport_code.strip().upper(), name.strip(), city.strip(), country.strip()))
            self.get_connection.commit()
            print("Airport added successfully.")
        except Exception as e:
            print("An error has occurred while adding airport.", e)

    def search_locations(self, keyword):
        try:
            sql = """
            SELECT Airport_code, Name, City, Country
            FROM Airport
            WHERE 
                Airport_code LIKE ?
                OR Name LIKE ?
                OR City LIKE ?
                OR Country LIKE ?
            ORDER BY City;
            """

            key = f"%{keyword.strip()}%"

            return self.get_cursor.execute(sql, (key, key, key, key)).fetchall()

        except Exception as e:
            print("Error searching locations.", e)

    def fetch(self, airport_code=None):
        try:
            if airport_code is not None and str(airport_code).strip() != "":
                return self.get_cursor.execute("""
                    SELECT * FROM Airport
                    WHERE Airport_code = ?;
                """, (airport_code.strip().upper(),)).fetchone()
            return self.get_cursor.execute("""
                SELECT * FROM Airport
                ORDER BY Airport_code;
            """).fetchall()
        except Exception as e:
            print("An error has occurred while fetching airport data.", e)

    def update(self, airport_code, name, city, country):
        try:
            self.get_cursor.execute("""
                UPDATE Airport
                SET Name = ?, City = ?, Country = ?
                WHERE Airport_code = ?;
            """, (name.strip(), city.strip(), country.strip(), airport_code.strip().upper()))
            self.get_connection.commit()
            print("Airport updated successfully.")
        except Exception as e:
            print("An error has occurred while updating airport.", e)

    def delete(self, airport_code):
        try:
            self.get_cursor.execute("""
                DELETE FROM Airport
                WHERE Airport_code = ?;
            """, (airport_code.strip().upper(),))
            self.get_connection.commit()
            print("Airport deleted successfully.")
        except Exception as e:
            print("An error has occurred while deleting airport.", e)



# ------------------------------------------------------------
# Aircraft Management Class
# ------------------------------------------------------------
# Manages aircraft records stored in the database.
#
# Responsibilities include:
#   • Adding aircraft types and capacities
#   • Searching aircraft by ID or keyword
#   • Updating aircraft information
#   • Deleting aircraft records
#
# Aircraft capacity is later used to determine flight crew
# allocation and available seating.
# ------------------------------------------------------------




class Aircraft(ProjectDB):

    def add(self, aircraft_type, capacity):
        try:
            self.get_cursor.execute("""
                INSERT INTO Aircraft (type, Capacity)
                VALUES (?, ?);
            """, (aircraft_type.strip(), int(capacity)))
            self.get_connection.commit()
            print("Aircraft added successfully.")
        except Exception as e:
            print("An error has occurred while adding aircraft.", e)

    def fetch(self, aircraft_id=None, keyword=None):
        try:
            # search by ID
            if aircraft_id is not None and str(aircraft_id).strip() != "":
                return self.get_cursor.execute("""
                    SELECT *
                    FROM Aircraft
                    WHERE Aircraft_Id = ?;
                """, (int(aircraft_id),)).fetchone()

            # flexible search
            if keyword is not None and str(keyword).strip() != "":
                key = f"%{keyword.strip()}%"

                return self.get_cursor.execute("""
                    SELECT *
                    FROM Aircraft
                    WHERE
                        type LIKE ?
                        OR CAST(Capacity AS TEXT) LIKE ?
                    ORDER BY Aircraft_Id;
                """, (key, key)).fetchall()

            return self.get_cursor.execute("""
                SELECT *
                FROM Aircraft
                ORDER BY Aircraft_Id;
            """).fetchall()

        except Exception as e:
            print("An error has occurred while fetching aircraft.", e)

    def update(self, aircraft_id, aircraft_type, capacity):
        try:
            self.get_cursor.execute("""
                UPDATE Aircraft
                SET type = ?, Capacity = ?
                WHERE Aircraft_Id = ?;
            """, (aircraft_type.strip(), int(capacity), int(aircraft_id)))
            self.get_connection.commit()
            print("Aircraft updated successfully.")
        except Exception as e:
            print("An error has occurred while updating aircraft.", e)

    def delete(self, aircraft_id):
        try:
            self.get_cursor.execute("""
                DELETE FROM Aircraft
                WHERE Aircraft_Id = ?;
            """, (int(aircraft_id),))
            self.get_connection.commit()
            print("Aircraft deleted successfully.")
        except Exception as e:
            print("An error has occurred while deleting aircraft.", e)


# ------------------------------------------------------------
# Employee Management Class
# ------------------------------------------------------------
# Manages airline staff records including pilots, cabin crew,
# mechanics, and ground staff.
#
# Functions include:
#   • Adding employee records
#   • Searching employees by name, ID, or job title
#   • Updating employee information
#   • Removing employee records
#
# Employee data is also used for automatic crew assignment
# to flights.
# ------------------------------------------------------------



class Employee(ProjectDB):

    def add(self, first_name, last_name, job_title):
        try:
            self.get_cursor.execute("""
                INSERT INTO Employee (First_name, Last_name, Job_title)
                VALUES (?, ?, ?);
            """, (first_name.strip(), last_name.strip(), job_title.strip()))
            self.get_connection.commit()
            print("Employee added successfully.")
        except Exception as e:
            print("An error has occurred while adding employee.", e)

    def fetch(self, employee_id=None, keyword=None):
        try:

            # search by ID
            if employee_id is not None and str(employee_id).strip() != "":
                return self.get_cursor.execute("""
                    SELECT *
                    FROM Employee
                    WHERE Employee_Id = ?;
                """, (int(employee_id),)).fetchone()

            # flexible search by name or job title (case sensitive)
            if keyword is not None and str(keyword).strip() != "":
                key = f"%{keyword.strip()}%"

                return self.get_cursor.execute("""
                    SELECT *
                    FROM Employee
                    WHERE
                        First_name LIKE ?
                        OR Last_name LIKE ?
                        OR Job_title LIKE ?
                    ORDER BY Employee_Id;
                """, (key, key, key)).fetchall()

            # default return all employees
            return self.get_cursor.execute("""
                SELECT *
                FROM Employee
                ORDER BY Employee_Id;
            """).fetchall()

        except Exception as e:
            print("An error has occurred while fetching employee data.", e)

    def update(self, employee_id, first_name, last_name, job_title):
        try:
            self.get_cursor.execute("""
                UPDATE Employee
                SET First_name = ?, Last_name = ?, Job_title = ?
                WHERE Employee_Id = ?;
            """, (first_name.strip(), last_name.strip(), job_title.strip(), int(employee_id)))
            self.get_connection.commit()
            print("Employee updated successfully.")
        except Exception as e:
            print("An error has occurred while updating employee.", e)

    def delete(self, employee_id):
        try:
            self.get_cursor.execute("""
                DELETE FROM Employee
                WHERE Employee_Id = ?;
            """, (int(employee_id),))
            self.get_connection.commit()
            print("Employee deleted successfully.")
        except Exception as e:
            print("An error has occurred while deleting employee.", e)


# ------------------------------------------------------------
# Customer Management Class
# ------------------------------------------------------------
# Stores and manages passenger information required for
# ticket booking and identification.
#
# Functions include:
#   • Creating new customer profiles
#   • Searching customers by ID, name, phone, or email
#   • Updating personal details
#   • Deleting customer records
#
# Customer data is linked to tickets and flight manifests.
# ------------------------------------------------------------



class Customer(ProjectDB):

    def add(self, title, first_name, last_name, gender, dob, citizenship, phone, email, passport_number, passport_expiry):

        try:
            self.get_cursor.execute("""
                INSERT INTO Customer (title, First_name, Last_name, Gender, Dob,
                    Citizenship, Phone, email, Passport_number, Passport_expiry
                        )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                    title.strip(),
                    first_name.strip(),
                    last_name.strip(),
                    gender.strip(),
                    dob.strip(),
                    citizenship.strip(),
                    phone.strip(),
                    email.strip().lower(),
                    passport_number.strip(),
                    passport_expiry.strip()
                ))
            self.get_connection.commit()
            print("Customer added successfully.")
        except Exception as e:
            print("An error has occurred while adding customer.", e)

    def fetch(self, customer_id=None, email=None, keyword=None):
        try:

            # search by customer ID
            if customer_id is not None and str(customer_id).strip() != "":
                return self.get_cursor.execute("""
                    SELECT * FROM Customer
                    WHERE Customer_id = ?;
                """, (int(customer_id),)).fetchone()

            # search by email
            if email is not None and str(email).strip() != "":
                return self.get_cursor.execute("""
                    SELECT * FROM Customer
                    WHERE email = ?;
                """, (email.strip().lower(),)).fetchone()

            # new flexible search
            if keyword is not None and str(keyword).strip() != "":
                key = f"%{keyword.strip()}%"

                return self.get_cursor.execute("""
                    SELECT *
                    FROM Customer
                    WHERE
                        First_name LIKE ?
                        OR Last_name LIKE ?
                        OR Phone LIKE ?
                        OR email LIKE ?
                        OR CAST(Customer_id AS TEXT) LIKE ?
                    ORDER BY Customer_id;
                """, (key, key, key, key, key)).fetchall()

            # default → return all customers
            return self.get_cursor.execute("""
                SELECT * FROM Customer
                ORDER BY Customer_id;
            """).fetchall()

        except Exception as e:
            print("An error has occurred while fetching customer data.", e)

    def update(self, customer_id, title, first_name, last_name, dob, citizenship, email):
        try:
            self.get_cursor.execute("""
                UPDATE Customer
                SET title = ?, First_name = ?, Last_name = ?, Dob = ?, Citizenship = ?, email = ?
                WHERE Customer_id = ?;
            """, (
                title.strip(),
                first_name.strip(),
                last_name.strip(),
                dob.strip(),
                citizenship.strip(),
                email.strip().lower(),
                int(customer_id)
            ))
            self.get_connection.commit()
            print("Customer updated successfully.")
        except Exception as e:
            print("An error has occurred while updating customer.", e)

    def delete(self, customer_id):
        try:
            self.get_cursor.execute("""
                DELETE FROM Customer
                WHERE Customer_id = ?;
            """, (int(customer_id),))
            self.get_connection.commit()
            print("Customer deleted successfully.")
        except Exception as e:
            print("An error has occurred while deleting customer.", e)


# ------------------------------------------------------------
# Flight Management Class
# ------------------------------------------------------------
# Handles flight scheduling and flight-related operations.
#
# Responsibilities include:
#   • Creating flight schedules
#   • Searching flights by origin, destination, or date
#   • Updating flight information
#   • Deleting flights
#   • Checking seats sold and remaining capacity
#
# When a new flight is created, crew members are automatically
# assigned using the CrewAllocator class.
# ------------------------------------------------------------



class Flight(ProjectDB):

    def add(self, airport_from, airport_to, aircraft_id, departure_date,
            departure_time, departure_gate, arrival_gate, duration, employee_id):
        try:
            self.get_cursor.execute("""
                INSERT INTO Flight (
                    Airport_from, Airport_to, Aircraft_Id, Departure_date,
                    Departure_time, Departure_gate, Arrival_gate, Duration, Employee_Id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                airport_from.strip().upper(),
                airport_to.strip().upper(),
                int(aircraft_id),
                departure_date.strip(),
                departure_time.strip(),
                departure_gate.strip(),
                arrival_gate.strip(),
                int(duration),
                int(employee_id)
            ))
            self.get_connection.commit()

            flight_id = self.get_cursor.lastrowid
            capacity = self.get_cursor.execute("""
            SELECT Capacity
            FROM Aircraft
            WHERE Aircraft_Id = ?
            """, (aircraft_id,)).fetchone()[0]

            CrewAllocator(self.get_cursor, self.get_connection).assign_flight_crew(flight_id, capacity)

            print("Flight added successfully.")

        except Exception as e:
            print("An error has occurred while adding flight.", e)

    def search_flights_any_location(self, from_keyword, to_keyword, departure_date=None):
        try:
            sql = """
            SELECT f.Flight_Id,
                   f.Departure_date,
                   f.Departure_time,
                   f.Airport_from,
                   ap1.City,
                   f.Airport_to,
                   ap2.City,
                   ac.type,
                   ac.Capacity,
                   f.Duration
            FROM Flight f
            JOIN Airport ap1 ON f.Airport_from = ap1.Airport_code
            JOIN Airport ap2 ON f.Airport_to = ap2.Airport_code
            JOIN Aircraft ac ON f.Aircraft_Id = ac.Aircraft_Id
            WHERE
            (
                ap1.Airport_code LIKE ?
                OR ap1.Name LIKE ?
                OR ap1.City LIKE ?
                OR ap1.Country LIKE ?
            )
            AND
            (
                ap2.Airport_code LIKE ?
                OR ap2.Name LIKE ?
                OR ap2.City LIKE ?
                OR ap2.Country LIKE ?
            )
            """

            key_from = f"%{from_keyword.strip()}%"
            key_to = f"%{to_keyword.strip()}%"

            params = [key_from, key_from, key_from, key_from,
                      key_to, key_to, key_to, key_to]

            if departure_date:
                sql += " AND f.Departure_date = ?"
                params.append(departure_date)

            sql += " ORDER BY f.Departure_date, f.Departure_time"

            return self.get_cursor.execute(sql, tuple(params)).fetchall()

        except Exception as e:
            print("Error searching flights.", e)

    def search(self, origin, destination=None):
        origin = f"%{origin}%"
        if destination:
            destination = f"%{destination}%"
            return self.get_cursor.execute("""
                SELECT 
                    f.Flight_Id,
                    f.Departure_date,
                    f.Departure_time,
                    f.Airport_from,
                    a1.City,
                    f.Airport_to,
                    a2.City,
                    ac.Type,
                    ac.Capacity,
                    f.Departure_gate,
                    f.Arrival_gate,
                    f.Duration
                FROM Flight f
                JOIN Airport a1 ON f.Airport_from = a1.Airport_code
                JOIN Airport a2 ON f.Airport_to = a2.Airport_code
                JOIN Aircraft ac ON f.Aircraft_Id = ac.Aircraft_Id
                WHERE
                    (f.Airport_from LIKE ? OR a1.City LIKE ?)
                    AND (f.Airport_to LIKE ? OR a2.City LIKE ?)
                ORDER BY f.Departure_date, f.Departure_time
            """, (origin, origin, destination, destination)).fetchall()
        else:
            return self.get_cursor.execute("""
                SELECT 
                    f.Flight_Id,
                    f.Departure_date,
                    f.Departure_time,
                    f.Airport_from,
                    a1.City,
                    f.Airport_to,
                    a2.City,
                    ac.Type,
                    ac.Capacity,
                    f.Departure_gate,
                    f.Arrival_gate,
                    f.Duration
                FROM Flight f
                JOIN Airport a1 ON f.Airport_from = a1.Airport_code
                JOIN Airport a2 ON f.Airport_to = a2.Airport_code
                JOIN Aircraft ac ON f.Aircraft_Id = ac.Aircraft_Id
                WHERE
                    f.Flight_Id LIKE ?
                    OR f.Airport_from LIKE ?
                    OR a1.City LIKE ?
                ORDER BY f.Departure_date, f.Departure_time
            """, (origin, origin, origin)).fetchall()


    def fetch(self, flight_id=None):
        try:
            if flight_id is not None and str(flight_id).strip() != "":
                return self.get_cursor.execute("""
                    SELECT Flight_Id, Airport_from, Airport_to, Aircraft_Id,
                           Departure_date, Departure_time, Departure_gate,
                           Arrival_gate, Duration, Employee_Id
                    FROM Flight
                    WHERE Flight_Id = ?;
                """, (int(flight_id),)).fetchone()

            return self.get_cursor.execute("""
                SELECT Flight_Id, Airport_from, Airport_to, Aircraft_Id,
                       Departure_date, Departure_time, Departure_gate,
                       Arrival_gate, Duration, Employee_Id
                FROM Flight
                ORDER BY Departure_date, Departure_time;
            """).fetchall()
        except Exception as e:
            print("An error has occurred while fetching flight data.", e)

    def fetch_detailed(self, flight_id=None):
        try:
            base_sql = """
            SELECT f.Flight_Id,
                   f.Departure_date,
                   f.Departure_time,
                   f.Airport_from,
                   ap1.City,
                   f.Airport_to,
                   ap2.City,
                   ac.type,
                   ac.Capacity,
                   f.Departure_gate,
                   f.Arrival_gate,
                   f.Duration,
                   COUNT(fc.Employee_Id) AS Crew_Count
            FROM Flight f
            JOIN Airport ap1 ON f.Airport_from = ap1.Airport_code
            JOIN Airport ap2 ON f.Airport_to = ap2.Airport_code
            JOIN Aircraft ac ON f.Aircraft_Id = ac.Aircraft_Id
            LEFT JOIN FlightCrew fc ON f.Flight_Id = fc.Flight_Id
            """

            if flight_id is not None and str(flight_id).strip() != "":
                sql = base_sql + """
                WHERE f.Flight_Id = ?
                GROUP BY f.Flight_Id
                ORDER BY f.Departure_date, f.Departure_time;
                """
                return self.get_cursor.execute(sql, (int(flight_id),)).fetchone()

            sql = base_sql + """
            GROUP BY f.Flight_Id
            ORDER BY f.Departure_date, f.Departure_time;
            """
            return self.get_cursor.execute(sql).fetchall()

        except Exception as e:
            print("An error has occurred while fetching detailed flights.", e)

    def update(self, flight_id, airport_from, airport_to, aircraft_id, departure_date,
               departure_time, departure_gate, arrival_gate, duration, employee_id):
        try:
            self.get_cursor.execute("""
                UPDATE Flight
                SET Airport_from = ?, Airport_to = ?, Aircraft_Id = ?, Departure_date = ?,
                    Departure_time = ?, Departure_gate = ?, Arrival_gate = ?, Duration = ?,
                    Employee_Id = ?
                WHERE Flight_Id = ?;
            """, (
                airport_from.strip().upper(),
                airport_to.strip().upper(),
                int(aircraft_id),
                departure_date.strip(),
                departure_time.strip(),
                departure_gate.strip(),
                arrival_gate.strip(),
                int(duration),
                int(employee_id),
                int(flight_id)
            ))
            self.get_connection.commit()
            print("Flight updated successfully.")
        except Exception as e:
            print("An error has occurred while updating flight.", e)

    def delete(self, flight_id):
        try:
            self.get_cursor.execute("""
                DELETE FROM Flight
                WHERE Flight_Id = ?;
            """, (int(flight_id),))
            self.get_connection.commit()
            print("Flight deleted successfully.")
        except Exception as e:
            print("An error has occurred while deleting flight.", e)

    def search_direct_flights(self, airport_from, airport_to, departure_date=None):
        try:
            sql = """
                SELECT f.Flight_Id,
                       f.Departure_date,
                       f.Departure_time,
                       f.Airport_from,
                       ap1.City,
                       f.Airport_to,
                       ap2.City,
                       ac.type,
                       ac.Capacity,
                       f.Duration
                FROM Flight f
                JOIN Airport ap1 ON f.Airport_from = ap1.Airport_code
                JOIN Airport ap2 ON f.Airport_to = ap2.Airport_code
                JOIN Aircraft ac ON f.Aircraft_Id = ac.Aircraft_Id
                WHERE f.Airport_from = ? AND f.Airport_to = ?
            """
            params = [airport_from.strip().upper(), airport_to.strip().upper()]

            if departure_date is not None and str(departure_date).strip() != "":
                sql += " AND f.Departure_date = ?"
                params.append(departure_date.strip())

            sql += " ORDER BY f.Departure_date, f.Departure_time;"
            return self.get_cursor.execute(sql, tuple(params)).fetchall()
        except Exception as e:
            print("An error has occurred while searching flights.", e)

    def seats_sold(self, flight_id):
        try:
            result = self.get_cursor.execute("""
                SELECT COUNT(*)
                FROM Ticket
                WHERE Flight_Id = ?;
            """, (int(flight_id),)).fetchone()
            return result[0] if result else 0
        except Exception as e:
            print("An error has occurred while counting seats sold.", e)
            return 0

    def seats_remaining(self, flight_id):
        try:
            result = self.get_cursor.execute("""
                SELECT ac.Capacity
                FROM Flight f
                JOIN Aircraft ac ON f.Aircraft_Id = ac.Aircraft_Id
                WHERE f.Flight_Id = ?;
            """, (int(flight_id),)).fetchone()

            if result is None:
                return None

            capacity = result[0]
            sold = self.seats_sold(flight_id)
            return capacity - sold
        except Exception as e:
            print("An error has occurred while checking remaining seats.", e)
            return None


# ------------------------------------------------------------
# Ticket Management Class
# ------------------------------------------------------------
# Handles ticket purchasing, ticket lookup, and ticket
# cancellation operations.
#
# Core functionality:
#   • Purchase tickets for customers
#   • Ensure flights have available seats
#   • Prevent duplicate bookings for the same flight
#   • View and search ticket records
#   • Cancel or update tickets
#
# Ticket data links customers to specific flights.
# ------------------------------------------------------------




class Ticket(ProjectDB):

    def add(self, customer_id, flight_id, cost, purchase_date=None):
        """
        Generic admin ticket add method.
        In normal customer flow, purchase_ticket should be used because it checks capacity.
        """
        try:
            if purchase_date is None:
                purchase_date = datetime.now().strftime("%Y-%m-%d")

            self.get_cursor.execute("""
                INSERT INTO Ticket (Customer_Id, Flight_Id, Cost, purchaseDate)
                VALUES (?, ?, ?, ?);
            """, (int(customer_id), int(flight_id), float(cost), purchase_date))
            self.get_connection.commit()
            print("Ticket added successfully.")
        except Exception as e:
            print("An error has occurred while adding ticket.", e)

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.get_cursor.execute("""
            SELECT 
                t.Ticket_number,
                t.Customer_Id,
                c.First_name || ' ' || c.Last_name,
                f.Flight_Id,
                f.Airport_from,
                f.Airport_to,
                f.Departure_date,
                f.Departure_time,
                t.Cost
            FROM Ticket t
            JOIN Customer c ON t.Customer_Id = c.Customer_id
            JOIN Flight f ON t.Flight_Id = f.Flight_Id
            WHERE
                CAST(t.Ticket_number AS TEXT) LIKE ?
                OR c.First_name LIKE ?
                OR c.Last_name LIKE ?
                OR CAST(f.Flight_Id AS TEXT) LIKE ?
                OR f.Airport_from LIKE ?
                OR f.Airport_to LIKE ?
            ORDER BY t.Ticket_number
        """, (keyword, keyword, keyword, keyword, keyword, keyword)).fetchall()




    def purchase_ticket(self, customer_id, flight_id, cost):
        try:
            flight = Flight()
            flight_id = int(flight_id)
            remaining = flight.seats_remaining(flight_id)

            if remaining is None:
                raise Exception("Flight not found.")

            if remaining <= 0:
                raise Exception("No seats available on this flight.")

            existing = self.get_cursor.execute("""
                SELECT Ticket_number
                FROM Ticket
                WHERE Customer_Id = ? AND Flight_Id = ?;
            """, (int(customer_id), int(flight_id))).fetchone()

            if existing is not None:
                raise Exception("This customer already has a ticket for the selected flight.")

            purchase_date = datetime.now().strftime("%Y-%m-%d")
            self.get_cursor.execute("""
                INSERT INTO Ticket (Customer_Id, Flight_Id, Cost, purchaseDate)
                VALUES (?, ?, ?, ?);
            """, (int(customer_id), int(flight_id), float(cost), purchase_date))
            self.get_connection.commit()
            print("Ticket purchased successfully.")
        except Exception as e:
            print("An error has occurred while purchasing ticket.", e)

    def fetch(self, ticket_number=None):
        try:
            if ticket_number is not None and str(ticket_number).strip() != "":
                return self.get_cursor.execute("""
                    SELECT * FROM Ticket
                    WHERE Ticket_number = ?;
                """, (int(ticket_number),)).fetchone()

            return self.get_cursor.execute("""
                SELECT * FROM Ticket
                ORDER BY Ticket_number;
            """).fetchall()
        except Exception as e:
            print("An error has occurred while fetching ticket data.", e)

    def fetch_detailed(self, ticket_number=None, customer_id=None):
        try:
            sql = """
                SELECT t.Ticket_number,
                       c.Customer_id,
                       c.First_name || ' ' || c.Last_name,
                       f.Flight_Id,
                       f.Airport_from,
                       f.Airport_to,
                       f.Departure_date,
                       f.Departure_time,
                       t.Cost,
                       t.purchaseDate
                FROM Ticket t
                JOIN Customer c ON t.Customer_Id = c.Customer_id
                JOIN Flight f ON t.Flight_Id = f.Flight_Id
                WHERE 1 = 1
            """
            params = []

            if ticket_number is not None and str(ticket_number).strip() != "":
                sql += " AND t.Ticket_number = ?"
                params.append(int(ticket_number))

            if customer_id is not None and str(customer_id).strip() != "":
                sql += " AND c.Customer_id = ?"
                params.append(int(customer_id))

            sql += " ORDER BY t.Ticket_number;"
            rows = self.get_cursor.execute(sql, tuple(params)).fetchall()

            if ticket_number is not None and len(rows) == 1:
                return rows[0]
            return rows
        except Exception as e:
            print("An error has occurred while fetching detailed ticket data.", e)

    def update(self, ticket_number, customer_id, flight_id, cost, purchase_date):
        try:
            self.get_cursor.execute("""
                UPDATE Ticket
                SET Customer_Id = ?, Flight_Id = ?, Cost = ?, purchaseDate = ?
                WHERE Ticket_number = ?;
            """, (
                int(customer_id),
                int(flight_id),
                float(cost),
                purchase_date.strip(),
                int(ticket_number)
            ))
            self.get_connection.commit()
            print("Ticket updated successfully.")
        except Exception as e:
            print("An error has occurred while updating ticket.", e)


    def update_date(self, ticket_number, purchase_date):
        try:
            self.get_cursor.execute("""
                UPDATE Ticket
                SET purchaseDate = ?
                WHERE Ticket_number = ?;
            """, (purchase_date.strip(), int(ticket_number)))
            self.get_connection.commit()
        except Exception as e:
            print("Error updating purchase date.", e)


    def delete(self, ticket_number):
        try:
            self.get_cursor.execute("""
                DELETE FROM Ticket
                WHERE Ticket_number = ?;
            """, (int(ticket_number),))
            self.get_connection.commit()
            print("Ticket deleted successfully.")
        except Exception as e:
            print("An error has occurred while deleting ticket.", e)

    def cancel_ticket(self, ticket_number):
        try:
            record = self.fetch(ticket_number)
            if record is None:
                raise Exception("Ticket not found.")

            self.delete(ticket_number)
            print("Ticket cancellation completed successfully.")
        except Exception as e:
            print("An error has occurred while cancelling ticket.", e)




# ------------------------------------------------------------
# Reporting Class
# ------------------------------------------------------------
# Generates operational reports using SQL queries.
#
# Available reports:
#   • Flight sales report (tickets sold and revenue)
#   • Employee flight assignment report
#   • Passenger manifest for a flight
#   • Flight crew report
#
# These reports help analyze airline operations.
# ------------------------------------------------------------




class Report(ProjectDB):

    def flight_sales_report(self):
        try:
            return self.get_cursor.execute("""
                SELECT f.Flight_Id,
                       f.Airport_from,
                       f.Airport_to,
                       f.Departure_date,
                       COUNT(t.Ticket_number) AS Tickets_Sold,
                       COALESCE(SUM(t.Cost), 0) AS Total_Sales
                FROM Flight f
                LEFT JOIN Ticket t ON f.Flight_Id = t.Flight_Id
                GROUP BY f.Flight_Id, f.Airport_from, f.Airport_to, f.Departure_date
                ORDER BY Total_Sales DESC;
            """).fetchall()
        except Exception as e:
            print("An error has occurred while generating flight sales report.", e)

    def flight_crew(self, flight_id):

        return self.get_cursor.execute("""
        SELECT e.Employee_Id,
               e.First_name || ' ' || e.Last_name,
               e.Job_title
        FROM FlightCrew fc
        JOIN Employee e
        ON fc.Employee_Id = e.Employee_Id
        WHERE fc.Flight_Id = ?
        """, (flight_id,)).fetchall()



    def employee_flight_report(self):
        try:
            return self.get_cursor.execute("""
            SELECT e.Employee_Id,
                   e.First_name || ' ' || e.Last_name,
                   e.Job_title,
                   COUNT(fc.Flight_Id) AS Flights_Assigned
            FROM Employee e
            LEFT JOIN FlightCrew fc
            ON e.Employee_Id = fc.Employee_Id
            GROUP BY e.Employee_Id
            ORDER BY Flights_Assigned DESC;
            """).fetchall()
        except Exception as e:
            print("An error has occurred while generating employee report.", e)

    def passenger_manifest(self, flight_id):
        try:
            return self.get_cursor.execute("""
                SELECT t.Ticket_number,
                       c.Customer_id,
                       c.First_name,
                       c.Last_name,
                       c.email
                FROM Ticket t
                JOIN Customer c ON t.Customer_Id = c.Customer_id
                WHERE t.Flight_Id = ?
                ORDER BY c.Last_name, c.First_name;
            """, (int(flight_id),)).fetchall()
        except Exception as e:
            print("An error has occurred while generating passenger manifest.", e)


# ------------------------------------------------------------
# CSV Data Import Class
# ------------------------------------------------------------
# Provides functionality to import sample data from CSV files
# into the database tables.
#
# Supported imports:
#   • Airports
#   • Aircraft
#   • Employees
#   • Customers
#   • Flights
#
# This allows quick initialization of the system with
# realistic dataset examples.
# ------------------------------------------------------------


class CSVImporter(ProjectDB):
    """
    Handles file I/O requirements
    """

    def import_airports(self, file_path):
        try:
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.get_cursor.execute("""
                        INSERT INTO Airport (Airport_code, Name, City, Country)
                        VALUES (?, ?, ?, ?);
                    """, (
                        row["Airport_code"].strip().upper(),
                        row["Name"].strip(),
                        row["City"].strip(),
                        row["Country"].strip()
                    ))
            self.get_connection.commit()
            print("Airport CSV imported successfully.")
        except Exception as e:
            print("An error has occurred while importing airports CSV.", e)

    def import_aircraft(self, file_path):
        try:
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.get_cursor.execute("""
                        INSERT INTO Aircraft (type, Capacity)
                        VALUES (?, ?);
                    """, (
                        row["type"].strip(),
                        int(row["Capacity"])
                    ))
            self.get_connection.commit()
            print("Aircraft CSV imported successfully.")
        except Exception as e:
            print("An error has occurred while importing aircraft CSV.", e)

    def import_employees(self, file_path):
        try:
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.get_cursor.execute("""
                        INSERT INTO Employee (First_name, Last_name, Job_title)
                        VALUES (?, ?, ?);
                    """, (
                        row["First_name"].strip(),
                        row["Last_name"].strip(),
                        row["Job_title"].strip()
                    ))
            self.get_connection.commit()
            print("Employee CSV imported successfully.")
        except Exception as e:
            print("An error has occurred while importing employees CSV.", e)

    def import_customers(self, file_path):
        try:
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    self.get_cursor.execute("""
                        INSERT INTO Customer (
                            title,
                            First_name,
                            Last_name,
                            Gender,
                            Dob,
                            Citizenship,
                            Phone,
                            email,
                            Passport_number,
                            Passport_expiry
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """, (
                        row["title"].strip(),
                        row["First_name"].strip(),
                        row["Last_name"].strip(),
                        row["Gender"].strip(),
                        row["Dob"].strip(),
                        row["Citizenship"].strip(),
                        row["Phone"].strip(),
                        row["email"].strip().lower(),
                        row["Passport_number"].strip(),
                        row["Passport_expiry"].strip()
                    ))

            self.get_connection.commit()
            print("Customer CSV imported successfully.")

        except Exception as e:
            print("An error has occurred while importing customers CSV.", e)

    def import_flights(self, file_path):
        try:
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    departure_date = row["Departure_date"].strip()

                    self.get_cursor.execute("""
                        INSERT INTO Flight (
                            Airport_from, Airport_to, Aircraft_Id, Departure_date,
                            Departure_time, Departure_gate, Arrival_gate, Duration, Employee_Id
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """, (
                        row["Airport_from"].strip().upper(),
                        row["Airport_to"].strip().upper(),
                        int(row["Aircraft_Id"]),
                        departure_date,
                        row["Departure_time"].strip(),
                        row["Departure_gate"].strip(),
                        row["Arrival_gate"].strip(),
                        int(row["Duration"]),
                        int(row["Employee_Id"])
                    ))
                    flight_id = self.get_cursor.lastrowid

                    capacity = self.get_cursor.execute("""
                    SELECT Capacity
                    FROM Aircraft
                    WHERE Aircraft_Id = ?
                    """, (int(row["Aircraft_Id"]),)).fetchone()[0]

                    CrewAllocator(self.get_cursor, self.get_connection).assign_flight_crew(
                        flight_id,
                        capacity
                    )

            self.get_connection.commit()
            print("Flight CSV imported successfully.")

        except Exception as e:
            print("An error has occurred while importing flights CSV.", e)

    def import_all_default_files(self):
        try:
            self.import_airports(os.path.join("data", "airports.csv"))
            self.import_aircraft(os.path.join("data", "aircraft.csv"))
            self.import_employees(os.path.join("data", "employees.csv"))
            self.import_customers(os.path.join("data", "customers.csv"))
            self.import_flights(os.path.join("data", "flights.csv"))
            print("All CSV files imported successfully.")
        except Exception as e:
            print("An error has occurred while importing default CSV files.", e)

# ------------------------------------------------------------
# Crew Allocation System
# ------------------------------------------------------------
# Automatically assigns flight crew members based on aircraft
# capacity and employee job roles.
#
# Crew categories include:
#   • Pilots
#   • Cabin crew / flight attendants
#   • Mechanics
#   • Ground staff
#
# Random selection ensures balanced distribution of staff
# across flights.
# ------------------------------------------------------------


import random


class CrewAllocator:

    def __init__(self, cursor, connection):
        self.get_cursor = cursor
        self.get_connection = connection

    def assign_flight_crew(self, flight_id, capacity):

        pilots = self.get_cursor.execute("""
        SELECT Employee_Id FROM Employee
        WHERE Job_title LIKE '%Pilot%'
        """).fetchall()

        cabin = self.get_cursor.execute("""
        SELECT Employee_Id FROM Employee
        WHERE Job_title LIKE '%Cabin%'
           OR Job_title LIKE '%Attendant%'
        """).fetchall()

        mechanics = self.get_cursor.execute("""
        SELECT Employee_Id FROM Employee
        WHERE Job_title LIKE '%Mechanic%'
        """).fetchall()

        ground = self.get_cursor.execute("""
        SELECT Employee_Id FROM Employee
        WHERE Job_title LIKE '%Ground%'
        """).fetchall()

        if capacity < 150:
            p = 2
            c = 4
            m = 1
            g = 1

        elif capacity < 220:
            p = 2
            c = 6
            m = 2
            g = 2

        else:
            p = 3
            c = random.randint(8,10)
            m = random.randint(2,3)
            g = 2

        crew = []

        crew += random.sample(pilots, min(p, len(pilots)))
        crew += random.sample(cabin, min(c, len(cabin)))
        crew += random.sample(mechanics, min(m, len(mechanics)))
        crew += random.sample(ground, min(g, len(ground)))

        for emp in crew:

            self.get_cursor.execute("""
            INSERT INTO FlightCrew (Flight_Id, Employee_Id, Role)
            VALUES (?, ?, ?)
            """,(flight_id, emp[0], "Assigned"))

        self.get_connection.commit()


# ------------------------------------------------------------
# Input Helper Utility Class
# ------------------------------------------------------------
# Provides reusable helper functions for user input
# validation within the command-line interface.
#
# Functions include:
#   • Non-empty string input validation
#   • Integer input validation
#   • Float input validation
#   • Pause utility for menu navigation
# ------------------------------------------------------------




class InputHelper:

    @staticmethod
    def prompt_non_empty(message):
        value = input(message).strip()
        while value == "":
            print("Value cannot be blank.")
            value = input(message).strip()
        return value

    @staticmethod
    def prompt_int(message):
        while True:
            value = input(message).strip()
            try:
                return int(value)
            except Exception:
                print("Please enter a valid integer.")

    @staticmethod
    def prompt_float(message):
        while True:
            value = input(message).strip()
            try:
                return float(value)
            except Exception:
                print("Please enter a valid number.")

    @staticmethod
    def pause():
        input("\nPress Enter to continue...")



# ------------------------------------------------------------
# Main Application Controller
# ------------------------------------------------------------
# This class represents the main command-line interface
# of the AirAsia Ticketing System.
#
# Responsibilities:
#   • Display the main system menu
#   • Route user selections to appropriate modules
#   • Coordinate interactions between database classes
#   • Manage system utilities and reports
#
# The run() function starts the interactive program loop.
# ------------------------------------------------------------





class AirAsiaProject:
    """
    Interactive application class.

    """

    def __init__(self):
        self.airport = Airport()
        self.aircraft = Aircraft()
        self.employee = Employee()
        self.customer = Customer()
        self.flight = Flight()
        self.ticket = Ticket()
        self.report = Report()
        self.importer = CSVImporter()
        self.db = ProjectDB()






    def search_and_select(self, rows, headers, widths, prompt_message="Enter value to continue: "):

        if not rows:
            print("No records found.")
            return None

        header_line = ""
        for h, w in zip(headers, widths):
            header_line += f"{h:<{w}} "

        print(header_line)
        print("-" * sum(widths))

        for r in rows:
            line = ""
            for v, w in zip(r, widths):
                line += f"{str(v):<{w}} "
            print(line)

        return InputHelper.prompt_non_empty(prompt_message)


    def show_main_menu(self):

        if os.name == "nt":
            os.system("cls")
        elif "TERM" in os.environ:
            os.system("clear")

        print("\n" + "=" * 60)
        print(f"{'AIRASIA TICKETING SYSTEM':^60}")
        print("=" * 60)

        print("\n" + "-" * 60)
        print(f"{'OPERATIONS':^60}")
        print("-" * 60)

        print(f"{'1':>3}  {'Airport Management':<40}")
        print(f"{'2':>3}  {'Aircraft Management':<40}")
        print(f"{'3':>3}  {'Employee Management':<40}")
        print(f"{'4':>3}  {'Customer Management':<40}")
        print(f"{'5':>3}  {'Flight Management':<40}")
        print(f"{'6':>3}  {'Ticket Management':<40}")

        print("\n" + "-" * 60)
        print(f"{'REPORTS':^60}")
        print("-" * 60)

        print(f"{'7':>3}  {'Flight Sales Report':<40}")
        print(f"{'8':>3}  {'Employee Flight Report':<40}")
        print(f"{'9':>3}  {'Passenger Manifest':<40}")
        print(f"{'10':>3} { 'Flight Crew Report':<40}")

        print("\n" + "-" * 60)
        print(f"{'SYSTEM UTILITIES':^60}")
        print("-" * 60)

        print(f"{'11':>3} {'Reset Database':<40}")
        print(f"{'12':>3} {'Import Sample CSV Data':<40}")

        print("\n" + "-" * 60)
        print(f"{'0':>3}  {'Exit System':<40}")
        print("-" * 60)

    def run(self):
        user_selection = ""

        while user_selection != "0":
            self.show_main_menu()
            user_selection = input("\nSelect an option: ").strip()

            if user_selection == "1":
                self.airport_menu()

            elif user_selection == "2":
                self.aircraft_menu()

            elif user_selection == "3":
                self.employee_menu()

            elif user_selection == "4":
                self.customer_menu()

            elif user_selection == "5":
                self.flight_menu()

            elif user_selection == "6":
                self.ticket_menu()

            elif user_selection == "7":
                self.flight_sales_report_menu()

            elif user_selection == "8":
                self.employee_flight_report_menu()

            elif user_selection == "9":
                self.passenger_manifest_menu()

            elif user_selection == "10":
                self.flight_crew_report_menu()

            elif user_selection == "11":
                self.reset_database_menu()

            elif user_selection == "12":
                self.import_csv_menu()

            elif user_selection == "0":
                print("Thank you for using the AirAsia Ticketing System.")

            else:
                print("Invalid selection. Please try again.")

    # ------------------------------------------------------------
    # Airport Management Menu
    # Provides interactive options for managing airport data.
    # ------------------------------------------------------------
    def airport_menu(self):

        while True:
            print("\n--- AIRPORT ---")
            print("\n1 - View all airports")
            print("2 - View airport by code/ Name/ City/ Country")
            print("3 - Add airport")
            print("4 - Update airport")
            print("5 - Delete airport")
            print("0 - Return to main menu")

            choice = input("\nSelect option: ").strip()

            if choice == "1":
                rows = self.airport.fetch()

                print(f"{'CODE':<10} {'AIRPORT NAME':<60} {'CITY':<30} {'COUNTRY':<20}")
                print("-" * 120)

                for row in rows:
                    print(f"{row[0]:<10} {row[1]:<60} {row[2]:<30} {row[3]:<20}")
                InputHelper.pause()


            elif choice == "2":
                keyword = InputHelper.prompt_non_empty(
                    "Search airport by code, name, city, or country: "
                )
                rows = self.airport.search_locations(keyword)
                if not rows:
                    print("No airports found.")
                else:
                    print(f"{'CODE':<10} {'NAME':<40} {'CITY':<20} {'COUNTRY':<20}")
                    print("-" * 90)
                    for row in rows:
                        print(f"{row[0]:<10} {row[1]:<40} {row[2]:<20} {row[3]:<20}")
                InputHelper.pause()


            elif choice == "3":
                code = InputHelper.prompt_non_empty("Airport code: ")
                name = InputHelper.prompt_non_empty("Airport name: ")
                city = InputHelper.prompt_non_empty("City: ")
                country = InputHelper.prompt_non_empty("Country: ")
                self.airport.add(code, name, city, country)
                InputHelper.pause()

            elif choice == "4":
                keyword = InputHelper.prompt_non_empty(
                    "Search airport by code, name, city, or country to update: "
                )
                rows = self.airport.search_locations(keyword)
                airport_code = self.search_and_select(
                    rows,
                    ["CODE", "NAME", "CITY", "COUNTRY"],
                    [10, 40, 20, 20],
                    "Enter Airport CODE to continue: "
                )
                if not airport_code:
                    return
                name = InputHelper.prompt_non_empty("New airport name: ")
                city = InputHelper.prompt_non_empty("New city: ")
                country = InputHelper.prompt_non_empty("New country: ")
                self.airport.update(airport_code, name, city, country)
                InputHelper.pause()


            elif choice == "5":
                code = InputHelper.prompt_non_empty("Airport code to delete: ")
                self.airport.delete(code)
                InputHelper.pause()



            elif choice == "0":

                return


            else:

                print("Invalid selection. Please try again.")



    # -------------------------
    # Aircraft menu
    # -------------------------
    def aircraft_menu(self):
        while True:
            print("\n--- AIRCRAFT ---")
            print("\n1 - View all aircraft")
            print("2 - Search aircraft (ID or type)")
            print("3 - Add aircraft")
            print("4 - Update aircraft")
            print("5 - Delete aircraft")
            print("0 - Return to main menu")

            choice = input("\nSelect option: ").strip()

            if choice == "1":
                rows = self.aircraft.fetch()

                print(f"{'ID':<6} {'TYPE':<25} {'CAPACITY':<10}")
                print("-" * 45)

                for row in rows:
                    print(f"{row[0]:<6} {row[1]:<25} {row[2]:<10}")
                InputHelper.pause()


            elif choice == "2":
                keyword = InputHelper.prompt_non_empty(
                    "Search by aircraft ID or aircraft type (Airbus/Boeing/ATR): "
                    )
                if keyword.isdigit():
                    row = self.aircraft.fetch(aircraft_id=int(keyword))
                    if row:
                        print(f"{'ID':<6} {'TYPE':<25} {'CAPACITY':<10}")
                        print("-" * 45)
                        print(f"{row[0]:<6} {row[1]:<25} {row[2]:<10}")
                    else:
                        print("Aircraft not found.")
                else:
                    rows = self.aircraft.fetch(keyword=keyword)
                    if rows:
                        print(f"{'ID':<6} {'TYPE':<25} {'CAPACITY':<10}")
                        print("-" * 45)
                        for row in rows:
                            print(f"{row[0]:<6} {row[1]:<25} {row[2]:<10}")
                    else:
                        print("No aircraft found.")
                InputHelper.pause()



            elif choice == "3":
                aircraft_type = InputHelper.prompt_non_empty("Aircraft type: ")
                capacity = InputHelper.prompt_int("Capacity: ")
                self.aircraft.add(aircraft_type, capacity)
                InputHelper.pause()




            elif choice == "4":
                keyword = InputHelper.prompt_non_empty(
                    "Search aircraft by ID, type, or capacity: "
                )
                rows = self.aircraft.fetch(keyword=keyword)
                aircraft_id = self.search_and_select(
                    rows,
                    ["ID", "TYPE", "CAPACITY"],
                    [6, 25, 10],
                    "Enter Aircraft ID to continue: "
                )
                if not aircraft_id:
                    return
                aircraft_type = InputHelper.prompt_non_empty("New aircraft type: ")
                capacity = InputHelper.prompt_int("New capacity: ")
                self.aircraft.update(int(aircraft_id), aircraft_type, capacity)
                InputHelper.pause()


            elif choice == "5":
                aircraft_id = InputHelper.prompt_int("Aircraft ID to delete: ")
                self.aircraft.delete(aircraft_id)
                InputHelper.pause()



            elif choice == "0":

                return


            else:

                print("Invalid selection. Please try again.")


    # -------------------------
    # Employee menu
    # -------------------------
    def employee_menu(self):
        while True:
            print("\n--- EMPLOYEE ---")
            print("\n1 - View all employees")
            print("2 - Search employee (by-ID / name / job title)")
            print("3 - Add employee")
            print("4 - Update employee")
            print("5 - Delete employee")
            print("0 - Return to main menu")

            choice = input("\nSelect option: ").strip()

            if choice == "1":
                rows = self.employee.fetch()

                print(f"{'ID':<6} {'FIRST NAME':<20} {'LAST NAME':<20} {'JOB TITLE':<25}")
                print("-" * 75)

                for row in rows:
                    print(f"{row[0]:<6} {row[1]:<20} {row[2]:<20} {row[3]:<25}")
                InputHelper.pause()


            elif choice == "2":
                keyword = InputHelper.prompt_non_empty(
                    "Search by employee ID, first name, last name, or job title: "
                )
                if keyword.isdigit():
                    row = self.employee.fetch(employee_id=int(keyword))
                    if row:
                        print(f"{'ID':<6} {'FIRST NAME':<20} {'LAST NAME':<20} {'JOB TITLE':<25}")
                        print("-" * 75)
                        print(f"{row[0]:<6} {row[1]:<20} {row[2]:<20} {row[3]:<25}")
                    else:
                        print("Employee not found.")

                else:
                    rows = self.employee.fetch(keyword=keyword)
                    if rows:
                        print(f"{'ID':<6} {'FIRST NAME':<20} {'LAST NAME':<20} {'JOB TITLE':<25}")
                        print("-" * 75)
                        for row in rows:
                            print(f"{row[0]:<6} {row[1]:<20} {row[2]:<20} {row[3]:<25}")
                    else:
                        print("No matching employees found.")
                InputHelper.pause()

            elif choice == "3":
                first_name = InputHelper.prompt_non_empty("First name: ")
                last_name = InputHelper.prompt_non_empty("Last name: ")
                job_title = InputHelper.prompt_non_empty("Job title: ")
                self.employee.add(first_name, last_name, job_title)
                InputHelper.pause()


            elif choice == "4":
                keyword = InputHelper.prompt_non_empty(
                    "Search employee by ID, first name, or last name: "
                )
                if keyword.isdigit():
                    rows = [self.employee.fetch(employee_id=int(keyword))]
                else:
                    rows = self.employee.fetch(keyword=keyword)
                if not rows:
                    print("No employees found.")
                    InputHelper.pause()
                    return
                print(f"{'ID':<6} {'FIRST NAME':<20} {'LAST NAME':<20} {'JOB TITLE':<25}")
                print("-" * 75)
                for row in rows:
                    print(f"{row[0]:<6} {row[1]:<20} {row[2]:<20} {row[3]:<25}")
                employee_id = InputHelper.prompt_int("Enter Employee ID to update: ")
                first_name = InputHelper.prompt_non_empty("New first name: ")
                last_name = InputHelper.prompt_non_empty("New last name: ")
                job_title = InputHelper.prompt_non_empty("New job title: ")
                self.employee.update(employee_id, first_name, last_name, job_title)
                InputHelper.pause()


            elif choice == "5":
                employee_id = InputHelper.prompt_int("Employee ID to delete: ")
                self.employee.delete(employee_id)
                InputHelper.pause()



            elif choice == "0":

                return


            else:

                print("Invalid selection. Please try again.")



    # -------------------------
    # Customer menu
    # -------------------------
    def customer_menu(self):
        while True:
            print("\n--- CUSTOMER ---")
            print("\n1 - View all customers")
            print("2 - Search customer")
            print("3 - Add customer")
            print("4 - Update customer")
            print("5 - Delete customer")
            print("0 - Return to main menu")

            choice = input("\nSelect option: ").strip()

            if choice == "1":
                rows = self.customer.fetch()

                print(
                    f"{'ID':<5} {'TITLE':<6} {'FIRST':<12} {'LAST':<12} {'GENDER':<8} "
                    f"{'DOB':<12} {'CITIZENSHIP':<15} {'PHONE':<15} {'EMAIL':<25} "
                    f"{'PASSPORT':<15} {'EXPIRY':<12}"
                )
                print("-" * 150)

                for row in rows:
                    print(
                        f"{row[0]:<5} {row[1]:<6} {row[2]:<12} {row[3]:<12} {row[4]:<8} "
                        f"{row[5]:<12} {row[6]:<15} {row[7]:<15} {row[8]:<25} "
                        f"{row[9]:<15} {row[10]:<12}"
                    )
                InputHelper.pause()


            elif choice == "2":
                keyword = InputHelper.prompt_non_empty(
                    "Search by ID, first name, last name, phone, or email: "
                )
                rows = self.customer.fetch(keyword=keyword)
                if rows:
                    print(
                        f"{'ID':<5} {'TITLE':<6} {'FIRST':<12} {'LAST':<12} {'GENDER':<8} {'DOB':<12} {'CITIZENSHIP':<15} {'PHONE':<15} {'EMAIL':<25} {'PASSPORT':<15} {'EXPIRY':<12}"
                    )
                    print("-" * 150)
                    for row in rows:
                        print(
                            f"{row[0]:<5} {row[1]:<6} {row[2]:<12} {row[3]:<12} {row[4]:<8} {row[5]:<12} "
                            f"{row[6]:<15} {row[7]:<15} {row[8]:<25} {row[9]:<15} {row[10]:<12}"
                        )
                else:
                    print("No matching customers found.")
                InputHelper.pause()


            elif choice == "3":

                title = InputHelper.prompt_non_empty("Title: ")
                first_name = InputHelper.prompt_non_empty("First name: ")
                last_name = InputHelper.prompt_non_empty("Last name: ")
                gender = InputHelper.prompt_non_empty("Gender: ")
                dob = InputHelper.prompt_non_empty("Date of birth (MM/DD/YY): ")
                citizenship = InputHelper.prompt_non_empty("Citizenship: ")
                phone = InputHelper.prompt_non_empty("Phone number: ")
                email = InputHelper.prompt_non_empty("Email: ")
                passport_number = InputHelper.prompt_non_empty("Passport number: ")
                passport_expiry = InputHelper.prompt_non_empty("Passport expiry (MM/DD/YY): ")
                self.customer.add(
                    title, first_name, last_name, gender, dob,
                    citizenship, phone, email, passport_number, passport_expiry
                )
                InputHelper.pause()



            elif choice == "4":
                keyword = InputHelper.prompt_non_empty(
                    "Search customer by ID, name, phone, email or passport: "
                )
                rows = self.customer.fetch(keyword=keyword)
                customer_id = self.search_and_select(
                    rows,
                    ["ID", "TITLE", "FIRST", "LAST", "PHONE", "EMAIL"],
                    [5, 6, 12, 12, 15, 25],
                    "Enter Customer ID to update: "
                )
                if not customer_id:
                    return

                title = InputHelper.prompt_non_empty("New title: ")
                first = InputHelper.prompt_non_empty("New first name: ")
                last = InputHelper.prompt_non_empty("New last name: ")
                dob = InputHelper.prompt_non_empty("New DOB: ")
                citizenship = InputHelper.prompt_non_empty("New citizenship: ")
                email = InputHelper.prompt_non_empty("New email: ")
                self.customer.update(customer_id, title, first, last, dob, citizenship, email)
                InputHelper.pause()

            elif choice == "5":
                customer_id = InputHelper.prompt_int("Customer ID to delete: ")
                self.customer.delete(customer_id)
                InputHelper.pause()



            elif choice == "0":

                return


            else:

                print("Invalid selection. Please try again.")

    # ------------------------------------------------------------
    # Flight Management Menu
    # ------------------------------------------------------------
    # Provides options to manage flight schedules within the system.
    # Users can:
    #   • View all scheduled flights with aircraft and seat details
    #   • Search flights by ID, airport code, or city
    #   • Add new flight schedules
    #   • Update existing flight information
    #   • Delete flight records
    #
    # Dynamic ticket pricing is calculated using the pricing engine
    # based on flight duration, aircraft type, departure time, and date.
    # ------------------------------------------------------------



    # -------------------------
    # Flight menu
    # -------------------------

    def flight_menu(self):
        while True:

            print("\n--- FLIGHT ---")
            print("\n1 - View all flights")
            print("2 - Search flights (ID / airport / city)")
            print("3 - Add flight")
            print("4 - Update flight")
            print("5 - Delete flight")
            print("0 - Return to main menu")

            from pricing_engine import calculate_dynamic_price

            choice = input("\nSelect option: ").strip()

            if choice == "1":
                rows = self.flight.fetch_detailed()

                print(f"{'ID':<5} {'DATE':<12} {'DEP TIME':<10} {'FROM':<6} {'CITY':<15} {'TO':<6} {'CITY':<15} {'AIRCRAFT TYPE':<20} {'SEATS':<6} {'CREW':<6} {'DEP GATE':<10} {'ARR GATE':<10} {'DURATION':<10} {'PRICE':<10}")
                print("-" * 150)

                for row in rows:
                    flight_id = row[0]
                    dep_date = row[1]
                    dep_time = row[2]
                    aircraft = row[7]
                    duration = row[11]

                    price = calculate_dynamic_price(duration, aircraft, dep_time, dep_date)

                    crew = row[12]

                    print(
                        f"{row[0]:<5} {row[1]:<12} {row[2]:<10} {row[3]:<6} {row[4]:<15} "
                        f"{row[5]:<6} {row[6]:<15} {row[7]:<20} {row[8]:<6} {crew:<6} "
                        f"{row[9]:<10} {row[10]:<10} {row[11]:<10} ${price:<8.2f}"
                    )
                InputHelper.pause()



            elif choice == "2":
                origin = InputHelper.prompt_non_empty(
                    "Search flights departing from (Flight ID / airport code / city): "
                )
                destination = input(
                    "Optional destination filter (airport code / city) - press Enter to skip: "
                ).strip()
                rows = self.flight.search(origin, destination)
                if not rows:
                    print("No matching flights found.")
                else:
                    print(
                        f"{'ID':<5} {'DATE':<12} {'DEP TIME':<10} {'FROM':<6} {'CITY':<15} "
                        f"{'TO':<6} {'CITY':<15} {'AIRCRAFT TYPE':<20} {'SEATS':<5} "
                        f"{'DEP GATE':<10} {'ARR GATE':<10} {'DURATION':<10} {'PRICE':<10}"
                    )
                    print("-" * 150)
                    for row in rows:
                        dep_date = row[1]
                        dep_time = row[2]
                        aircraft = row[7]
                        duration = row[11]
                        price = calculate_dynamic_price(duration, aircraft, dep_time, dep_date)
                        print(
                            f"{row[0]:<5} {row[1]:<12} {row[2]:<10} {row[3]:<6} {row[4]:<15} "
                            f"{row[5]:<6} {row[6]:<15} {row[7]:<20} {row[8]:<5} "
                            f"{row[9]:<10} {row[10]:<10} {row[11]:<10} ${price:<8.2f}"
                        )
                InputHelper.pause()

            elif choice == "3":
                airport_from = InputHelper.prompt_non_empty("From airport code: ")
                airport_to = InputHelper.prompt_non_empty("To airport code: ")
                aircraft_id = InputHelper.prompt_int("Aircraft ID: ")
                departure_date = InputHelper.prompt_non_empty("Departure date (MM/DD/YY): ")
                departure_time = InputHelper.prompt_non_empty("Departure time (HH:MM): ")
                departure_gate = InputHelper.prompt_non_empty("Departure gate: ")
                arrival_gate = InputHelper.prompt_non_empty("Arrival gate: ")
                duration = InputHelper.prompt_int("Duration in minutes: ")
                employee_id = InputHelper.prompt_int("Assigned employee ID: ")
                self.flight.add(
                    airport_from, airport_to, aircraft_id, departure_date,
                    departure_time, departure_gate, arrival_gate, duration, employee_id
                )
                InputHelper.pause()


            elif choice == "4":
                keyword = InputHelper.prompt_non_empty(
                    "Search flight by airport, date, or ID: "
                )
                rows = self.flight.search(keyword)
                flight_id = self.search_and_select(
                    rows,
                    ["ID", "DATE", "TIME", "FROM", "CITY", "TO", "CITY", "AIRCRAFT"],
                    [5, 12, 8, 6, 15, 6, 15, 20],
                    "Enter Flight ID to update: "
                )

                if not flight_id:
                    return

                airport_from = InputHelper.prompt_non_empty("New from airport code: ")
                airport_to = InputHelper.prompt_non_empty("New to airport code: ")
                aircraft_id = InputHelper.prompt_int("New aircraft ID: ")
                departure_date = InputHelper.prompt_non_empty("New departure date (MM/DD/YY): ")
                departure_time = InputHelper.prompt_non_empty("New departure time (HH:MM): ")
                departure_gate = InputHelper.prompt_non_empty("New departure gate: ")
                arrival_gate = InputHelper.prompt_non_empty("New arrival gate: ")
                duration = InputHelper.prompt_int("New duration in minutes: ")
                employee_id = InputHelper.prompt_int("New assigned employee ID: ")
                self.flight.update(
                    flight_id, airport_from, airport_to, aircraft_id, departure_date,
                    departure_time, departure_gate, arrival_gate, duration, employee_id
                )
                InputHelper.pause()

            elif choice == "5":
                flight_id = InputHelper.prompt_int("Flight ID to delete: ")
                self.flight.delete(flight_id)
                InputHelper.pause()



            elif choice == "0":

                return


            else:

                print("Invalid selection. Please try again.")

    # ------------------------------------------------------------
    # Ticket Management Menu
    # ------------------------------------------------------------
    # Handles ticket-related operations for passengers.
    #
    # Available functions:
    #   • View all purchased tickets
    #   • Search tickets by ticket number, customer name, or flight
    #   • Search available flights
    #   • Purchase new tickets
    #   • Update or rebook tickets
    #   • Cancel existing tickets
    #
    # The system ensures flight capacity limits are respected and
    # dynamically calculates ticket prices before purchase.
    # ------------------------------------------------------------

    # -------------------------
    # Ticket menu
    # -------------------------

    def ticket_menu(self):

        while True:
            print("\n--- TICKET MANAGEMENT ---")
            print("\n1 - View all tickets")
            print("2 - Search ticket")
            print("3 - Search flights")
            print("4 - Purchase ticket")
            print("5 - Update ticket")
            print("6 - Cancel ticket")
            print("0 - Return to main menu")

            choice = input("\nSelect option: ").strip()

            # --------------------------------------------------
            # VIEW ALL TICKETS
            # --------------------------------------------------

            if choice == "1":

                rows = self.ticket.fetch_detailed()

                if not rows:
                    print("No tickets found.")
                    InputHelper.pause()
                    continue

                print(
                    f"{'TICKET':<8} {'CUS ID':<7} {'CUSTOMER NAME':<25} "
                    f"{'FLIGHT':<7} {'FROM':<6} {'TO':<6} {'DATE':<12} "
                    f"{'TIME':<8} {'COST':<10} {'PURCHASE DATE':<15}"
                )
                print("-" * 120)

                for row in rows:
                    print(
                        f"{row[0]:<8} {row[1]:<7} {row[2]:<25} {row[3]:<7} "
                        f"{row[4]:<6} {row[5]:<6} {row[6]:<12} {row[7]:<8} "
                        f"${row[8]:<9.2f} {row[9]:<15}"
                    )

                InputHelper.pause()

            # --------------------------------------------------
            # SEARCH TICKET
            # --------------------------------------------------

            elif choice == "2":

                keyword = InputHelper.prompt_non_empty(
                    "Search ticket by Ticket Number, Customer Name, Flight ID, From, or To: "
                )

                rows = self.ticket.search(keyword)

                if not rows:
                    print("No tickets found.")
                    InputHelper.pause()
                    continue

                print(
                    f"{'TICKET':<8} {'CUSTOMER':<25} {'FLIGHT':<7} "
                    f"{'FROM':<6} {'TO':<6} {'DATE':<12} {'TIME':<8} {'COST':<10}"
                )
                print("-" * 90)

                for row in rows:
                    print(
                        f"{row[0]:<8} {row[2]:<25} {row[3]:<7} "
                        f"{row[4]:<6} {row[5]:<6} {row[6]:<12} {row[7]:<8} "
                        f"${row[8]:<9.2f}"
                    )

                InputHelper.pause()

            # --------------------------------------------------
            # SEARCH FLIGHTS
            # --------------------------------------------------

            elif choice == "3":

                self.search_flights_menu()
                continue

            # --------------------------------------------------
            # PURCHASE TICKET
            # --------------------------------------------------

            elif choice == "4":

                self.purchase_ticket_menu()
                continue

            # --------------------------------------------------
            # UPDATE / REBOOK TICKET
            # --------------------------------------------------

            elif choice == "5":

                rows = self.ticket.fetch_detailed()

                if not rows:
                    print("No tickets available to update.")
                    InputHelper.pause()
                    continue

                ticket_number = self.search_and_select(
                    rows,
                    ["TICKET", "CUS ID", "CUSTOMER NAME", "FLIGHT", "FROM", "TO", "DATE", "TIME", "COST",
                     "PURCHASE DATE"],
                    [8, 7, 25, 7, 6, 6, 12, 8, 10, 15],
                    "Enter Ticket Number to continue: "
                )

                if not ticket_number:
                    InputHelper.pause()
                    continue

                ticket_number = int(ticket_number)
                ticket_row = self.ticket.fetch_detailed(ticket_number=ticket_number)

                if not ticket_row:
                    print("Ticket not found.")
                    InputHelper.pause()
                    continue

                print("\nSelected Ticket:")
                print(
                    f"{'TICKET':<8} {'CUS ID':<7} {'CUSTOMER NAME':<25} "
                    f"{'FLIGHT':<7} {'FROM':<6} {'TO':<6} {'DATE':<12} "
                    f"{'TIME':<8} {'COST':<10} {'PURCHASE DATE':<15}"
                )
                print("-" * 120)

                print(
                    f"{ticket_row[0]:<8} {ticket_row[1]:<7} {ticket_row[2]:<25} "
                    f"{ticket_row[3]:<7} {ticket_row[4]:<6} {ticket_row[5]:<6} "
                    f"{ticket_row[6]:<12} {ticket_row[7]:<8} "
                    f"${ticket_row[8]:<9.2f} {ticket_row[9]:<15}"
                )

                print("\nWhat would you like to do?")
                print("1 - Cancel and refund ticket")
                print("2 - Rebook to alternate flight")
                print("0 - Return")

                update_choice = input("Select option: ").strip()

                # --------------------------------------------
                # CANCEL
                # --------------------------------------------

                if update_choice == "1":

                    self.ticket.cancel_ticket(ticket_number)
                    print("Ticket cancelled successfully.")
                    InputHelper.pause()

                # --------------------------------------------
                # REBOOK
                # --------------------------------------------

                elif update_choice == "2":

                    from pricing_engine import calculate_dynamic_price

                    customer_id = ticket_row[1]
                    old_cost = float(ticket_row[8])

                    print("\n--- SEARCH ALTERNATE FLIGHTS ---")

                    origin = InputHelper.prompt_non_empty(
                        "New origin (airport code / city / country): "
                    )

                    destination = InputHelper.prompt_non_empty(
                        "New destination (airport code / city / country): "
                    )

                    date = input("New departure date (optional, (MM/DD/YY): ").strip()

                    rows = self.flight.search_direct_flights(
                        origin,
                        destination,
                        date if date else None
                    )

                    if not rows:
                        print("No alternate flights found.")
                        InputHelper.pause()
                        continue

                    print(
                        f"{'OPT':<4} {'FLIGHT':<6} {'DATE':<12} {'TIME':<8} "
                        f"{'FROM':<6} {'CITY':<18} {'TO':<6} {'CITY':<18} "
                        f"{'AIRCRAFT':<20} {'SEATS':<7} {'DURATION':<10} {'PRICE':<10}"
                    )
                    print("-" * 140)

                    priced_rows = []

                    for i, row in enumerate(rows, start=1):
                        flight_id = row[0]
                        dep_date = row[1]
                        dep_time = row[2]
                        origin_code = row[3]
                        origin_city = row[4]
                        dest_code = row[5]
                        dest_city = row[6]
                        aircraft = row[7]
                        seats = row[8]
                        duration = row[9]

                        price = calculate_dynamic_price(duration, aircraft, dep_time, dep_date)

                        priced_rows.append((row, price))

                        print(
                            f"{i:<4} {flight_id:<6} {dep_date:<12} {dep_time:<8} "
                            f"{origin_code:<6} {origin_city:<18} {dest_code:<6} {dest_city:<18} "
                            f"{aircraft:<20} {seats:<7} {duration:<10} ${price:<8.2f}"
                        )

                    opt = InputHelper.prompt_int("Select alternate flight option: ")

                    if opt < 1 or opt > len(priced_rows):
                        print("Invalid option.")
                        InputHelper.pause()
                        continue

                    selected_row, new_price = priced_rows[opt - 1]
                    new_flight_id = selected_row[0]

                    diff = new_price - old_cost

                    print(f"\nOld ticket price : ${old_cost:.2f}")
                    print(f"New ticket price : ${new_price:.2f}")

                    if diff > 0:
                        print(f"Additional fare to collect: ${diff:.2f}")
                    elif diff < 0:
                        print(f"Refund amount: ${abs(diff):.2f}")
                    else:
                        print("No fare difference.")

                    confirm = input("Confirm rebooking? (y/n): ").strip().lower()

                    if confirm != "y":
                        print("Rebooking cancelled.")
                        InputHelper.pause()
                        continue

                    self.ticket.delete(ticket_number)
                    self.ticket.purchase_ticket(customer_id, new_flight_id, new_price)

                    print("Alternate flight booked successfully.")

                    InputHelper.pause()

            # --------------------------------------------------
            # CANCEL DIRECTLY
            # --------------------------------------------------

            elif choice == "6":

                ticket_number = InputHelper.prompt_int("Ticket number to cancel: ")
                self.ticket.cancel_ticket(ticket_number)
                InputHelper.pause()

            # --------------------------------------------------

            elif choice == "0":
                return

            else:
                print("Invalid selection. Please try again.")



    # -------------------------
    # Customer use cases
    # -------------------------

    # ------------------------------------------------------------
    # Flight Search Interface
    # ------------------------------------------------------------
    # Allows users to search available flights using flexible
    # location inputs including:
    #   • Airport code
    #   • Airport name
    #   • City
    #   • Country
    #
    # The system displays matching direct flights along with
    # aircraft type, available seats, duration, and calculated
    # ticket price.
    # ------------------------------------------------------------


    def search_flights_menu(self):

        print("\n--- SEARCH FLIGHTS ---")

        print("\nPassengers can search by:")
        print("City (Bangkok)")
        print("Country (Thailand)")
        print("Airport name (Changi)")
        print("Airport code (SIN)")

        from pricing_engine import calculate_dynamic_price

        from_location = InputHelper.prompt_non_empty("From location: ")
        to_location = InputHelper.prompt_non_empty("To location: ")

        departure_date = input("Departure date (MM/DD/YY) optional: ").strip()

        rows = self.flight.search_flights_any_location(
            from_location,
            to_location,
            departure_date if departure_date else None
        )

        if rows:

            print(
                f"{'ID':<5} {'DATE':<12} {'TIME':<8} {'FROM':<6} {'CITY':<18} {'TO':<6} {'CITY':<18} {'AIRCRAFT':<20} {'SEATS':<7} {'DURATION (in_Min)':<10} {'PRICE':<20}")
            print("-" * 140)

            for row in rows:
                duration = row[9]
                aircraft = row[7]
                dep_time = row[2]
                dep_date = row[1]

                price = calculate_dynamic_price(duration, aircraft, dep_time, dep_date)

                print(
                    f"{row[0]:<5} {row[1]:<12} {row[2]:<8} {row[3]:<6} {row[4]:<18} {row[5]:<6} {row[6]:<18} {row[7]:<20} {row[8]:<7} {row[9]:<10} ${price:<20.2f}")

        else:
            print("No flights found.")

        InputHelper.pause()

    # ------------------------------------------------------------
    # Ticket Purchase Workflow
    # ------------------------------------------------------------
    # Guides the user through the ticket purchasing process.
    #
    # Steps include:
    #   • Searching available flights
    #   • Selecting a flight
    #   • Choosing a registered customer
    #   • Calculating ticket price dynamically
    #   • Confirming and completing the booking
    #
    # The system prevents overbooking by checking remaining
    # seat availability before finalizing the purchase.
    # ------------------------------------------------------------


    def purchase_ticket_menu(self):

            from pricing_engine import calculate_dynamic_price

            while True:

                print("\n--- PURCHASE FLIGHT TICKET ---")
                print("\n1 - Search available flights")
                print("2 - Select flight and purchase ticket")
                print("0 - Return")

                choice = input("\nSelect option: ").strip()


                # -------------------------------------------------
                # OPTION 1 : SEARCH FLIGHTS
                # -------------------------------------------------

                if choice == "1":

                    print("\nPassengers can search by:")
                    print("City (Bangkok)")
                    print("Country (Thailand)")
                    print("Airport name (Changi)")
                    print("Airport code (SIN)")

                    origin = InputHelper.prompt_non_empty(
                        "Origin (city / country / airport / code): "
                    )
                    destination = input(
                        "Destination (optional – press Enter to show all routes): "
                    ).strip()

                    date = input("Departure date (MM/DD/YY) optional: ").strip()

                    rows = self.flight.search(origin, destination if destination else None)

                    if not rows:
                        print("No flights found.")
                        InputHelper.pause()
                        continue

                    print(
                        f"{'OPT':<4} {'FLIGHT':<6} {'DATE':<12} {'TIME':<8} "
                        f"{'FROM':<6} {'CITY':<18} {'TO':<6} {'CITY':<18} "
                        f"{'AIRCRAFT':<20} {'SEATS':<7} {'DURATION':<10} {'PRICE':<10}"
                    )
                    print("-" * 140)

                    for i, row in enumerate(rows, start=1):
                        flight_id = row[0]
                        dep_date = row[1]
                        dep_time = row[2]
                        origin_code = row[3]
                        origin_city = row[4]
                        dest_code = row[5]
                        dest_city = row[6]
                        aircraft = row[7]
                        seats = row[8]
                        duration = row[11]

                        price = calculate_dynamic_price(duration, aircraft, dep_time, dep_date)

                        print(
                            f"{i:<4} {flight_id:<6} {dep_date:<12} {dep_time:<8} "
                            f"{origin_code:<6} {origin_city:<18} {dest_code:<6} {dest_city:<18} "
                            f"{aircraft:<20} {seats:<7} {duration:<10} ${price:<8.2f}"
                        )

                    InputHelper.pause()

                # ------------------------------------------------------------
                # Ticket Purchase Workflow
                # ------------------------------------------------------------
                # Guides the user through the ticket purchasing process.
                #
                # Steps include:
                #   • Searching available flights
                #   • Selecting a flight
                #   • Choosing a registered customer
                #   • Calculating ticket price dynamically
                #   • Confirming and completing the booking
                #
                # The system prevents overbooking by checking remaining
                # seat availability before finalizing the purchase.
                # ------------------------------------------------------------

                # -------------------------------------------------
                # OPTION 2 : PURCHASE TICKET
                # -------------------------------------------------

                elif choice == "2":

                    flight_id = InputHelper.prompt_int("Enter Flight ID to book: ")

                    remaining = self.flight.seats_remaining(flight_id)

                    if remaining is None:
                        print("Flight not found.")
                        InputHelper.pause()
                        continue

                    if remaining <= 0:
                        print("No seats available.")
                        InputHelper.pause()
                        continue

                    customers = self.customer.fetch()

                    if not customers:
                        print("No customers found.")
                        InputHelper.pause()
                        continue

                    print(f"\n{'OPT':<4} {'ID':<5} {'NAME':<25} {'EMAIL':<30}")
                    print("-" * 70)

                    for i, c in enumerate(customers, start=1):
                        name = f"{c[2]} {c[3]}"
                        print(f"{i:<4} {c[0]:<5} {name:<25} {c[8]:<30}")

                    cust_opt = InputHelper.prompt_int("Select customer option: ")

                    if cust_opt < 1 or cust_opt > len(customers):
                        print("Invalid option.")
                        InputHelper.pause()
                        continue

                    customer_id = customers[cust_opt - 1][0]

                    flight = self.flight.fetch_detailed(flight_id)

                    if not flight:
                        print("Flight not found.")
                        InputHelper.pause()
                        continue

                    duration = flight[11]
                    aircraft = flight[7]
                    dep_time = flight[2]
                    dep_date = flight[1]

                    price = calculate_dynamic_price(duration, aircraft, dep_time, dep_date)

                    print(f"\nTicket price: ${price:.2f}")

                    confirm = input("Confirm purchase? (y/n): ").lower()

                    if confirm != "y":
                        print("Purchase cancelled.")
                        InputHelper.pause()
                        continue

                    self.ticket.purchase_ticket(customer_id, flight_id, price)

                    print("Ticket successfully booked.")

                    InputHelper.pause()

                elif choice == "0":
                    return

                else:
                    print("Invalid selection.")

    # ------------------------------------------------------------
    # Ticket Cancellation
    # ------------------------------------------------------------
    # Allows users to cancel an existing flight ticket by entering
    # the ticket number.
    #
    # The system removes the ticket record and frees the seat
    # on the associated flight.
    # ------------------------------------------------------------

    def cancel_ticket_menu(self):
        print("\n--- CANCEL FLIGHT TICKET ---")
        ticket_number = InputHelper.prompt_int("Ticket number to cancel: ")
        self.ticket.cancel_ticket(ticket_number)
        InputHelper.pause()

    # -------------------------
    # Reports
    # -------------------------

    # ------------------------------------------------------------
    # Flight Sales Report
    # ------------------------------------------------------------
    # Generates a summary report showing ticket sales per flight.
    #
    # The report displays:
    #   • Flight number
    #   • Origin and destination airports
    #   • Flight date
    #   • Total tickets sold
    #   • Total revenue generated
    #
    # This report helps monitor flight performance and revenue.
    # ------------------------------------------------------------


    def flight_sales_report_menu(self):
        print("\n--- FLIGHT SALES REPORT ---")
        rows = self.report.flight_sales_report()
        print(f"{'FLIGHT':<7} {'FROM':<6} {'TO':<6} {'DATE':<12} {'TICKETS':<8} {'TOTAL SALES':<12}")
        print("-" * 60)

        for row in rows:
            print(f"{row[0]:<7} {row[1]:<6} {row[2]:<6} {row[3]:<12} {row[4]:<8} {row[5]:<12.2f}")
        InputHelper.pause()

    # ------------------------------------------------------------
    # Employee Flight Assignment Report
    # ------------------------------------------------------------
    # Displays the number of flights assigned to each employee.
    #
    # The report includes:
    #   • Employee ID
    #   • Employee name
    #   • Job title
    #   • Number of assigned flights
    #
    # This helps track crew workload distribution.
    # ------------------------------------------------------------

    def employee_flight_report_menu(self):
        print("\n--- EMPLOYEE FLIGHT REPORT ---")
        rows = self.report.employee_flight_report()
        print(f"{'EMP ID':<7} {'EMPLOYEE NAME':<25} {'JOB TITLE':<20} {'FLIGHTS':<8}")
        print("-" * 65)

        for row in rows:
            print(f"{row[0]:<7} {row[1]:<25} {row[2]:<20} {row[3]:<8}")
        InputHelper.pause()

    # ------------------------------------------------------------
    # Passenger Manifest Report
    # ------------------------------------------------------------
    # Displays a list of passengers booked on a selected flight.
    #
    # Information shown includes:
    #   • Ticket number
    #   • Customer ID
    #   • Passenger first and last name
    #   • Email contact
    #
    # This report is typically used by airline staff during
    # boarding and flight preparation.
    # ------------------------------------------------------------

    def passenger_manifest_menu(self):

        print("\n--- PASSENGER MANIFEST ---")
        from pricing_engine import calculate_dynamic_price
        origin = InputHelper.prompt_non_empty(
            "Search flights departing from (Flight ID / airport code / city): "
        )
        destination = input(
            "Optional destination filter (airport code / city) - press Enter to skip: "
        ).strip()
        rows = self.flight.search(origin, destination if destination else None)
        if not rows:
            print("No matching flights found.")
            InputHelper.pause()

            return
        print(
            f"{'OPT':<4} {'FLIGHT':<6} {'DATE':<12} {'TIME':<8} "
            f"{'FROM':<6} {'CITY':<15} {'TO':<6} {'CITY':<15} "
            f"{'AIRCRAFT':<20} {'SEATS':<6} {'DURATION':<8}"
        )
        print("-" * 110)

        for i, row in enumerate(rows, start=1):
            flight_id = row[0]
            dep_date = row[1]
            dep_time = row[2]
            origin_code = row[3]
            origin_city = row[4]
            dest_code = row[5]
            dest_city = row[6]
            aircraft = row[7]
            seats = row[8]
            duration = row[11]

            print(
                f"{i:<4} {flight_id:<6} {dep_date:<12} {dep_time:<8} "
                f"{origin_code:<6} {origin_city:<15} {dest_code:<6} {dest_city:<15} "
                f"{aircraft:<20} {seats:<6} {duration:<8}"
            )

        option = InputHelper.prompt_int("Select flight option: ")

        if option < 1 or option > len(rows):
            print("Invalid selection.")
            InputHelper.pause()
            return

        flight_id = rows[option - 1][0]

        print(f"\nPassenger Manifest for Flight {flight_id}\n")

        passengers = self.report.passenger_manifest(flight_id)

        if passengers:

            print(
                f"{'TICKET':<8} {'CUS ID':<7} {'FIRST NAME':<15} "
                f"{'LAST NAME':<15} {'EMAIL':<30}"
            )
            print("-" * 80)

            for row in passengers:
                print(
                    f"{row[0]:<8} {row[1]:<7} {row[2]:<15} {row[3]:<15} {row[4]:<30}"
                )

        else:
            print("No passengers found for this flight.")

        InputHelper.pause()

    # ------------------------------------------------------------
    # Flight Crew Assignment Report
    # ------------------------------------------------------------
    # Displays all employees assigned to a specific flight.
    #
    # The report lists:
    #   • Employee ID
    #   • Employee name
    #   • Job title
    #
    # Crew assignments are automatically generated when flights
    # are created based on aircraft capacity and staff roles.
    # ------------------------------------------------------------

    def flight_crew_report_menu(self):

        print("\n--- FLIGHT CREW REPORT ---")
        keyword = InputHelper.prompt_non_empty(
            "Search flights by ID, airport code, or city: "
        )
        rows = self.flight.search(keyword)
        if not rows:
            print("No flights found.")
            InputHelper.pause()
            return
        print(
            f"{'OPT':<4} {'FLIGHT':<6} {'DATE':<12} {'TIME':<8} "
            f"{'FROM':<6} {'CITY':<15} {'TO':<6} {'CITY':<15}"
        )
        print("-" * 80)

        for i, row in enumerate(rows, start=1):
            print(
                f"{i:<4} {row[0]:<6} {row[1]:<12} {row[2]:<8} "
                f"{row[3]:<6} {row[4]:<15} {row[5]:<6} {row[6]:<15}"
            )
        opt = InputHelper.prompt_int("Select flight option: ")

        if opt < 1 or opt > len(rows):
            print("Invalid selection.")
            InputHelper.pause()
            return
        flight_id = rows[opt - 1][0]
        crew = self.report.flight_crew(flight_id)
        print(f"\nCrew assigned to Flight {flight_id}\n")
        if not crew:
            print("No crew assigned.")
            InputHelper.pause()
            return

        print(f"{'EMP ID':<8} {'NAME':<25} {'JOB TITLE':<25}")
        print("-" * 60)
        for c in crew:
            print(f"{c[0]:<8} {c[1]:<25} {c[2]:<25}")

        InputHelper.pause()

    # -------------------------
    # Admin utility actions
    # -------------------------

    # ------------------------------------------------------------
    # Database Reset Utility
    # ------------------------------------------------------------
    # Administrative function used to completely reset the system
    # database.
    #
    # This operation:
    #   • Deletes all current records
    #   • Rebuilds the database schema
    #   • Reinitializes application connections
    #
    # This is mainly used for testing or restoring the system to
    # a clean initial state.
    # ------------------------------------------------------------


    def reset_database_menu(self):

        print("\n--- RESET DATABASE ---")

        confirm = input("This will delete all current records. Continue? (y/n): ").strip().lower()

        if confirm == "y":

            # Close all active connections first
            self.airport.get_connection.close()
            self.aircraft.get_connection.close()
            self.employee.get_connection.close()
            self.customer.get_connection.close()
            self.flight.get_connection.close()
            self.ticket.get_connection.close()
            self.report.get_connection.close()
            self.importer.get_connection.close()
            self.db.get_connection.close()

            # Now reset database
            ProjectDB().reset_database()

            # Recreate connections
            self.__init__()

        else:
            print("Reset cancelled.")

        InputHelper.pause()

    # ------------------------------------------------------------
    # CSV Data Import Utility
    # ------------------------------------------------------------
    # Allows administrators to quickly populate the database
    # using predefined CSV files.
    #
    # Data imported may include:
    #   • Airports
    #   • Aircraft
    #   • Employees
    #   • Customers
    #   • Flights
    #
    # This feature simplifies testing and system initialization.
    # ------------------------------------------------------------


    def import_csv_menu(self):
        print("\n--- IMPORT SAMPLE CSV DATA ---")
        print("This assumes the sample files are inside the data folder.")
        confirm = input("Import all default CSV files now? (y/n): ").strip().lower()
        if confirm == "y":
            self.importer.import_all_default_files()
        else:
            print("Import cancelled.")
        InputHelper.pause()


if __name__ == "__main__":
    app = AirAsiaProject()
    app.run()


# ------------------------------------------------------------
# Program Entry Point
# ------------------------------------------------------------
# Initializes the AirAsia Ticketing System and launches
# the main interactive command-line interface.
# ------------------------------------------------------------