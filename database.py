import os
from app import app, db

# This script will find the DB, wipe it, and rebuild it.

print(f"1. Flask thinks the database is located at: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

with app.app_context():
    # Force delete all tables (Wipes the data clean)
    db.drop_all()
    print("2. Old tables deleted successfully.")
    
    # Create new tables with the 'role' column
    db.create_all()
    print("3. New tables created successfully!")