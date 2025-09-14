import streamlit as st
import pandas as pd
import os
import base64
from io import BytesIO
from PIL import Image

from utils.data_processing import preprocess_data, perform_eda
from utils.visualization import generate_all_visualizations
from utils.ai_summary import generate_ai_summary, calculate_kpis

# Streamlit page config
st.set_page_config(page_title="Excel Insight Generator", layout="wide")

st.title("📊 Excel Insight Generator")
st.markdown("Upload your Excel/CSV files and get instant AI-powered insights.")

# File uploader
uploaded_file = st.file_uploader("📂 Upload your file", type=["xlsx", "xls", "csv"])

if uploaded_file:
    try:
        # Load file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Preprocess + EDA
        df = preprocess_data(df)
        eda_results = perform_eda(df)
        kpis = calculate_kpis(df)

        # KPIs Section
        st.subheader("📌 Key Performance Indicators")
        kpi_cols = st.columns(3)  # 3 KPIs per row

        for i, (key, value) in enumerate(kpis.items()):
            with kpi_cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="background-color:#f9f9f9; padding:15px; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.1); margin-bottom:10px;">
                        <h4 style="color:black; font-weight:bold; margin:0;">{key}</h4>
                        <p style="font-size:20px; margin:0; color:#2E86C1;"><b>{value}</b></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Data Preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head(20))

        # Visualizations
        st.subheader("📈 Visualizations")
        visuals = generate_all_visualizations(df)
        def show_base64_image(img_str):
            image_data = base64.b64decode(img_str)
            image = Image.open(BytesIO(image_data))
            st.image(image)

        for section, plots in visuals.items():
            st.markdown(f"### {section.replace('_', ' ').title()}")

            if isinstance(plots, dict):  # multiple plots
                for col, img_str in plots.items():
                    st.markdown(f"**{col}**")
                    show_base64_image(img_str)
            elif plots:  # single plot
                show_base64_image(plots)

        # AI Insights
        st.subheader("🤖 AI-Powered Insights")
        ai_summary = generate_ai_summary(eda_results, kpis)
        st.markdown(
            f"""
            <div style="background-color:#eef6fb; padding:20px; border-radius:12px; border-left:6px solid #1f77b4; line-height:1.6;">
                {ai_summary}
            </div>
            """,
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")
