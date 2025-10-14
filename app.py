
import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(layout="wide", page_title="SafeAI Prediction Audit Dashboard")

st.title("SafeAI Prediction Audit Dashboard")
st.markdown("Simulate safety audits for image classification models in automotive systems.")

# ---------------------------
# Sidebar Navigation
# ---------------------------
menu = st.sidebar.radio("Navigate", ["Compliance", "Dashboard", "Report"])

uploaded_file = st.file_uploader("Upload Prediction CSV", type=["csv"])
image_folder = st.text_input("Path to image folder")
threshold = st.slider("Safety Accuracy Threshold", 0.0, 1.0, 0.5)

# ---------------------------
# Load Data and Prepare Columns
# ---------------------------
df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully.")
    # Check required columns
    if "confidence" not in df.columns or "predicted" not in df.columns:
        st.error("CSV must contain 'predicted' and 'confidence' columns.")
    else:
        # Add Audit Result column
        df["Audit Result"] = np.where(df["confidence"] >= threshold, "Pass", "Fail")

# ---------------------------
# Compliance Tab
# ---------------------------
if menu == "Compliance":
    st.header("Compliance Section")
    st.write("ISO 26262 / SOTIF checks, risk heatmap, and compliance export.")

    if df is not None and all(col in df.columns for col in ["confidence", "prediction", "Audit Result"]):
        # Risk Heatmap
        st.subheader("Risk Heatmap")
        pivot = df.pivot_table(values="confidence", index="prediction", columns="Audit Result", aggfunc="mean")
        fig, ax = plt.subplots()
        sns.heatmap(pivot, cmap="coolwarm", annot=True, ax=ax)
        st.pyplot(fig)

        # Compliance Summary
        st.subheader("Compliance Summary")
        fail_rate = (df["Audit Result"] == "Fail").mean()
        st.metric("Fail Rate", f"{fail_rate:.2%}")

        # Placeholder for ISO checks
        st.info("Future Feature: Add ISO 26262 / SOTIF compliance checklist logic here.")
    else:
        st.warning("Upload a valid CSV to view compliance metrics.")

# ---------------------------
# Dashboard Tab
# ---------------------------
elif menu == "Dashboard":
    st.header("Dashboard")
    if df is not None:
        st.subheader("Audit Summary")
        st.dataframe(df[["image_id", "prediction", "confidence", "Audit Result"]])

        # KPIs
        fail_rate = (df["Audit Result"] == "Fail").mean()
        st.metric("Fail Rate", f"{fail_rate:.2%}")

        # Image Viewer
        if image_folder and os.path.exists(image_folder):
            selected_image = st.selectbox("Select image", df["image_id"])
            image_path = os.path.join(image_folder, selected_image)
            st.image(Image.open(image_path), caption=selected_image)
    else:
        st.warning("Upload a CSV to view dashboard.")

# ---------------------------
# Report Tab
# ---------------------------
elif menu == "Report":
    st.header("Report Generation")
    if df is not None:
        # Export CSV
        if st.button("Export Audit Report (CSV)"):
            df.to_csv("audit_report.csv", index=False)
            st.success("Audit report exported as audit_report.csv")

        # Export PDF
        def export_pdf(dataframe, filename="compliance_report.pdf"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Compliance Audit Report", ln=True, align="C")
            for index, row in dataframe.iterrows():
                pdf.cell(200, 10, txt=f"{row['image_id']} - {row['Audit Result']} ({row['confidence']:.2f})", ln=True)
            pdf.output(filename)
            return filename

        if st.button("Export Compliance Report (PDF)"):
            file_path = export_pdf(df)
            st.success(f"Report saved as {file_path}")
    else:
        st.warning("Upload a CSV to generate reports.")

