#!/usr/bin/env python3
"""
Script to initialize the database
"""
from models.database import engine, Base, init_db
from models.models import Investigation, CollectedData, Alert

if __name__ == "__main__":
    print("🗄️  Initializing database...")
    print(f"📍 Database URL: {engine.url}")

    try:
        # Créer toutes les tables
        init_db()
        print("✅ All database tables created successfully!")
        print("\nTables created:")
        print("  - investigations")
        print("  - collected_data")
        print("  - alerts")

    except Exception as e:
        print(f"❌ Error creating database: {e}")
        exit(1)
