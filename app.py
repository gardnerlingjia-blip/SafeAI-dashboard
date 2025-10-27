
import threading
import uvicorn
import streamlit.web.cli as stcli
from fastapi import FastAPI
import pandas as pd
import numpy as np
import os
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
import streamlit as st

# Import external modules
from pages.dashboard import show_dashboard
from pages.compliance import show_compliance
from utils.metrics import compute_metrics

# ---------------------------
# FastAPI App for Health Checks
# ---------------------------
app = FastAPI()

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

# ---------------------------
# Streamlit Dashboard Logic
# ---------------------------
def run_streamlit():
    st.set_page_config(layout="wide", page_title="SafeAI Prediction Audit Dashboard")
    st.sidebar.image("assets/logo.png", width=150)
    st.sidebar.title("SafeAI Dashboard")

    # Sidebar Navigation
    page = st.sidebar.radio("Navigate", ["Dashboard", "Compliance", "Report"])
    uploaded_file = st.sidebar.file_uploader("Upload Prediction CSV", type=["csv"])
    image_folder = st.sidebar.text_input("Path to image folder")
    threshold = st.sidebar.slider("Safety Accuracy Threshold", 0.0, 1.0, 0.5)

    # Load Data
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state["data"] = df
        st.session_state["threshold"] = threshold
        st.session_state["image_folder"] = image_folder

    # Page routing using external modules
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

# ---------------------------
# Run FastAPI + Streamlit Together
# ---------------------------
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    threading.Thread(target=lambda: stcli.main(["run", "app.py"])).start()
    run_fastapi()
