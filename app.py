
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score

# Page configuration
st.set_page_config(page_title="SafeAI Prediction Audit Dashboard", layout="wide")

# Sidebar layout
with st.sidebar:
    st.image("assets/logo.png", width=150)  # Make sure logo.png is in assets/
    st.markdown("## SafeAI Dashboard")
    uploaded_file = st.file_uploader("Upload Prediction CSV", type=["csv"])
    use_sample = st.checkbox("Use sample data from GitHub")
    selected = st.selectbox("Navigate", ["Dashboard", "Compliance", "Report"])
    safety_threshold = st.slider("Safety Accuracy Threshold", min_value=0.0, max_value=1.0, value=0.9)

# Main content
st.title(f"{selected} Section")

df = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
elif use_sample:
    # Replace the URL below with your actual GitHub raw CSV link
    url = "https://github.com/gardnerlingjia-blip/SafeAI-dashboard//data/sample_predictions.csv"
    try:
        df = pd.read_csv(url)
        st.info("Loaded sample data from GitHub.")
    except Exception as e:
        st.error(f"Could not load sample data from GitHub: {e}")

if df is not None:
    # Validate columns
    if 'actual' in df.columns and 'predicted' in df.columns:
        # ✅ Compliance Summary
        accuracy = accuracy_score(df['actual'], df['predicted'])
        st.subheader("Compliance Summary")
        st.metric(label="Model Accuracy", value=f"{accuracy:.2%}")
        if accuracy < safety_threshold:
            st.error(f"⚠️ Accuracy below safety threshold of {safety_threshold:.0%}")
        else:
            st.success("✅ Accuracy meets safety threshold")

        # ✅ Class Distribution Chart
        st.subheader("Class Distribution")
        class_counts = df['predicted'].value_counts().reset_index()
        class_counts.columns = ['Class', 'Count']
        fig_bar = px.bar(class_counts, x='Class', y='Count', title='Predicted Class Distribution')
        st.plotly_chart(fig_bar, use_container_width=True)

        # ✅ Confusion Matrix Heatmap
        st.subheader("Confusion Matrix")
        labels = sorted(df['actual'].unique())
        cm = confusion_matrix(df['actual'], df['predicted'], labels=labels)
        fig_cm, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels, ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("Confusion Matrix")
        st.pyplot(fig_cm)

    else:
        st.error("CSV must contain 'actual' and 'predicted' columns.")
else:
    st.info("Please upload a CSV file from the sidebar or select 'Use sample data from GitHub'.")
