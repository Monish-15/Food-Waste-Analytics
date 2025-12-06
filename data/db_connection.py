# db_connection.py
from pymongo import MongoClient
import streamlit as st

@st.cache_resource
def get_db_connection():
    try:
        # ✅ Replace this with your MongoDB URI
        client = MongoClient("mongodb://localhost:27017/")
        db = client["budget_tracker_db"]
        st.success("🟢 Connected to MongoDB successfully!")
        return db
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None
