import pandas as pd
import pyodbc

# ------------------- AZURE SQL CONFIG -------------------
SERVER = "venkatproject.database.windows.net"
DATABASE = "Venkygm007"
USERNAME = "Venkygm007"
PASSWORD = "Nature@143"

# ------------------- CONNECT AND PULL DATA -------------------
try:
    print("Connecting to Azure SQL...")
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD}"
    )
    
    query = "SELECT * FROM Employees"
    
    # Load data into a DataFrame
    print("Pulling data from 'Employees' table...")
    df = pd.read_sql(query, conn)
    
    # Save to CSV in the local folder
    output_file = "pulled_data.csv"
    df.to_csv(output_file, index=False)
    
    print(f"✅ Data successfully pulled and saved to {output_file}")
    print("📊 Preview of pulled data:")
    print(df)
    
    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")
