
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

def show_dashboard():
    st.header("📊 Prediction Dashboard")

    if "data" not in st.session_state:
        st.warning("Please upload a CSV file from the sidebar.")
        return

    df = st.session_state["data"]

    # Prediction Distribution
    pred_counts = df["prediction"].value_counts().reset_index()
    pred_counts.columns = ["Class", "Count"]
    fig_pred = px.bar(pred_counts, x="Class", y="Count", title="Prediction Distribution")
    st.plotly_chart(fig_pred)

    # Risk Overview
    risk_counts = df["risk_flag"].value_counts().reset_index()
    risk_counts.columns = ["Risk Level", "Count"]
    fig_risk = px.pie(risk_counts, names="Risk Level", values="Count", title="Risk Overview")
    st.plotly_chart(fig_risk)

    # Image Viewer
    st.subheader("🖼️ Image Viewer")
    selected_file = st.selectbox("Select an image filename", df["filename"].unique())
    selected_row = df[df["filename"] == selected_file].iloc[0]

    st.image(f"data/{selected_file}", caption=selected_file, use_column_width=True)
    st.markdown(f"**Prediction:** {selected_row['prediction']}")
    st.markdown(f"**Confidence:** {selected_row['confidence']}")
    st.markdown(f"**Risk Level:** {selected_row['risk_flag']}")
