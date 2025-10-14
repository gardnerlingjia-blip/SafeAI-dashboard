

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import os
from fpdf import FPDF

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(layout="wide", page_title="SafeAI Prediction Audit Dashboard")

st.title("SafeAI Prediction Audit Dashboard")
st.markdown("Simulate safety audits for image classification models in automotive systems.")

# ---------------------------
# SIDEBAR NAVIGATION
# ---------------------------
menu = st.sidebar.radio("Navigate", ["Compliance", "Dashboard", "Report"])

uploaded_file = st.file_uploader("Upload Prediction CSV", type=["csv"])
image_folder = st.text_input("Path to image folder")
threshold = st.slider("Safety Accuracy Threshold", 0.0, 1.0, 0.9)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["Pass"] = df["confidence"] >= threshold
    df["Audit Result"] = np.where(df["Pass"], "Pass", "Fail")

# ---------------------------
# COMPLIANCE TAB
# ---------------------------
if menu == "Compliance":
    st.header("Compliance Section")
    st.write("ISO 26262 / SOTIF compliance checks, risk heatmap, export compliance docs.")

    if uploaded_file:
        # ISO compliance check summary
        st.subheader("Compliance Metrics")
        fail_rate = (df["Audit Result"] == "Fail").mean()
        st.metric("Fail Rate", f"{fail_rate:.2%}")
        st.metric("Threshold", f"{threshold:.2f}")

        # Risk Heatmap
        st.subheader("Risk Heatmap")
        fig, ax = plt.subplots()
        pivot = df.pivot_table(values="confidence", index="prediction", columns="Audit Result", aggfunc="mean")
        sns.heatmap(pivot, cmap="coolwarm", annot=True, ax=ax)
        st.pyplot(fig)

        # Export compliance documentation
        if st.button("Export Compliance Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="SafeAI Compliance Report", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Fail Rate: {fail_rate:.2%}", ln=True)
            pdf.cell(200, 10, txt=f"Threshold: {threshold:.2f}", ln=True)
            pdf.output("compliance_report.pdf")
            st.success("Compliance report exported as compliance_report.pdf")

# ---------------------------
# DASHBOARD TAB
# ---------------------------
elif menu == "Dashboard":
    st.header("Audit Dashboard")
    if uploaded_file:
        st.subheader("Audit Summary")
        st.dataframe(df[["image_id", "prediction", "confidence", "Audit Result"]])

        # KPIs
        st.metric("Fail Rate", f"{fail_rate:.2%}")
        st.metric("Total Images", len(df))

        # Image Viewer
        if image_folder and os.path.exists(image_folder):
            selected_image = st.selectbox("Select image", df["image_id"])
            image_path = os.path.join(image_folder, selected_image)
            st.image(Image.open(image_path), caption=selected_image)

# ---------------------------
# REPORT TAB
# ---------------------------
elif menu == "Report":
    st.header("Generate Audit Report")
    if uploaded_file:
        if st.button("Export Audit Report (CSV)"):
            df.to_csv("audit_report.csv", index=False)
            st.success("Audit report exported as audit_report.csv")

        if st.button("Export Audit Report (PDF)"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="SafeAI Audit Report", ln=True, align="C")
            for _, row in df.iterrows():
                pdf.cell(200, 10, txt=f"{row['image_id']} - {row['prediction']} - {row['confidence']:.2f} - {row['Audit Result']}", ln=True)
            pdf.output("audit_report.pdf")
            st.success("Audit report exported as audit_report.pdf")



