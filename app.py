import streamlit as st
import os
import pandas as pd

from scraper_api import scrape_remotive, save_to_csv
from analyzer import analyze_jobs

st.set_page_config(layout="wide")
st.title("📊 Real-Time Job Trend Analyzer")
st.markdown("Fetch and analyze remote job trends from Remotive.")

st.sidebar.header("Controls")
keyword = st.sidebar.text_input("Enter job keyword (e.g., Python Developer):", "Python Developer")
fetch_button = st.sidebar.button("Fetch Latest Jobs", key="fetch")

csv_filename = "real-time-job-trend-analyzer/jobs.csv"

if fetch_button:
    with st.spinner(f"Scraping jobs for keyword: 	{keyword}	 ..."):
        jobs = scrape_remotive(keyword)
        if jobs:
            save_to_csv(jobs, filename=csv_filename)
            st.success(f"Job data scraped and saved to {csv_filename}!")
            if "analysis_data" in st.session_state:
                del st.session_state.analysis_data
        else:
            st.warning("No jobs found or scraping failed.")

st.header("Job Market Analysis")

if os.path.exists(csv_filename):
    if "analysis_data" not in st.session_state:
        with st.spinner("Analyzing job data..."):
            st.session_state.analysis_data = analyze_jobs(filename=csv_filename)

    analysis_data = st.session_state.analysis_data

    if analysis_data:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top Job Titles")
            if not analysis_data["Top Job Titles"].empty:
                st.bar_chart(analysis_data["Top Job Titles"], use_container_width=True)
            else:
                st.info("No title data to display.")

            st.subheader("Job Postings per Day")
            if not analysis_data["Job Postings per Day"].empty:
                daily_data_df = analysis_data["Job Postings per Day"].reset_index()
                daily_data_df.columns = ["Date", "Count"]
                st.line_chart(daily_data_df.set_index("Date"), use_container_width=True)
            else:
                st.info("No posting date data to display.")

        with col2:
            st.subheader("Top Locations")
            if not analysis_data["Top Locations"].empty:
                st.bar_chart(analysis_data["Top Locations"], use_container_width=True)
            else:
                st.info("No location data to display.")

        with st.expander("View Raw Data Sample"):
            try:
                df_raw = pd.read_csv(csv_filename)
                st.dataframe(df_raw.head(10))
            except Exception as e:
                st.error(f"Could not read or display raw data: {e}")

    else:
        st.warning("Analysis could not be performed. Check logs or try fetching data again.")
else:
    st.info(f"No job data file ({csv_filename}) found. Click 	Fetch Latest Jobs	 in the sidebar first.")

