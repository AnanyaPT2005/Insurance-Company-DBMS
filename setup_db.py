import sqlite3

conn = sqlite3.connect('insurance_management.db')
c = conn.cursor()

# Login table (for customer & insurance provider)
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('customer', 'insurance_provider')) NOT NULL,
    patient_id TEXT,  -- for customers
    FOREIGN KEY(patient_id) REFERENCES patient(PatientID)
)
''')

conn.commit()
conn.close()

print("Login table added successfully!")
