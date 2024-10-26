import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('portal.db')
c = conn.cursor()

# Create Users table (if it doesn't exist)
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)''')

# Create Marks table (if it doesn't exist)
c.execute('''CREATE TABLE IF NOT EXISTS marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    marks INTEGER,
    class TEXT,
    department TEXT
)''')

# Insert 5 users (students, staff, HOD, principal)
users_data = [
    ('student1', 'password1', 'Student'),
    ('student2', 'password2', 'Student'),
    ('staff1', 'password3', 'Staff'),
    ('hod1', 'password4', 'HOD'),
    ('principal', 'password5', 'Principal')
]

c.executemany('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', users_data)

# Insert 5 sample marks records for students
marks_data = [
    (1, 'CTPS', 85, 'second', 'AIML'),
    (1, 'L1', 90, 'second', 'AIML'),
    (2, 'L1', 78, 'second', 'DS'),
    (2, 'L2', 88, 'second', 'DS'),
    (1, 'L2', 92, 'second', 'AIML'),
]

c.executemany('INSERT INTO marks (student_id, subject, marks, class, department) VALUES (?, ?, ?, ?, ?)', marks_data)

# Commit changes and close the connection
conn.commit()
conn.close()




import pandas as pd
from pathlib import Path

def excel_to_database(excel_file, database_name, sheet_names=None):
    """
    Convert Excel file to SQLite database.
    
    Parameters:
    excel_file (str): Path to Excel file
    database_name (str): Name for the SQLite database
    sheet_names (list, optional): List of sheet names to convert. If None, converts all sheets.
    
    Returns:
    str: Path to created database
    """
    # Create database connection
    conn = sqlite3.connect(database_name)
    
    try:
        # Read all sheets if sheet_names is None
        if sheet_names is None:
            excel_data = pd.read_excel(excel_file, sheet_name=None)
        else:
            excel_data = {sheet: pd.read_excel(excel_file, sheet_name=sheet) 
                         for sheet in sheet_names}
        
        # Convert each sheet to a table
        for sheet_name, df in excel_data.items():
            # Clean column names (remove spaces, special characters)
            df.columns = [col.lower().replace(' ', '_').replace('-', '_') 
                         for col in df.columns]
            
            # Remove any invalid characters from sheet name
            table_name = ''.join(char for char in sheet_name 
                               if char.isalnum() or char == '_').lower()
            
            # Write to database
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            print(f"Converted sheet '{sheet_name}' to table '{table_name}'")
            print(f"Number of rows: {len(df)}")
            print(f"Columns: {', '.join(df.columns)}\n")
    
    finally:
        conn.close()
    
    return database_name

def main():
    """
    Example usage of the converter
    """
    # Example paths
    excel_file = "C:\chandru\Portal_DB\Students Performance Report - 2027 Batch - v1.xls"
    db_name = "output.db"
    
    try:
        # Convert Excel to database
        db_path = excel_to_database(excel_file, db_name)
        print(f"Successfully created database: {db_path}")
        
        # Optional: Verify the conversion
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\nDatabase contents:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]
            print(f"Table: {table_name}, Rows: {row_count}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()