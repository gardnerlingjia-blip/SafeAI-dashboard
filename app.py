
import streamlit as st
import pandas as pd
from pages.dashboard import show_dashboard
from pages.compliance import show_compliance
from utils.metrics import compute_metrics

st.set_page_config(page_title="SafeAI Audit Dashboard", layout="wide")

# Sidebar setup

with open("assets/logo.txt", "r") as file:
    st.sidebar.text(file.read())

st.sidebar.title("SafeAI Dashboard")
uploaded_file = st.sidebar.file_uploader("Upload Prediction CSV", type=["csv"])

# Load data into session state
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state["data"] = df

# Navigation
page = st.sidebar.radio("Navigate", ["Dashboard", "Compliance", "Report"])

# Page routing
if page == "Dashboard":
    show_dashboard()
elif page == "Compliance":
    show_compliance()
elif page == "Report":
    st.header("📄 Audit Report")
    if "data" not in st.session_state:
        st.warning("Please upload a CSV file from the sidebar.")
    else:
        df = st.session_state["data"]
        metrics = compute_metrics(df)
        if metrics:
            st.subheader("Model Performance Metrics")
            for k, v in metrics.items():
                if k == "Confusion Matrix":
                    st.write("Confusion Matrix:")
                    st.write(v)
                else:
                    st.metric(k, f"{v:.2f}")
        else:
            st.info("True labels not available. Metrics cannot be computed.")

        st.subheader("Export Report")
        st.download_button("Download CSV", df.to_csv(index=False), "audit_report.csv", "text/csv")
