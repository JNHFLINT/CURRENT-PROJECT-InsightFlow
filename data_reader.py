from ai_recommendations import generate_recommendations

import pandas as pd 
import openpyxl
import streamlit as st
import plotly.express as px

# Upload Excel File via streamlit
uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

# Read the uploaded Excel file
if uploaded_file:

    sheets = pd.read_excel(
        uploaded_file,
        sheet_name=None
    )

    # Display the list of sheets found in the Excel file
    st.write("Sheets Found:")
    st.write(list(sheets.keys()))

    # Load the data from each sheet
    jobs_df = sheets["Jobs"]
    employees_df = sheets["Employees"]
    monthly_df = sheets["Monthly_Summary"]

    # Create visualizations for data "jobs"
    fig_jobs = px.line(jobs_df, x="Job_ID", y="Total_Job_Cost")
    st.subheader("Jobs")
    st.dataframe(jobs_df)
    st.plotly_chart(fig_jobs)

    # Create visualizations for data "employees"
    fig_employees = px.bar(employees_df, x="Employee_ID", y="Total_Worker_Cost")
    st.subheader("Employees")
    st.dataframe(employees_df)
    st.plotly_chart(fig_employees)

    # Create visualizations for data "monthly"
    fig_monthly = px.line(monthly_df, x="Month", y="Revenue")
    st.subheader("Monthly Summary")
    st.dataframe(monthly_df)
    st.plotly_chart(fig_monthly)

    st.header("AI Insights")

if st.button("Generate AI Recommendations"):
    insights = generate_recommendations(
        jobs_df,
        employees_df,
        monthly_df,
        st.secrets["GROQ_API_KEY"]
    )
    st.write(insights)
