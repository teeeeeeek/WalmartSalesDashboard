import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("C:/Users/KarteekPC/Documents/ALY6040Module4/WalmartPerformanceDataset.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
regions = st.sidebar.multiselect("Select Region(s):", options=df["Region"].unique(), default=df["Region"].unique())
stores = st.sidebar.multiselect("Select Store(s):", options=df["Store_ID"].unique(), default=df["Store_ID"].unique())
departments = st.sidebar.multiselect("Select Department(s):", options=df["Department"].unique(), default=df["Department"].unique())
dates = pd.to_datetime(df["Date"].unique())
date_range = st.sidebar.date_input("Select Date Range:", [dates.min(), dates.max()])

# Filter data
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Store_ID"].isin(stores)) &
    (df["Department"].isin(departments)) &
    (pd.to_datetime(df["Date"]) >= pd.to_datetime(date_range[0])) &
    (pd.to_datetime(df["Date"]) <= pd.to_datetime(date_range[1]))
]

# Main dashboard
st.title("Walmart Business Performance Dashboard")
st.markdown("This dashboard provides insights into sales, inventory, and profit trends across Walmart stores.")

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Average Profit Margin", f"{filtered_df['Profit_Margin'].mean():.2%}")
col3.metric("Total Foot Traffic", f"{filtered_df['Foot_Traffic'].sum():,}")

# Line chart - Sales trend over time
sales_trend = filtered_df.groupby("Date")["Sales"].sum().reset_index()
st.plotly_chart(px.line(sales_trend, x="Date", y="Sales", title="Sales Trend Over Time"))

# Bar chart - Profit by region
region_profit = filtered_df.groupby("Region")["Sales"].sum().reset_index()
st.plotly_chart(px.bar(region_profit, x="Region", y="Sales", title="Sales by Region", text_auto=True))

# Scatter plot - Inventory vs Sales
st.plotly_chart(px.scatter(filtered_df, x="Inventory_Units", y="Sales", color="Department", title="Inventory vs Sales"))

# Download filtered data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    return output.getvalue()

st.download_button(
    label="Download Filtered Data as Excel",
    data=to_excel(filtered_df),
    file_name="filtered_walmart_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Footer
st.markdown("---")
st.caption("Developed for ALY6040 Assignment 4 | Powered by Streamlit")
