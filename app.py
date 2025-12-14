"""
Excel-to-Insights Bot - Main Streamlit Application
Automated data analysis, visualization, and AI-powered insights generation
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
from pathlib import Path

# Import custom modules
from modules.data_processor import DataProcessor
from modules.eda_engine import EDAEngine
from modules.visualization_engine import VisualizationEngine
from modules.ai_insights import AIInsightsGenerator
from modules.report_generator import ReportGenerator

# Page configuration
st.set_page_config(
    page_title="Excel-to-Insights Bot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #f0f8ff;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Excel-to-Insights Bot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your Excel data into actionable insights in minutes</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Excel+Insights", use_container_width=True)
        st.markdown("### 🚀 Quick Start")
        st.markdown("""
        1. Upload your Excel file
        2. Review data preview
        3. Click 'Analyze Data'
        4. Explore insights
        """)
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        # AI Model selection
        ai_model = st.selectbox(
            "AI Model",
            ["OpenAI GPT-4", "Google Gemini", "OpenAI GPT-3.5"],
            help="Select the AI model for insights generation"
        )
        
        # Analysis depth
        analysis_depth = st.select_slider(
            "Analysis Depth",
            options=["Quick", "Standard", "Deep"],
            value="Standard",
            help="Choose analysis comprehensiveness"
        )
        
        # Visualization style
        viz_style = st.selectbox(
            "Visualization Style",
            ["Professional", "Colorful", "Minimal"],
            help="Select chart styling"
        )
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("[📖 Documentation](#)")
        st.markdown("[💡 Sample Reports](#)")
        st.markdown("[🐛 Report Issues](#)")
    
    # Main content area
    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=['xlsx', 'xls', 'csv'],
        help="Supported formats: .xlsx, .xls, .csv (Max 200MB)"
    )
    
    if uploaded_file is not None:
        # Initialize session state
        if 'analysis_complete' not in st.session_state:
            st.session_state.analysis_complete = False
        
        try:
            # File information
            file_details = {
                "Filename": uploaded_file.name,
                "File Size": f"{uploaded_file.size / 1024:.2f} KB",
                "Upload Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with st.expander("📁 File Information", expanded=True):
                cols = st.columns(3)
                for idx, (key, value) in enumerate(file_details.items()):
                    cols[idx].metric(key, value)
            
            # Load data
            with st.spinner("Loading data..."):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            
            # Data preview
            st.markdown("### 📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Dataset overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rows", f"{len(df):,}")
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Numeric Columns", len(df.select_dtypes(include=[np.number]).columns))
            with col4:
                st.metric("Missing Values", f"{df.isnull().sum().sum():,}")
            
            # Analyze button
            if st.button("🔍 Analyze Data", type="primary", use_container_width=True):
                analyze_data(df, ai_model, analysis_depth, viz_style)
                st.session_state.analysis_complete = True
            
            # Display results if analysis is complete
            if st.session_state.analysis_complete and 'results' in st.session_state:
                display_results(st.session_state.results)
                
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("Please ensure your file is a valid Excel or CSV file.")
    
    else:
        # Landing page when no file is uploaded
        st.markdown("### 👋 Welcome to Excel-to-Insights Bot")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 🎯 What We Do
            - Automated data cleaning
            - Statistical analysis
            - Smart visualizations
            - AI-powered insights
            """)
        
        with col2:
            st.markdown("""
            #### ⚡ Key Features
            - Upload & analyze in minutes
            - No coding required
            - Professional reports
            - Export to PDF/Excel
            """)
        
        with col3:
            st.markdown("""
            #### 📊 Supported Data
            - Sales & revenue data
            - Customer analytics
            - Financial reports
            - Operational metrics
            """)
        
        st.markdown("---")
        st.info("👆 Upload an Excel file to get started!")

