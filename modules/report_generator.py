"""
Report Generator Module
Creates PDF and Excel reports with insights and visualizations
"""

from fpdf import FPDF  # fpdf2 uses the same import name
import pandas as pd
from datetime import datetime
from typing import Dict, Any
import os

class ReportGenerator:
    """
    Generate professional PDF and Excel reports
    """
    
    def __init__(self):
        """Initialize Report Generator"""
        self.report_dir = "reports"
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate_pdf_report(
        self,
        cleaned_df: pd.DataFrame,
        eda_results: Dict,
        insights: Dict,
        charts: Dict
    ) -> str:
        """
        Generate comprehensive PDF report
        
        Args:
            cleaned_df: Cleaned DataFrame
            eda_results: EDA analysis results
            insights: AI-generated insights
            charts: Dictionary of chart figures
        
        Returns:
            Path to generated PDF file
        """
        pdf = PDFReport()
        
        # Cover page
        pdf.add_cover_page()
        
        # Executive summary
        pdf.add_executive_summary(insights)
        
        # Data overview
        pdf.add_data_overview(cleaned_df, eda_results)
        
        # Key findings
        pdf.add_key_findings(insights)
        
        # Statistical summary
        pdf.add_statistical_summary(eda_results)
        
        # Recommendations
        pdf.add_recommendations(insights)
        
        # Save PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/insights_report_{timestamp}.pdf"
        pdf.output(filename)
        
        return filename
    
    def generate_excel_report(
        self,
        cleaned_df: pd.DataFrame,
        eda_results: Dict
    ) -> str:
        """
        Generate Excel report with multiple sheets
        
        Args:
            cleaned_df: Cleaned DataFrame
            eda_results: EDA analysis results
        
        Returns:
            Path to generated Excel file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/data_analysis_{timestamp}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: Cleaned data
            cleaned_df.to_excel(writer, sheet_name='Cleaned Data', index=False)
            
            # Sheet 2: Descriptive statistics
            if 'descriptive_stats' in eda_results and not eda_results['descriptive_stats'].empty:
                eda_results['descriptive_stats'].to_excel(writer, sheet_name='Statistics')
            
            # Sheet 3: Correlation matrix
            if 'correlations' in eda_results and 'correlation_matrix' in eda_results['correlations']:
                eda_results['correlations']['correlation_matrix'].to_excel(writer, sheet_name='Correlations')
            
            # Sheet 4: KPIs
            if 'kpis' in eda_results:
                kpi_df = pd.DataFrame(list(eda_results['kpis'].items()), columns=['KPI', 'Value'])
                kpi_df.to_excel(writer, sheet_name='KPIs', index=False)
        
        return filename


class PDFReport(FPDF):
    """
    Custom PDF class with styling
    """
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        """Page header"""
        if self.page_no() > 1:  # Skip header on cover page
            self.set_font('Arial', 'B', 12)
            self.set_text_color(31, 119, 180)
            self.cell(0, 10, 'Excel-to-Insights Bot - Analysis Report', 0, 1, 'C')
            self.ln(5)
    
    def footer(self):
        """Page footer"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def add_cover_page(self):
        """Add cover page"""
        self.add_page()
        
        # Title
        self.set_font('Arial', 'B', 28)
        self.set_text_color(31, 119, 180)
        self.ln(60)
        self.cell(0, 20, 'Data Analysis Report', 0, 1, 'C')
        
        # Subtitle
        self.set_font('Arial', '', 16)
        self.set_text_color(100)
        self.cell(0, 10, 'Automated Insights & Recommendations', 0, 1, 'C')
        
        # Date
        self.ln(20)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'Generated on: {datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')
        
        # Logo/Icon (placeholder)
        self.ln(40)
        self.set_font('Arial', 'B', 48)
        self.set_text_color(31, 119, 180)
        self.cell(0, 20, '📊', 0, 1, 'C')
    
    def add_executive_summary(self, insights: Dict):
        """Add executive summary section"""
        self.add_page()
        
        self.set_font('Arial', 'B', 18)
        self.set_text_color(31, 119, 180)
        self.cell(0, 10, 'Executive Summary', 0, 1)
        self.ln(5)
        
        self.set_font('Arial', '', 11)
        self.set_text_color(0)
        
        summary = insights.get('executive_summary', 'No summary available.')
        self.multi_cell(0, 6, summary)
    
    def add_data_overview(self, df: pd.DataFrame, eda_results: Dict):
        """Add data overview section"""
        self.add_page()
        
        self.set_font('Arial', 'B', 18)
        self.set_text_color(31, 119, 180)
        self.cell(0, 10, 'Data Overview', 0, 1)
        self.ln(5)
        
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0)
        
        # Dataset dimensions
        self.cell(0, 8, f'Total Records: {len(df):,}', 0, 1)
        self.cell(0, 8, f'Total Variables: {len(df.columns)}', 0, 1)
        self.ln(5)
        
        # Column names
        self.cell(0, 8, 'Columns:', 0, 1)
        self.set_font('Arial', '', 10)
        
        # Display columns in a grid
        col_text = ', '.join(df.columns.tolist())
        self.multi_cell(0, 6, col_text)
    
    def add_key_findings(self, insights: Dict):
        """Add key findings section"""
        self.add_page()
        
        self.set_font('Arial', 'B', 18)
        self.set_text_color(31, 119, 180)
        self.cell(0, 10, 'Key Findings', 0, 1)
        self.ln(5)
        
        self.set_font('Arial', '', 11)
        self.set_text_color(0)
        
        findings = insights.get('key_findings', [])
        
        for i, finding in enumerate(findings, 1):
            self.set_font('Arial', 'B', 11)
            self.cell(10, 6, f'{i}.', 0, 0)
            self.set_font('Arial', '', 11)
            self.multi_cell(0, 6, finding)
            self.ln(2)
    
    def add_statistical_summary(self, eda_results: Dict):
        """Add statistical summary section"""
        self.add_page()
        
        self.set_font('Arial', 'B', 18)
        self.set_text_color(31, 119, 180)
        self.cell(0, 10, 'Statistical Summary', 0, 1)
        self.ln(5)
        
        # KPIs
        if 'kpis' in eda_results:
            self.set_font('Arial', 'B', 14)
            self.set_text_color(0)
            self.cell(0, 8, 'Key Performance Indicators', 0, 1)
            self.ln(3)
            
            self.set_font('Arial', '', 11)
            for kpi_name, kpi_value in eda_results['kpis'].items():
                self.cell(0, 6, f'{kpi_name}: {kpi_value}', 0, 1)
            
            self.ln(5)
        
        # Correlations
        if 'correlations' in eda_results:
            strong_corrs = eda_results['correlations'].get('strong_correlations', [])
            if strong_corrs:
                self.set_font('Arial', 'B', 14)
                self.cell(0, 8, 'Strong Correlations', 0, 1)
                self.ln(3)
                
                self.set_font('Arial', '', 11)
                for corr in strong_corrs[:5]:
                    text = f"{corr['var1']} ↔ {corr['var2']}: {corr['correlation']} ({corr['strength']})"
                    self.cell(0, 6, text, 0, 1)
    
    def add_recommendations(self, insights: Dict):
        """Add recommendations section"""
        self.add_page()
        
        self.set_font('Arial', 'B', 18)
        self.set_text_color(31, 119, 180)
        self.cell(0, 10, 'Recommendations', 0, 1)
        self.ln(5)
        
        self.set_font('Arial', '', 11)
        self.set_text_color(0)
        
        recommendations = insights.get('recommendations', [])
        
        for i, rec in enumerate(recommendations, 1):
            self.set_font('Arial', 'B', 11)
            self.cell(10, 6, f'{i}.', 0, 0)
            self.set_font('Arial', '', 11)
            self.multi_cell(0, 6, rec)
            self.ln(2)
