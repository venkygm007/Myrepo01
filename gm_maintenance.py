import pyodbc
import pandas as pd

# ------------------- AZURE SQL CONFIG -------------------
SERVER = "venkatproject.database.windows.net"
DATABASE = "Venkygm007"
USERNAME = "Venkygm007"
PASSWORD = "Nature@143"

def setup_gm_products():
    try:
        print("Connecting to Azure SQL for GM Products Maintenance...")
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD}"
        )
        cursor = conn.cursor()

        # 1. Create GM_Products Table
        print("Ensuring GM_Products table exists...")
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='GM_Products' AND xtype='U')
        CREATE TABLE GM_Products (
            ProductID INT IDENTITY(1,1) PRIMARY KEY,
            Category VARCHAR(100),
            ProductName VARCHAR(200),
            Price DECIMAL(10, 2),
            StockQuantity INT,
            LastUpdated DATETIME DEFAULT GETDATE()
        )
        """)
        conn.commit()

        # 2. Add Initial Data (Dryfruits, Plastics, and Chicken Pickle)
        products = [
            ('Dryfruits', 'Premium Almonds (500g)', 450.00, 50),
            ('Dryfruits', 'Cashew Nuts Jumbo (500g)', 550.00, 40),
            ('Plastics', 'Storage Container Set (3pc)', 120.00, 100),
            ('Plastics', 'Plastic Water Bottle (1L)', 45.00, 200),
            ('Pickle', 'Spicy Chicken Pickle (250g)', 180.00, 30),
            ('Pickle', 'Boneless Chicken Pickle (500g)', 350.00, 25),
            ('Pickle', 'Andhra Style Chicken Pickle (250g)', 190.00, 45)
        ]

        print("Updating product inventory...")
        for category, name, price, stock in products:
            # Check if product exists to update instead of insert
            cursor.execute("SELECT 1 FROM GM_Products WHERE ProductName = ?", name)
            if cursor.fetchone():
                cursor.execute("""
                    UPDATE GM_Products 
                    SET Category = ?, Price = ?, StockQuantity = ?, LastUpdated = GETDATE()
                    WHERE ProductName = ?
                """, category, price, stock, name)
            else:
                cursor.execute("""
                    INSERT INTO GM_Products (Category, ProductName, Price, StockQuantity) 
                    VALUES (?, ?, ?, ?)
                """, category, name, price, stock)

        conn.commit()
        print("✅ GM Products database updated successfully!")

        # 3. Verify and Display Data
        cursor.execute("SELECT * FROM GM_Products")
        rows = cursor.fetchall()
        print("\n📊 Current Inventory (GM Dryfruits & Plastics + Pickles):")
        print(f"{'ID':<4} | {'Category':<15} | {'Product Name':<30} | {'Price':<8} | {'Stock':<6}")
        print("-" * 75)
        for row in rows:
            print(f"{row.ProductID:<4} | {row.Category:<15} | {row.ProductName:<30} | {row.Price:<8.2f} | {row.StockQuantity:<6}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_gm_products()
