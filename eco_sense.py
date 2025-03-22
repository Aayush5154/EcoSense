import streamlit as st
import pandas as pd
import sqlite3
import time
from datetime import datetime

# Set Streamlit Page Config
st.set_page_config(page_title="EcoSense - Waste Reduction Platform", page_icon="🌱", layout="wide")

# Custom CSS for Background and Styling
# Custom CSS for Background and Styling
# Custom CSS for Background and Styling
# Custom CSS for Styling
st.markdown(
    """
    <style>
    /* Set Background Color */
    [data-testid="stAppViewContainer"] {
        background-color: #E8F5E9; /* Light Green */
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #2E7D32 !important;  /* Dark Green */
        color: white !important;
    }

    /* Sidebar Text Styling */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Buttons Styling */
    div.stButton > button {
        border-radius: 10px;
        background-color: #4CAF50; /* Green */
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #388E3C;
    }

    /* Headers */
    .st-emotion-cache-10trblm {
        color: #1B5E20; /* Dark Green */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Database Setup
conn = sqlite3.connect("ecosense.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS waste_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    material TEXT,
    quantity REAL,
    date TEXT,
    method TEXT
)
""")
conn.commit()

# Session State for Login
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""

# Authentication Function
def authenticate(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cursor.fetchone() is not None

def register(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def main():
    if not st.session_state["authenticated"]:
        login()
        return
    
    st.sidebar.title("🌿 EcoSense Menu")
    page = st.sidebar.radio("", ["🏠 Home", "📝 Log Waste", "📊 Insights", "🚀 Action Plan", "🏆 Leaderboard", "💬 Forum", "ℹ Project Info"])
    
    if page == "🏠 Home":
        home_screen()
    elif page == "📝 Log Waste":
        log_waste()
    elif page == "📊 Insights":
        waste_insights()
    elif page == "🚀 Action Plan":
        action_plan()
    elif page == "🏆 Leaderboard":
        leaderboard()
    elif page == "💬 Forum":
        community_forum()
    else:
        project_info()

def login():
    st.title("🔐 Login to EcoSense")
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")
    
    st.subheader("New User? Register Below")
    new_user = st.text_input("Choose Username")
    new_pass = st.text_input("Choose Password", type="password")
    if st.button("Register"):
        if register(new_user, new_pass):
            st.success("✅ Registration Successful! You can now log in.")
        else:
            st.error("⚠ Username already exists!")

def home_screen():
    st.header("🌍 Welcome to EcoSense!")
    st.subheader("Your personalized waste tracking dashboard")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="♻ Waste Reduction", value="28%", delta="5%")
    with col2:
        st.metric(label="🔄 Recovered Materials", value="167 kg", delta="23 kg")
    with col3:
        st.metric(label="🌱 CO₂ Equivalent Saved", value="103 kg", delta="-12 kg")

def log_waste():
    st.header("📝 Log Your Waste")
    material = st.selectbox("Material Type", ["Food", "Plastic", "Paper", "Glass", "Metal", "Electronics", "Other"])
    quantity = st.number_input("Amount (kg)", min_value=0.1, max_value=50.0, value=0.5, step=0.1)
    entry_date = st.date_input("Entry Date", datetime.now())
    handling = st.selectbox("Handling Method", ["Recycled", "Composted", "Landfill", "Donated", "Repurposed"])
    
    if st.button("💾 Save Entry"):
        cursor.execute("INSERT INTO waste_log (username, material, quantity, date, method) VALUES (?, ?, ?, ?, ?)",
                       (st.session_state["username"], material, quantity, entry_date.strftime('%Y-%m-%d'), handling))
        conn.commit()
        st.success(f"✅ Logged {quantity} kg of {material}")

def waste_insights():
    st.header("📊 Waste Insights")
    df = pd.read_sql_query("SELECT * FROM waste_log", conn)
    st.dataframe(df)
    st.download_button("⬇ Download Data", df.to_csv(), "waste_data.csv", "text/csv")

def action_plan():
    st.header("🚀 Personalized Action Plan")
    st.write("🌿 Reduce plastic waste by 35% in 90 days!")
    st.progress(0.58)

def leaderboard():
    st.header("🏆 Leaderboard - Top Waste Reducers")
    df = pd.read_sql_query("SELECT username, SUM(quantity) as total FROM waste_log GROUP BY username ORDER BY total DESC", conn)
    st.table(df)

def community_forum():
    st.header("💬 Community Forum - Share Your Tips")
    comment = st.text_area("📝 Share a sustainability tip:")
    if st.button("📢 Post"):
        st.success("✅ Your tip has been posted!")

def project_info():
    st.header("ℹ About EcoSense")
    st.write("EcoSense is a waste reduction platform for a greener planet.")
    st.markdown("*GitHub Repository:* [github.com/Aayush5154/EcoSense](https://github.com/Aayush5154/EcoSense)")

if __name__ == "__main__":
    main()
