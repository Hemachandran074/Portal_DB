import sqlite3

# Connect to the database
db_path = 'D:\Portal_DB\output.db'  # Update the path if needed
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the USERS table if it doesn't exist
"""
cursor.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        portal_id TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'student'
    );
''')
"""
# Insert data into USERS table from table1, setting password and role
"""
cursor.execute('''
    INSERT INTO USERS (portal_id, password, role)
    SELECT portal_id, 'password' AS password, 'student' AS role
    FROM table1;
''')
"""



#Creating Teacher, Staffs, Principal, Hods
users_data = [
    ('Gayatri', 'password', 'Staff'),
    ('Narmatha', 'password', 'Staff'),
    ('Hemalatha', 'password', 'HOD'),
    ('principal', 'password', 'Principal')
]

cursor.executemany('INSERT INTO users (portal_id, password, role) VALUES (?, ?, ?)', users_data)
# Commit the transaction and close the connection
conn.commit()
conn.close()

print("USERS table created and populated successfully.")
