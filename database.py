import sqlite3
import os


# ==========================================
# DATABASE LOCATION
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_DIR = os.path.join(BASE_DIR, "database")

os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "travel.db")

# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# CREATE TABLE
# ==========================================

def create_table():

    connection = get_connection()


    connection.execute("""
        CREATE TABLE IF NOT EXISTS trips (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            start_location TEXT NOT NULL,

            destination TEXT NOT NULL,

            start_date TEXT,

            end_date TEXT,

            currency TEXT DEFAULT '₹',

            budget REAL,

            travelers INTEGER,

            interests TEXT
        )
    """)


    connection.commit()


    # Add currency column if old database does not have it
    columns = connection.execute(
        "PRAGMA table_info(trips)"
    ).fetchall()


    column_names = [
        column["name"]
        for column in columns
    ]


    if "currency" not in column_names:

        connection.execute("""
            ALTER TABLE trips
            ADD COLUMN currency TEXT DEFAULT '₹'
        """)

        connection.commit()


    connection.close()


# ==========================================
# SAVE TRIP
# ==========================================

def save_trip(
    start_location,
    destination,
    start_date,
    end_date,
    currency,
    budget,
    travelers,
    interests
):

    connection = get_connection()


    cursor = connection.execute("""
        INSERT INTO trips
        (
            start_location,
            destination,
            start_date,
            end_date,
            currency,
            budget,
            travelers,
            interests
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        start_location,
        destination,
        start_date,
        end_date,
        currency,
        budget,
        travelers,
        interests

    ))


    connection.commit()


    trip_id = cursor.lastrowid


    connection.close()


    return trip_id


# ==========================================
# GET ALL TRIPS
# ==========================================

def get_trips():

    connection = get_connection()


    trips = connection.execute("""
        SELECT *
        FROM trips
        ORDER BY id DESC
    """).fetchall()


    connection.close()


    return [
        dict(trip)
        for trip in trips
    ]


# ==========================================
# DELETE TRIP
# ==========================================

def delete_trip(trip_id):

    connection = get_connection()


    cursor = connection.execute(
        """
        DELETE FROM trips
        WHERE id = ?
        """,
        (trip_id,)
    )


    connection.commit()


    deleted = cursor.rowcount


    connection.close()


    return deleted
