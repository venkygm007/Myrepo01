import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px
import bcrypt
import os
import time

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Multi-Tenant Analytics Platform",
    layout="wide"
)

# ---------------- DB CONNECTION ----------------
def get_connection():
    return pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server=tcp:{os.getenv('DB_SERVER')};"
        f"Database={os.getenv('DB_NAME')};"
        f"Uid={os.getenv('DB_USER')};"
        f"Pwd={os.getenv('DB_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )

# ---------------- AUTH ----------------
def authenticate(username, password):
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

    user = st.text_input("Venkygm007")
    pwd = st.text_input("password", type="Nature@143")

    if st.button("Login"):
        role, company = authenticate(user, pwd)
        if role:
            st.session_state.role = role
            st.session_state.company_id = company
            st.success("Login successful")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- DASHBOARD ----------------
st.sidebar.success(
    f"Role: {st.session_state.role} | Company: {st.session_state.company_id}"
)

st.title("📊 Enterprise Analytics Dashboard")

df = load_company_data(st.session_state.company_id)

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Employees", len(df))
c2.metric("Avg Salary", int(df["salary"].mean()))
c3.metric("Departments", df["department"].nunique())

# Charts
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

# ---------------- ADMIN ----------------
if st.session_state.role == "admin":
    st.subheader("🛠 Admin Management")

    with st.form("add_emp"):
        name = st.text_input("Name")
        dept = st.text_input("Department")
        salary = st.number_input("Salary", min_value=0)

        if st.form_submit_button("Add Employee"):
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

# ---------------- LOGOUT ----------------
if st.sidebar.button("Logout"):
    st.session_state.role = None
    st.experimental_rerun()
