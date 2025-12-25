from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# ------------------- AZURE SQL CONFIG -------------------
SERVER = "venkatproject.database.windows.net"
DATABASE = "Venkygm007"
USERNAME = "Venkygm007"
PASSWORD = "Nature@143"

def get_db_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD}"
    )

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GM_Products ORDER BY Category, ProductName")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', products=products)
    except Exception as e:
        return f"Error: {e}. Please ensure the GM_Products table exists by running gm_maintenance.py first."

@app.route('/add', methods=['POST'])
def add_product():
    category = request.form['category']
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO GM_Products (Category, ProductName, Price, StockQuantity)
        VALUES (?, ?, ?, ?)
    """, category, name, price, stock)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
