#!/usr/bin/env python3
import os
import psycopg2
from psycopg2 import sql

# Lire le fichier SQL
with open('/backend/seed_exercises.sql', 'r') as f:
    seed_sql = f.read()

# Connexion à la DB
conn = psycopg2.connect(
    host=os.getenv('DB_HOST', 'db'),
    database=os.getenv('POSTGRES_DB', 'gym_app'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
    port=5432
)

cursor = conn.cursor()

try:
    # Vérifier si les données existent déjà
    cursor.execute("SELECT COUNT(*) FROM exercises;")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Seeding database...")
        cursor.execute(seed_sql)
        conn.commit()
        print(f"✅ Database seeded with {cursor.rowcount} exercises")
    else:
        print(f"✅ Database already has {count} exercises")
        
except Exception as e:
    print(f"❌ Error seeding database: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
