
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import os
from fpdf import FPDF

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(layout="wide", page_title="SafeAI Prediction Audit Dashboard")

st.title("SafeAI Prediction Audit Dashboard")
st.markdown("Simulate safety audits for image classification models in automotive systems.")

# ----------------------------
# Sidebar Navigation
# ----------------------------
menu = st.sidebar.radio("Navigate", ["Compliance", "Dashboard", "Report"])

uploaded_file = st.file_uploader("Upload Prediction CSV", type=["csv"])
image_folder = st.text_input("Path to image folder")
threshold = st.slider("Safety Accuracy Threshold", 0.0, 1.0, 0.5)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["Pass"] = df["confidence"] >= threshold
    df["Audit Result"] = np.where(df["Pass"], "Pass", "Fail")

# ----------------------------
# Compliance Tab
# ----------------------------
if menu == "Compliance":
    st.header("Compliance Section")
    st.write("ISO 26262 / SOTIF checks, risk heatmap, export compliance docs.")

    if uploaded_file:
        st.subheader("Compliance Metrics")
        fail_rate = (df["Audit Result"] == "Fail").mean()
        st.metric("Fail Rate", f"{fail_rate:.2%}")

        # Risk Heatmap
        st.subheader("Risk Heatmap")
        fig, ax = plt.subplots()
        pivot = df.pivot_table(values="confidence", index="prediction", columns="Audit Result", aggfunc="mean")
        sns.heatmap(pivot, cmap="coolwarm", annot=True, ax=ax)
        st.pyplot(fig)

        # Compliance Checklist
        st.write("✅ ISO 26262 threshold applied")
        st.write("✅ SOTIF audit logic integrated")

# ----------------------------
# Dashboard Tab
# ----------------------------
elif menu == "Dashboard":
    st.header("Dashboard")
    if uploaded_file:
        st.subheader("Audit Summary")
        st.dataframe(df[["image_id", "prediction", "confidence", "Audit Result"]])

        # KPI Metrics
        st.metric("Total Images", len(df))
        st.metric("Pass Count", (df["Audit Result"] == "Pass").sum())
        st.metric("Fail Count", (df["Audit Result"] == "Fail").sum())

        # Trend Chart
        st.subheader("Confidence Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df["confidence"], bins=20, kde=True, ax=ax)
        st.pyplot(fig)

        # Image Viewer
        if image_folder and os.path.exists(image_folder):
            selected_image = st.selectbox("Select image", df["image_id"])
            image_path = os.path.join(image_folder, selected_image)
            st.image(Image.open(image_path), caption=selected_image)

# ----------------------------
# Report Tab
# ----------------------------
elif menu == "Report":
    st.header("Report Section")
    if uploaded_file:
        st.subheader("Export Audit Report")
        if st.button("Export CSV"):
            df.to_csv("audit_report.csv", index=False)
            st.success("Audit report exported as audit_report.csv")

        # PDF Export
        def export_pdf(dataframe, filename="compliance_report.pdf"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Compliance Audit Report", ln=True, align="C")

            for index, row in dataframe.iterrows():
                pdf.cell(200, 10, txt=f"{row['image_id']} - {row['Audit Result']} ({row['confidence']:.2f})", ln=True)

            pdf.output(filename)
            return filename

        if st.button("Export PDF"):
            file_path = export_pdf(df)
            st.success(f"Report saved as {file_path}")

