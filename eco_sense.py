import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from PIL import Image
import time

# ✅ Ensure set_page_config is at the top
st.set_page_config(page_title="EcoSense - Waste Reduction Platform", page_icon="🌱", layout="wide")

# Simulated user database
users = {"admin": "password123", "user1": "eco123"}

# Apply custom styles
st.markdown(
    """
    <style>
        body {
            background-color: #f0f7f4;
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            padding: 2rem;
        }
        .title {
            text-align: center;
            color: #1b5e20;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background: linear-gradient(45deg, #43a047 30%, #4caf50 90%);
            color: white;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(45deg, #388e3c 30%, #43a047 90%);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-1px);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Session State for login
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def authenticate(username, password):
    return users.get(username) == password

def main():
    if not st.session_state["authenticated"]:
        login()
        return
    
    st.sidebar.title("🌿 EcoSense Menu")
    page = st.sidebar.radio("", ["🏠 Home", "📝 Log Waste", "📊 Insights", "🚀 Action Plan", "🏆 Leaderboard", "💬 Forum", "ℹ️ Project Info"])
    
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
    if st.button("Login", help="Click to login"):
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")

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
    
    material_type = st.selectbox("Select Material Type", ["Food", "Plastic", "Paper", "Glass", "Metal", "Electronics", "Other"])
    quantity = st.number_input("Amount (kg)", min_value=0.1, max_value=50.0, value=0.5, step=0.1)
    entry_date = st.date_input("Entry Date", datetime.now())
    handling = st.selectbox("Handling Method", ["Recycled", "Composted", "Landfill", "Donated", "Repurposed"])
    
    if st.button("💾 Save Entry"):
        st.success(f"✅ Logged {quantity} kg of {material_type}")
    
    st.subheader("🤖 AI Waste Recognition")
    file_upload = st.file_uploader("📸 Upload an image", type=["jpg", "png", "jpeg"])
    if file_upload is not None:
        st.image(file_upload, caption="Uploaded image", width=250)
        time.sleep(2)
        st.success("🤖 AI Recognized: Plastic Bottle")
        st.info("💡 Recommendation: Recycle it in a plastic bin")

def waste_insights():
    st.header("📊 Waste Insights")
    
    span = st.selectbox("Select Time Period", ["7 Days", "30 Days", "90 Days", "1 Year"])
    days = int(span.split()[0])
    
    dates = pd.date_range(end=datetime.now(), periods=days)
    waste_data = pd.DataFrame({
        "Date": dates,
        "Organic": np.random.normal(1.8, 0.6, days),
        "Plastic": np.random.normal(0.9, 0.4, days),
        "Paper": np.random.normal(0.7, 0.3, days)
    })
    waste_data.set_index("Date", inplace=True)
    
    st.line_chart(waste_data)
    st.download_button("⬇ Download Data", waste_data.to_csv(), "waste_data.csv", "text/csv")

def action_plan():
    st.header("🚀 Personalized Action Plan")
    st.write("🌿 Reduce plastic waste by 35% in 90 days!")
    st.progress(0.58)
    st.write("💡 Try using reusable alternatives like cloth bags and metal straws.")

def leaderboard():
    st.header("🏆 Leaderboard - Top Waste Reducers")
    data = {"User": ["Aayush", "Saksham", "Arthav", "Aaryan"], "Waste Reduced (kg)": [85, 74, 66, 58]}
    st.table(pd.DataFrame(data))

def community_forum():
    st.header("💬 Community Forum - Share Your Tips")
    comment = st.text_area("📝 Share a sustainability tip:")
    if st.button("📢 Post"):
        st.success("✅ Your tip has been posted!")
    
    st.subheader("📌 Recent Tips")
    st.write("- Alice: Use bamboo toothbrushes instead of plastic ones!")
    st.write("- Bob: Carry a reusable bottle everywhere!")
    st.write("- Charlie: Try composting at home!")

def project_info():
    st.header("ℹ️ About EcoSense")
    st.write("EcoSense is a waste reduction platform for a greener planet.")
    st.markdown("**GitHub Repository:** [github.com/Aayush5154/EcoSense](https://github.com/Aayush5154/EcoSense)")

if __name__ == "__main__":
    main()
