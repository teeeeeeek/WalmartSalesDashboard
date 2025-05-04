import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Set Streamlit page config
st.set_page_config(page_title="Walmart Dashboard", layout="wide")

# Load data
@st.cache_data

def load_data():
    return pd.read_csv("WalmartPerformanceDataset.csv")

df = load_data()

# Sidebar filters
st.sidebar.title("🔍 Filter Options")
st.sidebar.markdown("Customize your view:")
regions = st.sidebar.multiselect("🌎 Select Region(s):", options=df["Region"].unique(), default=df["Region"].unique())
stores = st.sidebar.multiselect("🏬 Select Store(s):", options=df["Store_ID"].unique(), default=df["Store_ID"].unique())
departments = st.sidebar.multiselect("🛒 Select Department(s):", options=df["Department"].unique(), default=df["Department"].unique())
dates = pd.to_datetime(df["Date"].unique())
date_range = st.sidebar.date_input("📆 Select Date Range:", [dates.min(), dates.max()])

# Filter data
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Store_ID"].isin(stores)) &
    (df["Department"].isin(departments)) &
    (pd.to_datetime(df["Date"]) >= pd.to_datetime(date_range[0])) &
    (pd.to_datetime(df["Date"]) <= pd.to_datetime(date_range[1]))
]

# Dashboard header
st.title("📊 Walmart Business Performance Dashboard")
st.markdown("""
This interactive dashboard provides real-time insights into Walmart's regional sales, customer traffic, and departmental trends. Use the filters on the left to explore key metrics and performance indicators.
""")

# KPI Cards
st.subheader("📌 Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("💰 Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
kpi2.metric("📈 Avg. Profit Margin", f"{filtered_df['Profit_Margin'].mean():.2%}")
kpi3.metric("👣 Total Foot Traffic", f"{filtered_df['Foot_Traffic'].sum():,}")

# Line chart - Sales trend over time
st.markdown("### 📅 Weekly Sales Trend")
sales_trend = filtered_df.groupby("Date")["Sales"].sum().reset_index()
st.plotly_chart(px.line(sales_trend, x="Date", y="Sales", title="Sales Trend Over Time", markers=True))

# Bar chart - Profit by region
st.markdown("### 🌍 Sales by Region")
region_profit = filtered_df.groupby("Region")["Sales"].sum().reset_index()
st.plotly_chart(px.bar(region_profit, x="Region", y="Sales", title="Total Sales by Region", text_auto=True, color="Region"))

# Scatter plot - Inventory vs Sales
st.markdown("### 🏷️ Inventory vs. Sales by Department")
st.plotly_chart(px.scatter(filtered_df, x="Inventory_Units", y="Sales", color="Department", title="Inventory Efficiency by Department", size="Sales", hover_name="Store_ID"))

# Additional enhancement - Departmental breakdown pie chart
st.markdown("### 🍕 Sales Contribution by Department")
dept_share = filtered_df.groupby("Department")["Sales"].sum().reset_index()
st.plotly_chart(px.pie(dept_share, names="Department", values="Sales", title="Department-wise Sales Distribution"))

# Download filtered data as CSV
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_walmart_data.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.caption("Developed for ALY6040 Assignment 4 | Sreekarteek Akshinthala | Powered by Streamlit")
