import pyodbc

# ------------------- AZURE SQL CONFIG -------------------
SERVER = "venkatproject.database.windows.net"
DATABASE = "Venkygm007"
USERNAME = "Venkygm007"
PASSWORD = "Nature@143"

# ------------------- PUSH IMAGE TO AZURE SQL -------------------
def push_image_to_sql(file_path, image_name):
    try:
        print(f"Connecting to Azure SQL to push {image_name}...")
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD}"
        )
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Product_Images' AND xtype='U')
        CREATE TABLE Product_Images (
            ID INT IDENTITY(1,1) PRIMARY KEY,
            ImageName VARCHAR(255),
            ImageData VARBINARY(MAX)
        )
        """)
        conn.commit()

        # Read image as binary
        with open(file_path, "rb") as file:
            binary_data = file.read()

        # Insert into database
        cursor.execute("INSERT INTO Product_Images (ImageName, ImageData) VALUES (?, ?)", (image_name, pyodbc.Binary(binary_data)))
        conn.commit()
        
        print(f"✅ Image '{image_name}' successfully pushed to Azure SQL!")
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    push_image_to_sql("Sunflowerseeds.jpg", "Sunflowerseeds")
