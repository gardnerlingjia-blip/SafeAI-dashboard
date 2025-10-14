
import streamlit as st
import pandas as pd
from pages.dashboard import show_dashboard
from pages.compliance import show_compliance
from utils.metrics import compute_metrics
from streamlit_option_menu import option_menu
import base64

import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score



# Custom CSS
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
            padding: 20px;
        }
        .css-1d391kg {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("assets/logo.jpg", width=150)
    st.markdown("## SafeAI Dashboard")
    uploaded_file = st.file_uploader("Upload Prediction CSV", type=["csv"])
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Compliance", "Report"],
        icons=["bar-chart", "shield-check", "file-earmark-text"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )

st.title(f"{selected} Section")


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


if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'actual' in df.columns and 'predicted' in df.columns:
        # Accuracy
        accuracy = accuracy_score(df['actual'], df['predicted'])
        st.metric("Model Accuracy", f"{accuracy:.2%}")

        # Compliance check
        safety_threshold = 0.9
        if accuracy < safety_threshold:
            st.error(f"⚠️ Accuracy below {safety_threshold:.0%}")
        else:
            st.success("✅ Accuracy meets safety threshold")

        # Class distribution
        st.subheader("Class Distribution")
        fig_bar = px.bar(df['predicted'].value_counts(), title="Predicted Class Distribution")
        st.plotly_chart(fig_bar)

        # Confusion matrix
        st.subheader("Confusion Matrix")
        labels = sorted(df['actual'].unique())
        cm = confusion_matrix(df['actual'], df['predicted'], labels=labels)
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
        st.pyplot(fig)
    else:
        st.error("CSV must contain 'actual' and 'predicted' columns.")

