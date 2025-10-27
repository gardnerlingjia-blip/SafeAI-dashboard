

import streamlit as st
import pandas as pd

def show_compliance():
    st.header("✅ Compliance Simulation")

    if "data" not in st.session_state:
        st.warning("Please upload a CSV file from the sidebar.")
        return

    df = st.session_state["data"]

    st.sidebar.subheader("🔧 Compliance Settings")
    min_confidence = st.sidebar.slider("Minimum Confidence Threshold", 0.0, 1.0, 0.7)
    allowed_risks = st.sidebar.multiselect("Allowed Risk Levels", ["low", "medium", "high"], default=["low", "medium"])

    def check_compliance(row):
        return row["confidence"] >= min_confidence and row["risk_flag"] in allowed_risks

    df["compliant"] = df.apply(check_compliance, axis=1)
    pass_rate = df["compliant"].mean() * 100

    st.metric("Compliance Pass Rate", f"{pass_rate:.2f}%")
    st.dataframe(df[["filename", "prediction", "confidence", "risk_flag", "compliant"]])
