import pyodbc
import bcrypt
import os
from dotenv import load_dotenv

# Load environment variables if .env exists
load_dotenv()

# ---------------- DB CONNECTION ----------------
def get_connection():
    try:
        conn = pyodbc.connect(
            "Driver={SQL Server};"
            f"Server=tcp:{os.getenv('DB_SERVER')};"
            f"Database={os.getenv('DB_NAME')};"
            f"Uid={os.getenv('DB_USER')};"
            f"Pwd={os.getenv('DB_PASSWORD')};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# ---------------- USER MANAGEMENT ----------------

def create_user_table():
    conn = get_connection()
    if not conn: return
    
    cur = conn.cursor()
    # Create users table if it doesn't exist
    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
    CREATE TABLE users (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL,
        company_id INT NOT NULL
    )
    """
    cur.execute(create_table_query)
    conn.commit()
    print("Users table checked/created.")
    conn.close()

def add_user(username, password, role, company_id):
    conn = get_connection()
    if not conn: return
    
    cur = conn.cursor()
    hashed_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    try:
        cur.execute(
            "INSERT INTO users (username, password, role, company_id) VALUES (?, ?, ?, ?)",
            (username, hashed_pwd, role, company_id)
        )
        conn.commit()
        print(f"User '{username}' added successfully.")
    except Exception as e:
        print(f"Error adding user: {e}")
    finally:
        conn.close()

def list_users():
    conn = get_connection()
    if not conn: return
    
    cur = conn.cursor()
    cur.execute("SELECT username, role, company_id FROM users")
    rows = cur.fetchall()
    
    print("\n--- Current Users ---")
    for row in rows:
        print(f"User: {row[0]}, Role: {row[1]}, Company ID: {row[2]}")
    print("----------------------\n")
    conn.close()

def delete_user(username):
    conn = get_connection()
    if not conn: return
    
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    print(f"User '{username}' deleted.")
    conn.close()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("User Management Script")
    print("1. Create/Check Users Table")
    print("2. Add New User")
    print("3. List All Users")
    print("4. Delete User")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter choice (1-5): ")
        
        if choice == '1':
            create_user_table()
        elif choice == '2':
            u = input("Username: ")
            p = input("Password: ")
            r = input("Role (admin/user): ")
            c = input("Company ID: ")
            add_user(u, p, r, int(c))
        elif choice == '3':
            list_users()
        elif choice == '4':
            u = input("Username to delete: ")
            delete_user(u)
        elif choice == '5':
            break
        else:
            print("Invalid choice.")
