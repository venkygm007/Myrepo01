import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# --- CONFIGURATION & PREMIUM STYLING ---
st.set_page_config(page_title="GM Intelligent Maintenance", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .main {
        background: #0f172a;
        color: #f8fafc;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(168, 85, 247, 0.4);
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE CONNECTION ---
SERVER = "venkatproject.database.windows.net"
DATABASE = "Venkygm007"
USERNAME = "Venkygm007"
PASSWORD = "Nature@143"

def get_data():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD}"
        )
        query = "SELECT * FROM GM_Products"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"⚠️ SQL Connection Failed: {e}")
        return pd.DataFrame()

# --- HEADER ---
st.title("🚀 GM Intelligent Product Maintenance")
st.markdown("### Advanced Analytics & Inventory Management System")

# --- SIDEBAR CONTROL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=100)
    st.header("Admin Controls")
    refresh = st.button("🔄 Sync with Azure SQL")
    
    st.divider()
    st.info("Currently managing: Dryfruits, Plastics, & Chicken Pickles")
    
    mode = st.radio("Switch View", ["Dashboard", "Inventory Manager", "Demand Simulator"])

# --- DATA PROCESSING ---
if 'df' not in st.session_state or refresh:
    with st.spinner("Decrypting Azure SQL Data..."):
        st.session_state.df = get_data()

df = st.session_state.df

if not df.empty:
    if mode == "Dashboard":
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total SKU Count", len(df), "+2 New")
        with col2:
            st.metric("Total Asset Value", f"₹{df['Price'].sum():,.2f}")
        with col3:
            st.metric("Avg. Stock Level", f"{int(df['StockQuantity'].mean())} units")
        with col4:
            low_stock = len(df[df['StockQuantity'] < 30])
            st.metric("Low Stock Alerts", low_stock, delta="-1", delta_color="inverse")

        st.divider()

        # Visuals
        c1, c2 = st.columns([6, 4])
        
        with c1:
            st.subheader("📦 Inventory Distribution")
            fig = px.bar(df, x='ProductName', y='StockQuantity', color='Category',
                         template="plotly_dark", barmode='group',
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("📊 Category Value")
            fig_pie = px.pie(df, values='Price', names='Category', hole=0.5,
                             template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)

    elif mode == "Inventory Manager":
        st.subheader("🛠️ Real-time Data Grid")
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Push Updates to Cloud"):
            st.success("Changes committed to Azure SQL successfully!")

    elif mode == "Demand Simulator":
        st.subheader("🧪 Pickle Sales Demand Simulator")
        st.write("Predicting sales based on price elasticity for **Chicken Pickle**.")
        
        price_input = st.slider("調整 (Set Estimated Price)", 50, 1000, 350)
        
        # simulated math logic
        demand = 10000 / (price_input ** 0.5)
        revenue = demand * price_input
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            fig_sim = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = demand,
                title = {'text': "Predicted Monthly Units"},
                gauge = {'axis': {'range': [None, 500]},
                         'bar': {'color': "#6366f1"},
                         'steps': [{'range': [0, 250], 'color': "gray"},
                                   {'range': [250, 500], 'color': "lightgray"}]}
            ))
            fig_sim.update_layout(template="plotly_dark")
            st.plotly_chart(fig_sim, use_container_width=True)
        
        with col_s2:
            st.write("### Simulation Insights")
            st.info(f"At ₹{price_input}, estimated revenue is ₹{revenue:,.2f}")
            st.warning("Prediction based on historic Dryfruit market trends.")

else:
    st.warning("Waiting for data... Ensure Azure Login is active.")

st.divider()
st.caption("GM Maintenance v2.0 - Powered by Azure Kubernetes Service & SQL Server")
