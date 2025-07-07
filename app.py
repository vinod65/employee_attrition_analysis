import streamlit as st
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide")

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# 🔹 Title
st.title("💼 Employee Attrition Dashboard")

# 🔹 Load data from SQLite
conn = sqlite3.connect("hr.db")
df = pd.read_sql_query("SELECT * FROM employee_data", conn)
conn.close()

# 🔹 Success message
st.success("✅ Data loaded successfully!")

# 🔹 Show data table
st.subheader("Employee Data Table")
st.dataframe(df)

# 🔹 KPIs
st.subheader("Attrition Summary")
total = len(df)
left = df[df["Attrition"] == "Yes"].shape[0]
avg_income = df[df["Attrition"] == "Yes"]["MonthlyIncome"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Employees", total)
col2.metric("Employees Left", left)
col3.metric("Avg Income (Left)", f"₹{avg_income:.0f}")

# 🔹 Gender-wise Attrition Pie Chart
st.subheader("📌 Gender-wise Attrition")
gender_counts = df[df["Attrition"] == "Yes"]["Gender"].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# 🔹 Department-wise Attrition Bar Chart
st.subheader("📌 Department-wise Attrition")
dept_counts = df[df["Attrition"] == "Yes"]["Department"].value_counts()
fig2, ax2 = plt.subplots()
ax2.bar(dept_counts.index, dept_counts.values, color='skyblue')
ax2.set_xlabel("Department")
ax2.set_ylabel("No. of Employees Left")
st.pyplot(fig2)

# 🔹 Sidebar Filter by Department
st.sidebar.header("🔍 Filter Data")
selected_dept = st.sidebar.selectbox("Select Department", df["Department"].unique())
filtered_df = df[df["Department"] == selected_dept]

# 🔹 Filtered Data Table
st.subheader(f"📄 Data for {selected_dept} Department")
st.dataframe(filtered_df)

# 🔹 Download Filtered Data Button
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name=f'{selected_dept}_data.csv',
    mime='text/csv',
)
