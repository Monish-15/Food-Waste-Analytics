import os
import pandas as pd
import streamlit as st
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Food Waste Analytics Dashboard", layout="wide")

# --- LOAD DATA ---
data_path = os.path.join("data", "summary.csv")

if not os.path.exists(data_path):
    st.error(f"❌ Could not find the file: {data_path}")
    st.stop()

# Read CSV
df = pd.read_csv(data_path)
df.columns = df.columns.str.lower().str.strip()

st.title("🌍 Food Waste Analytics Dashboard")

st.subheader("Dataset Overview")
st.write(df.head())

# --- AUTO-DETECT COLUMN NAMES ---
col_map = {
    "country": None,
    "year": None,
    "waste": None,
    "food type": None
}

for col in df.columns:
    if "country" in col:
        col_map["country"] = col
    elif "year" in col:
        col_map["year"] = col
    elif "waste" in col or "amount" in col or "kg" in col:
        col_map["waste"] = col
    elif "food" in col or "category" in col or "item" in col:
        col_map["food type"] = col

# --- CHECK MAPPING ---
missing = [k for k, v in col_map.items() if v is None]
if missing:
    st.error(f"⚠️ Could not detect columns for: {missing}")
    st.write("Columns found:", df.columns.tolist())
    st.stop()

# Rename for consistency
df = df.rename(columns={
    col_map["country"]: "country",
    col_map["year"]: "year",
    col_map["waste"]: "waste",
    col_map["food type"]: "food type"
})

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")

countries = sorted(df["country"].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", countries)

years = sorted(df["year"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", years)

filtered_df = df[(df["country"] == selected_country) & (df["year"] == selected_year)]

# --- VISUALIZATIONS ---
st.subheader(f"📊 Food Waste Breakdown — {selected_country} ({selected_year})")

if filtered_df.empty:
    st.info("No data available for selected filters.")
else:
    fig_pie = px.pie(
        filtered_df,
        values="waste",
        names="food type",
        title=f"Food Waste Composition in {selected_country} ({selected_year})",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    country_trend = df[df["country"] == selected_country]
    fig_line = px.line(
        country_trend,
        x="year",
        y="waste",
        color="food type",
        markers=True,
        title=f"Yearly Trend of Food Waste in {selected_country}"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- SUMMARY ---
st.subheader("📈 Summary Statistics")
st.write(filtered_df.describe())

st.success("✅ Dashboard loaded successfully!")
#cd "D:\BTECH-I\Food Waste Analytics streamlit run app.py"
