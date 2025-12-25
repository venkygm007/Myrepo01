import pandas as pd
import pyodbc

# ------------------- FILE CREATION -------------------
data = {
    "EmpID": [1, 2, 3],
    "Name": ["Ravi", "Sita", "Arjun"],
    "Department": ["IT", "HR", "Finance"],
    "Salary": [60000, 55000, 65000]
}

df = pd.DataFrame(data)
df.to_csv("employees.csv", index=False)
print("✅ employees.csv created")

# ------------------- AZURE SQL CONFIG -------------------
SERVER = "venkatproject.database.windows.net"
DATABASE = "Venkygm007"
USERNAME = "Venkygm007"
PASSWORD = "Nature@143"

# ------------------- CONNECT TO AZURE SQL -------------------
try:
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD}"
    )
    cursor = conn.cursor()
    print("✅ Connected to Azure SQL")

    # ------------------- CREATE/RESET TABLE -------------------
    # Dropping and Recreating to ensure schema matches [EmpID, Name, Department, Salary]
    print("🔄 Resetting table to match schema...")
    cursor.execute("IF EXISTS (SELECT * FROM sysobjects WHERE name='Employees' AND xtype='U') DROP TABLE Employees")
    
    cursor.execute("""
        CREATE TABLE [Employees] (
            [EmpID] INT PRIMARY KEY,
            [Name] VARCHAR(100),
            [Department] VARCHAR(50),
            [Salary] INT
        )
    """)
    conn.commit()
    print("✅ Table created with correct schema")

    # ------------------- DELETE EXISTING DATA (Optional, for clean run) -------------------
    # cursor.execute("DELETE FROM Employees")
    # conn.commit()

    # ------------------- INSERT DATA ------------------
    df = pd.read_csv("employees.csv")

    for _, row in df.iterrows():
        # Clean parameter passing to avoid preparing issues
        emp_id = int(row.EmpID)
        name = str(row.Name)
        dept = str(row.Department)
        salary = int(row.Salary)

        # Check if exists first
        cursor.execute("SELECT 1 FROM Employees WHERE EmpID = ?", emp_id)
        if cursor.fetchone():
            cursor.execute("""
                UPDATE Employees 
                SET Name = ?, Department = ?, Salary = ? 
                WHERE EmpID = ?
            """, name, dept, salary, emp_id)
        else:
            cursor.execute("""
                INSERT INTO Employees (EmpID, Name, Department, Salary) 
                VALUES (?, ?, ?, ?)
            """, emp_id, name, dept, salary)

    conn.commit()
    print("✅ Data pushed to Azure SQL")

    # ------------------- VERIFY DATA -------------------
    cursor.execute("SELECT * FROM Employees")
    rows = cursor.fetchall()

    print("📊 Data in Azure SQL:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()
    print("✅ Done")

except Exception as e:
    print(f"❌ Error: {e}")
