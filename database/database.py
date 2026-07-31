"""
Database Module
Tyre Claim Management System (TCMS)

This module is responsible for:
1. Connecting to the SQLite database
2. Creating the database if it doesn't exist
3. Creating all required tables using schema.sql
"""

import sqlite3
from pathlib import Path


# Project Root Folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Database File Path
DATABASE_PATH = BASE_DIR / "database" / "claims.db"

# SQL Schema File
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


def get_connection():
    """
    Create and return a SQLite database connection.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    return connection


def initialize_database():
    """
    Create all database tables using schema.sql.
    """

    connection = get_connection()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        schema = schema_file.read()

    connection.executescript(schema)

    connection.commit()

    connection.close()

    print("✅ Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()
    