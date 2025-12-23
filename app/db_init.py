#!/usr/bin/env python3
"""
Database initialization script for ColorNote application.
This script creates the database tables and sets up the initial schema.
"""

import os
import sys
from app import create_app
from app.models import db

def init_database():
    """Initialize the database with required tables."""
    try:
        # Create Flask app
        app = create_app()

        with app.app_context():
            print("Creating database tables...")

            # Create all tables
            db.create_all()

            print("Database tables created successfully!")
            print("Available tables:")
            for table in db.metadata.tables.keys():
                print(f"  - {table}")

            return True

    except Exception as e:
        print(f"Error initializing database: {e}", file=sys.stderr)
        return False

def reset_database():
    """Drop all tables and recreate them."""
    try:
        app = create_app()

        with app.app_context():
            print("Dropping existing tables...")
            db.drop_all()

            print("Recreating database tables...")
            db.create_all()

            print("Database reset completed successfully!")
            return True

    except Exception as e:
        print(f"Error resetting database: {e}", file=sys.stderr)
        return False

def check_connection():
    """Check database connection."""
    try:
        app = create_app()

        with app.app_context():
            # Try to execute a simple query
            db.engine.execute(db.text("SELECT 1"))
            print("Database connection successful!")
            return True

    except Exception as e:
        print(f"Database connection failed: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python db_init.py <command>")
        print("Commands:")
        print("  init     - Initialize database tables")
        print("  reset    - Drop and recreate all tables")
        print("  check    - Check database connection")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "init":
        success = init_database()
    elif command == "reset":
        success = reset_database()
    elif command == "check":
        success = check_connection()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

    sys.exit(0 if success else 1)
