import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px
import bcrypt
import os
import time
import struct
from azure.identity import DefaultAzureCredential

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Multi-Tenant Analytics Platform (Azure AD Auth)",
    layout="wide"
)

# ---------------- DB CONNECTION (Azure AD Auth) ----------------
def get_connection():
    # 1. Configuration from Environment
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    
    # 2. Connection String for Azure SQL (using ODBC Driver 18)
    conn_str = f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server},1433;Database={database};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    
    # 3. Use Password Auth if credentials exist, otherwise use Azure AD Token
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    
    if db_user and db_password:
        return pyodbc.connect(conn_str + f"Uid={db_user};Pwd={db_password};")
    else:
        # NO PASSWORD NEEDED: Use Azure AD Token (Managed Identity / az login)
        credential = DefaultAzureCredential()
        
        # Get token for Azure SQL (resource ID for SQL is fixed)
        token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("utf-16-le")
        
        # Format the token for pyodbc (SQL_COPT_SS_ACCESS_TOKEN = 1256)
        token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        
        return pyodbc.connect(conn_str, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})

# ---------------- AUTH (App Layer) ----------------
def authenticate(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT password, role, company_id FROM users WHERE username=?",
            username
        )
        row = cur.fetchone()
        conn.close()

        if row and bcrypt.checkpw(password.encode(), row[0].encode()):
            return row[1], row[2]
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
    return None, None

# ---------------- DATA ----------------
@st.cache_data(ttl=300)
def load_company_data(company_id):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM employees WHERE company_id=?",
        conn,
        params=[company_id]
    )
    conn.close()
    return df

# ---------------- SESSION ----------------
if "role" not in st.session_state:
    st.session_state.role = None
    st.session_state.company_id = None

# ---------------- LOGIN ----------------
if not st.session_state.role:
    st.title("🔐 Secure Enterprise Login")
    st.info("Now using Azure AD Passwordless Authentication for Database connection.")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        role, company = authenticate(user, pwd)
        if role:
            st.session_state.role = role
            st.session_state.company_id = company
            st.success("Login successful")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- DASHBOARD ----------------
st.sidebar.success(
    f"Role: {st.session_state.role} | Company: {st.session_state.company_id}"
)

st.title("📊 Enterprise Analytics Dashboard")

try:
    df = load_company_data(st.session_state.company_id)

    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Employees", len(df))
    c2.metric("Avg Salary", int(df["salary"].mean()) if not df.empty else 0)
    c3.metric("Departments", df["department"].nunique() if not df.empty else 0)

    # Charts
    if not df.empty:
        fig = px.bar(
            df.groupby("department")["salary"].mean().reset_index(),
            x="department",
            y="salary",
            title="Average Salary by Department"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Data
        st.subheader("Employee Records")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data found for your company.")

except Exception as e:
    st.error(f"Error loading data: {e}")

# ---------------- ADMIN ----------------
if st.session_state.role == "admin":
    st.subheader("🛠 Admin Management")

    with st.form("add_emp"):
        name = st.text_input("Name")
        dept = st.text_input("Department")
        salary = st.number_input("Salary", min_value=0)

        if st.form_submit_button("Add Employee"):
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO employees VALUES (?, ?, ?, ?)",
                    name,
                    dept,
                    salary,
                    st.session_state.company_id
                )
                conn.commit()
                conn.close()
                st.cache_data.clear()
                st.success("Employee added")
            except Exception as e:
                st.error(f"Failed to add employee: {e}")

# ---------------- LOGOUT ----------------
if st.sidebar.button("Logout"):
    st.session_state.role = None
    st.rerun()
