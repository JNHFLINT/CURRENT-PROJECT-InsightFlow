from ai_recommendations import generate_recommendations
from sqlalchemy import create_engine

import pandas as pd
import streamlit as st
import plotly.express as px


# ---------------------------------------------------------
# Database Engine Helper
# ---------------------------------------------------------
def get_engine(db_type, host, user, password, database):
    if db_type == "PostgreSQL":
        return create_engine(f"postgresql://{user}:{password}@{host}/{database}")
    if db_type == "MySQL":
        return create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    if db_type == "SQLite":
        return create_engine(f"sqlite:///{database}")
    raise ValueError(f"Unsupported database type: {db_type}")


# ---------------------------------------------------------
# Excel Loader
# ---------------------------------------------------------
def load_excel(uploaded_file):
    try:
        sheets = pd.read_excel(uploaded_file, sheet_name=None)
        st.write("Sheets Found:", list(sheets.keys()))

        return (
            sheets.get("Jobs"),
            sheets.get("Employees"),
            sheets.get("Monthly_Summary"),
        )
    except Exception as e:
        st.error(f"Failed to load Excel file: {e}")
        return None, None, None


# ---------------------------------------------------------
# Database Loader
# ---------------------------------------------------------
def load_database(db_type, host, user, password, database):
    try:
        engine = get_engine(db_type, host, user, password, database)

        jobs_df = pd.read_sql("SELECT * FROM Jobs", engine)
        employees_df = pd.read_sql("SELECT * FROM Employees", engine)
        monthly_df = pd.read_sql("SELECT * FROM Monthly_Summary", engine)

        st.success("Connected and loaded tables successfully!")
        return jobs_df, employees_df, monthly_df

    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None, None, None


# ---------------------------------------------------------
# Visualization Section
# ---------------------------------------------------------
def show_visualizations(jobs_df, employees_df, monthly_df):
    st.subheader("Jobs")
    st.dataframe(jobs_df)
    st.plotly_chart(px.line(jobs_df, x="job_id", y="total_job_cost"))

    st.subheader("Employees")
    st.dataframe(employees_df)
    st.plotly_chart(px.bar(employees_df, x="employee_id", y="total_worker_cost"))

    st.subheader("Monthly Summary")
    st.dataframe(monthly_df)
    st.plotly_chart(px.line(monthly_df, x="month", y="revenue"))


# ---------------------------------------------------------
# AI Insights Section
# ---------------------------------------------------------
def show_ai_insights(jobs_df, employees_df, monthly_df):
    st.header("AI Insights")

    if st.button("Generate AI Recommendations"):
        insights = generate_recommendations(
            jobs_df,
            employees_df,
            monthly_df,
            st.secrets["GROQ_API_KEY"]
        )
        st.write(insights)


# ---------------------------------------------------------
# Main App Flow
# ---------------------------------------------------------
def main():
    st.title("Business Insights Dashboard")

    data_source = st.radio("Select Data Source", ["Excel File", "Database"])
    st.subheader("Load Data")

    jobs_df = employees_df = monthly_df = None

    # -----------------------------
    # Excel Loader
    # -----------------------------
    if data_source == "Excel File":
        uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

        if uploaded_file:
            jobs_df, employees_df, monthly_df = load_excel(uploaded_file)
            if jobs_df is not None:
                st.success("Excel data loaded successfully!")

    # -----------------------------
    # Database Loader
    # -----------------------------
    elif data_source == "Database":
        with st.form("db_form"):
            db_type = st.selectbox("Database Type", ["PostgreSQL", "MySQL", "SQLite"])
            host = st.text_input("Host (ignored for SQLite)", key="db_host")
            user = st.text_input("User (ignored for SQLite)", key="db_user")
            password = st.text_input("Password", type="password", key="db_password")
            database = st.text_input("Database Name or SQLite File Path", key="db_name")

            submitted = st.form_submit_button("Connect to Database")

        if submitted:
            jobs_df, employees_df, monthly_df = load_database(
                db_type, host, user, password, database
            )

    # -----------------------------
    # If data loaded → show visuals + AI
    # -----------------------------
    if jobs_df is not None:
        show_visualizations(jobs_df, employees_df, monthly_df)
        show_ai_insights(jobs_df, employees_df, monthly_df)


# ---------------------------------------------------------
# Run App
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
