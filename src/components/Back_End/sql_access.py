import sqlite3

def get_student_data(portal_id, role):
    conn = sqlite3.connect("output.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enable column names in the result
    cursor = conn.cursor()

    try:
        if role == "student":
            cursor.execute("SELECT * FROM table1 WHERE portal_id = ?", (portal_id,))
            result = cursor.fetchone()  # Single row for students
            
            # Save only the specific student data to result.db
            if result:
                save_to_result_db([dict(result)], role)  # Pass the role for context
            
            return result  # Return as a Row object for student access
        else:  # For principals or other roles
            cursor.execute("SELECT * FROM table1")
            result = cursor.fetchall()  # All rows for principals
            
            # Save all student data to result.db
            if result:
                save_to_result_db([dict(row) for row in result], role)  # Pass the role for context
            
            return result  # Return as a list of Row objects for principals
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Improved error handling
        return None
    finally:
        conn.close()

def save_to_result_db(data, role):
    """Saves the given data to result.db."""
    try:
        with sqlite3.connect("result.db") as conn:
            cursor = conn.cursor()
            
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS table1 (
                    s_no INTEGER PRIMARY KEY,
                    portal_id TEXT,
                    register_number TEXT,
                    name TEXT,
                    department TEXT,
                    ctps REAL,
                    l1___score REAL,
                    l2___score REAL,
                    l3___score REAL,
                    l4___score REAL,
                    l5___score REAL,
                    pds REAL,
                    total_score REAL,
                    user_role TEXT  -- Added a column for user role
                )
            """)

            # Clear previous data for the specific role
            cursor.execute("DELETE FROM table1 WHERE user_role = ?", (role,))
            
            # Insert new data
            for entry in data:
                entry['user_role'] = role  # Add user role to each entry
            cursor.executemany("INSERT INTO table1 (s_no, portal_id, register_number, name, department, ctps, l1___score, l2___score, l3___score, l4___score, l5___score, pds, total_score, user_role) VALUES (:s_no, :portal_id, :register_number, :name, :department, :ctps, :l1___score, :l2___score, :l3___score, :l4___score, :l5___score, :pds, :total_score, :user_role)", data)
            
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving to result.db: {e}")