def analyze_data(df, ai_model, analysis_depth, viz_style):
    """Perform comprehensive data analysis"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = {}
    
    try:
        # Step 1: Data Cleaning
        status_text.text("🧹 Cleaning and preprocessing data...")
        progress_bar.progress(20)
        processor = DataProcessor(df)
        cleaned_df, cleaning_report = processor.clean_data()
        results['cleaned_df'] = cleaned_df
        results['cleaning_report'] = cleaning_report
        
        # Step 2: Exploratory Data Analysis
        status_text.text("📊 Performing exploratory data analysis...")
        progress_bar.progress(40)
        eda_engine = EDAEngine(cleaned_df)
        eda_results = eda_engine.analyze()
        results['eda_results'] = eda_results
        
        # Step 3: Generate Visualizations
        status_text.text("📈 Creating visualizations...")
        progress_bar.progress(60)
        viz_engine = VisualizationEngine(cleaned_df, style=viz_style.lower())
        charts = viz_engine.generate_all_charts()
        results['charts'] = charts
        
        # Step 4: AI Insights Generation
        status_text.text("🤖 Generating AI-powered insights...")
        progress_bar.progress(80)
        ai_generator = AIInsightsGenerator(model=ai_model)
        insights = ai_generator.generate_insights(eda_results, cleaned_df)
        results['insights'] = insights
        
        # Step 5: Finalize
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(100)
        
        # Store results in session state
        st.session_state.results = results
        
        st.success("✨ Analysis completed successfully!")
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        st.exception(e)

def display_results(results):
    """Display analysis results in organized tabs"""
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    tabs = st.tabs([
        "🧹 Data Quality",
        "📈 Statistics",
        "📊 Visualizations",
        "🤖 AI Insights"
    ])
    
    # Tab 1: Data Quality
    with tabs[0]:
        st.markdown("### Data Cleaning Report")
        cleaning_report = results.get('cleaning_report', {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows Processed", cleaning_report.get('total_rows', 0))
        with col2:
            st.metric("Columns Cleaned", cleaning_report.get('columns_cleaned', 0))
        with col3:
            st.metric("Missing Values Handled", cleaning_report.get('missing_handled', 0))
        
        if cleaning_report.get('transformations'):
            st.markdown("#### Transformations Applied")
            for transformation in cleaning_report['transformations']:
                st.markdown(f"- {transformation}")
    
    # Tab 2: Statistics
    with tabs[1]:
        st.markdown("### Statistical Summary")
        eda_results = results.get('eda_results', {})
        
        if 'descriptive_stats' in eda_results:
            st.dataframe(eda_results['descriptive_stats'], use_container_width=True)
        
        if 'kpis' in eda_results:
            st.markdown("#### Key Performance Indicators")
            kpi_cols = st.columns(min(4, len(eda_results['kpis'])))
            for idx, (kpi_name, kpi_value) in enumerate(eda_results['kpis'].items()):
                with kpi_cols[idx % 4]:
                    st.metric(kpi_name, kpi_value)
    
    # Tab 3: Visualizations
    with tabs[2]:
        st.markdown("### Data Visualizations")
        charts = results.get('charts', {})
        
        if charts:
            for chart_name, chart_fig in charts.items():
                st.plotly_chart(chart_fig, use_container_width=True)
        else:
            st.info("No visualizations generated.")
    
    # Tab 4: AI Insights
    with tabs[3]:
        st.markdown("### AI-Generated Insights")
        insights = results.get('insights', {})
        
        if 'executive_summary' in insights:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("#### 📝 Executive Summary")
            st.markdown(insights['executive_summary'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        if 'key_findings' in insights:
            st.markdown("#### 🔍 Key Findings")
            for finding in insights['key_findings']:
                st.markdown(f"- {finding}")
        
        if 'recommendations' in insights:
            st.markdown("#### 💡 Recommendations")
            for rec in insights['recommendations']:
                st.markdown(f"- {rec}")
    


if __name__ == "__main__":
    main()
