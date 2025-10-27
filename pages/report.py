
import streamlit as st
import pandas as pd

def show():
    st.title("📄 Documentation Generator")

    # Try to load prediction data from session state or fallback to sample CSV
    df = None
    if "prediction_data" in st.session_state:
        df = st.session_state["prediction_data"]
    else:
        try:
            df = pd.read_csv("data/sample_predictions.csv")
        except FileNotFoundError:
            st.warning("No prediction data found. Please upload a CSV file or generate predictions first.")
            return

    # Display the data preview
    st.subheader("🔍 Prediction Audit Summary")
    st.dataframe(df)

    # Button to download the report as CSV
    st.download_button(
        label="📥 Download Audit Report as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="audit_report.csv",
        mime="text/csv"
    )
