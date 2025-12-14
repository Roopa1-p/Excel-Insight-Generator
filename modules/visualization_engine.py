"""
Visualization Engine
Automatically generates appropriate charts based on data characteristics
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns

class VisualizationEngine:
    """
    Intelligent chart generation based on data types and patterns
    """
    
    def __init__(self, df: pd.DataFrame, style: str = 'professional'):
        """
        Initialize Visualization Engine
        
        Args:
            df: Cleaned pandas DataFrame
            style: Visual style ('professional', 'colorful', 'minimal')
        """
        self.df = df
        self.style = style
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Set color scheme based on style
        self.color_scheme = self._get_color_scheme()
    
    def _get_color_scheme(self) -> Dict:
        """Get color palette based on selected style"""
        schemes = {
            'professional': {
                'primary': '#1f77b4',
                'secondary': '#ff7f0e',
                'palette': px.colors.qualitative.Set2
            },
            'colorful': {
                'primary': '#e74c3c',
                'secondary': '#3498db',
                'palette': px.colors.qualitative.Vivid
            },
            'minimal': {
                'primary': '#34495e',
                'secondary': '#95a5a6',
                'palette': px.colors.qualitative.Pastel
            }
        }
        return schemes.get(self.style, schemes['professional'])
    
    def generate_all_charts(self) -> Dict:
        """
        Generate all relevant charts automatically
        
        Returns:
            Dictionary of chart names and Plotly figure objects
        """
        charts = {}
        
        # 1. Distribution charts for numeric columns
        if self.numeric_cols:
            charts.update(self._create_distribution_charts())
        
        # 2. Categorical analysis charts
        if self.categorical_cols:
            charts.update(self._create_categorical_charts())
        
        # 3. Correlation heatmap
        if len(self.numeric_cols) >= 2:
            charts['Correlation Heatmap'] = self._create_correlation_heatmap()
        
        # 4. Time series charts
        if self.datetime_cols and self.numeric_cols:
            charts.update(self._create_time_series_charts())
        
        # 5. Comparison charts
        if self.categorical_cols and self.numeric_cols:
            charts.update(self._create_comparison_charts())
        
        # 6. Box plots for outlier detection
        if self.numeric_cols:
            charts['Box Plot Analysis'] = self._create_box_plots()
        
        return charts
    
    def _create_distribution_charts(self) -> Dict:
        """Create distribution visualizations for numeric columns"""
        charts = {}
        
        # Limit to first 3 numeric columns to avoid overwhelming
        for col in self.numeric_cols[:3]:
            # Histogram
            fig = px.histogram(
                self.df,
                x=col,
                nbins=30,
                title=f'Distribution of {col}',
                color_discrete_sequence=[self.color_scheme['primary']],
                marginal='box'  # Add box plot on top
            )
            
            fig.update_layout(
                showlegend=False,
                template='plotly_white',
                title_font_size=16,
                xaxis_title=col,
                yaxis_title='Frequency'
            )
            
            charts[f'Distribution: {col}'] = fig
        
        return charts
    
    def _create_categorical_charts(self) -> Dict:
        """Create charts for categorical variables"""
        charts = {}
        
        for col in self.categorical_cols[:3]:  # Limit to first 3
            value_counts = self.df[col].value_counts().head(10)  # Top 10 categories
            
            # Bar chart
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f'Top Categories in {col}',
                labels={'x': col, 'y': 'Count'},
                color=value_counts.values,
                color_continuous_scale=self.color_scheme['palette']
            )
            
            fig.update_layout(
                showlegend=False,
                template='plotly_white',
                title_font_size=16,
                xaxis_tickangle=-45
            )
            
            charts[f'Category Analysis: {col}'] = fig
            
            # Pie chart if <= 7 categories
            if len(value_counts) <= 7:
                fig_pie = px.pie(
                    values=value_counts.values,
                    names=value_counts.index,
                    title=f'Proportion of {col}',
                    color_discrete_sequence=self.color_scheme['palette']
                )
                
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                fig_pie.update_layout(template='plotly_white', title_font_size=16)
                
                charts[f'Pie Chart: {col}'] = fig_pie
        
        return charts
    
    def _create_correlation_heatmap(self) -> go.Figure:
        """Create correlation heatmap for numeric variables"""
        corr_matrix = self.df[self.numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto='.2f',
            aspect='auto',
            title='Correlation Matrix',
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1
        )
        
        fig.update_layout(
            template='plotly_white',
            title_font_size=16,
            width=700,
            height=600
        )
        
        return fig
    
    def _create_time_series_charts(self) -> Dict:
        """Create time-based trend charts"""
        charts = {}
        
        date_col = self.datetime_cols[0]  # Use first datetime column
        
        # Create time series for first 2 numeric columns
        for num_col in self.numeric_cols[:2]:
            # Sort by date
            df_sorted = self.df.sort_values(by=date_col)
            
            fig = px.line(
                df_sorted,
                x=date_col,
                y=num_col,
                title=f'{num_col} Over Time',
                markers=True
            )
            
            fig.update_traces(line_color=self.color_scheme['primary'], line_width=2)
            fig.update_layout(
                template='plotly_white',
                title_font_size=16,
                xaxis_title='Date',
                yaxis_title=num_col,
                hovermode='x unified'
            )
            
            charts[f'Time Series: {num_col}'] = fig
        
        return charts
    
    def _create_comparison_charts(self) -> Dict:
        """Create comparison charts between categorical and numeric variables"""
        charts = {}
        
        # Take first categorical and first numeric column
        if self.categorical_cols and self.numeric_cols:
            cat_col = self.categorical_cols[0]
            num_col = self.numeric_cols[0]
            
            # Group by category and calculate mean
            grouped = self.df.groupby(cat_col)[num_col].mean().sort_values(ascending=False).head(10)
            
            fig = px.bar(
                x=grouped.index,
                y=grouped.values,
                title=f'Average {num_col} by {cat_col}',
                labels={'x': cat_col, 'y': f'Average {num_col}'},
                color=grouped.values,
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(
                showlegend=False,
                template='plotly_white',
                title_font_size=16,
                xaxis_tickangle=-45
            )
            
            charts[f'Comparison: {num_col} by {cat_col}'] = fig
        
        return charts
    
    def _create_box_plots(self) -> go.Figure:
        """Create box plots for outlier detection"""
        # Limit to first 4 numeric columns
        cols_to_plot = self.numeric_cols[:4]
        
        fig = go.Figure()
        
        for col in cols_to_plot:
            fig.add_trace(go.Box(
                y=self.df[col],
                name=col,
                boxmean='sd'  # Show mean and standard deviation
            ))
        
        fig.update_layout(
            title='Box Plot Analysis - Outlier Detection',
            template='plotly_white',
            title_font_size=16,
            yaxis_title='Value',
            showlegend=True
        )
        
        return fig
    
    def create_custom_chart(self, chart_type: str, x_col: str, y_col: str = None, **kwargs) -> go.Figure:
        """
        Create a custom chart with specified parameters
        
        Args:
            chart_type: Type of chart ('bar', 'line', 'scatter', 'pie', etc.)
            x_col: Column for x-axis
            y_col: Column for y-axis (optional for some chart types)
            **kwargs: Additional parameters for the chart
        
        Returns:
            Plotly figure object
        """
        if chart_type == 'bar':
            fig = px.bar(self.df, x=x_col, y=y_col, **kwargs)
        elif chart_type == 'line':
            fig = px.line(self.df, x=x_col, y=y_col, **kwargs)
        elif chart_type == 'scatter':
            fig = px.scatter(self.df, x=x_col, y=y_col, **kwargs)
        elif chart_type == 'pie':
            fig = px.pie(self.df, names=x_col, values=y_col, **kwargs)
        elif chart_type == 'histogram':
            fig = px.histogram(self.df, x=x_col, **kwargs)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        fig.update_layout(template='plotly_white')
        return fig
