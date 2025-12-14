"""
Exploratory Data Analysis Engine
Performs comprehensive statistical analysis and KPI calculation
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Any
from datetime import datetime

class EDAEngine:
    """
    Automated Exploratory Data Analysis
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize EDA Engine
        
        Args:
            df: Cleaned pandas DataFrame
        """
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    def analyze(self) -> Dict[str, Any]:
        """
        Perform complete exploratory data analysis
        
        Returns:
            Dictionary containing all analysis results
        """
        results = {}
        
        # Descriptive statistics
        results['descriptive_stats'] = self._descriptive_statistics()
        
        # Correlation analysis
        results['correlations'] = self._correlation_analysis()
        
        # Distribution analysis
        results['distributions'] = self._distribution_analysis()
        
        # Categorical analysis
        results['categorical_analysis'] = self._categorical_analysis()
        
        # Time series analysis (if applicable)
        if self.datetime_cols:
            results['time_series'] = self._time_series_analysis()
        
        # Calculate KPIs
        results['kpis'] = self._calculate_kpis()
        
        # Detect trends
        results['trends'] = self._detect_trends()
        
        return results
    
    def _descriptive_statistics(self) -> pd.DataFrame:
        """Generate comprehensive descriptive statistics"""
        if not self.numeric_cols:
            return pd.DataFrame()
        
        stats_df = self.df[self.numeric_cols].describe()
        
        # Add additional statistics
        stats_df.loc['variance'] = self.df[self.numeric_cols].var()
        stats_df.loc['skewness'] = self.df[self.numeric_cols].skew()
        stats_df.loc['kurtosis'] = self.df[self.numeric_cols].kurtosis()
        stats_df.loc['range'] = self.df[self.numeric_cols].max() - self.df[self.numeric_cols].min()
        stats_df.loc['cv'] = (self.df[self.numeric_cols].std() / self.df[self.numeric_cols].mean()) * 100  # Coefficient of variation
        
        return stats_df.round(2)
    
    def _correlation_analysis(self) -> Dict:
        """Analyze correlations between numeric variables"""
        if len(self.numeric_cols) < 2:
            return {}
        
        corr_matrix = self.df[self.numeric_cols].corr()
        
        # Find strong correlations (> 0.7 or < -0.7)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': round(corr_value, 3),
                        'strength': 'Strong Positive' if corr_value > 0 else 'Strong Negative'
                    })
        
        return {
            'correlation_matrix': corr_matrix.round(3),
            'strong_correlations': strong_correlations
        }
    
    def _distribution_analysis(self) -> Dict:
        """Analyze distributions of numeric variables"""
        distributions = {}
        
        for col in self.numeric_cols:
            data = self.df[col].dropna()
            
            if len(data) > 0:
                distributions[col] = {
                    'mean': round(data.mean(), 2),
                    'median': round(data.median(), 2),
                    'mode': round(data.mode()[0], 2) if len(data.mode()) > 0 else None,
                    'std': round(data.std(), 2),
                    'skewness': round(data.skew(), 2),
                    'kurtosis': round(data.kurtosis(), 2),
                    'is_normal': self._test_normality(data)
                }
        
        return distributions
    
    def _test_normality(self, data: pd.Series) -> bool:
        """Test if data follows normal distribution using Shapiro-Wilk test"""
        if len(data) < 3 or len(data) > 5000:  # Shapiro-Wilk limitations
            return False
        
        try:
            _, p_value = stats.shapiro(data)
            return p_value > 0.05  # If p > 0.05, assume normal distribution
        except:
            return False
    
    def _categorical_analysis(self) -> Dict:
        """Analyze categorical variables"""
        categorical_info = {}
        
        for col in self.categorical_cols:
            value_counts = self.df[col].value_counts()
            
            categorical_info[col] = {
                'unique_values': self.df[col].nunique(),
                'most_common': value_counts.index[0] if len(value_counts) > 0 else None,
                'most_common_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                'most_common_pct': round((value_counts.iloc[0] / len(self.df)) * 100, 2) if len(value_counts) > 0 else 0,
                'top_5': value_counts.head(5).to_dict()
            }
        
        return categorical_info
    
    def _time_series_analysis(self) -> Dict:
        """Analyze time-based patterns"""
        time_analysis = {}
        
        for date_col in self.datetime_cols:
            # Sort by date
            df_sorted = self.df.sort_values(by=date_col)
            
            time_analysis[date_col] = {
                'date_range': {
                    'start': df_sorted[date_col].min(),
                    'end': df_sorted[date_col].max(),
                    'duration_days': (df_sorted[date_col].max() - df_sorted[date_col].min()).days
                },
                'frequency': self._detect_frequency(df_sorted[date_col])
            }
            
            # If there are numeric columns, analyze trends over time
            if self.numeric_cols:
                for num_col in self.numeric_cols[:3]:  # Limit to first 3 numeric columns
                    trend = self._calculate_trend(df_sorted, date_col, num_col)
                    if trend:
                        time_analysis[f'{num_col}_trend'] = trend
        
        return time_analysis
    
    def _detect_frequency(self, date_series: pd.Series) -> str:
        """Detect the frequency of time series data"""
        if len(date_series) < 2:
            return "Unknown"
        
        # Calculate median difference between consecutive dates
        diffs = date_series.diff().dropna()
        median_diff = diffs.median()
        
        if median_diff.days <= 1:
            return "Daily"
        elif median_diff.days <= 7:
            return "Weekly"
        elif median_diff.days <= 31:
            return "Monthly"
        elif median_diff.days <= 92:
            return "Quarterly"
        else:
            return "Yearly"
    
    def _calculate_trend(self, df: pd.DataFrame, date_col: str, value_col: str) -> Dict:
        """Calculate trend using linear regression"""
        try:
            # Convert dates to numeric (days since first date)
            df_temp = df[[date_col, value_col]].dropna()
            if len(df_temp) < 2:
                return None
            
            x = (df_temp[date_col] - df_temp[date_col].min()).dt.days.values
            y = df_temp[value_col].values
            
            # Linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # Calculate percentage change
            first_value = y[0]
            last_value = y[-1]
            pct_change = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0
            
            return {
                'slope': round(slope, 4),
                'direction': 'Increasing' if slope > 0 else 'Decreasing',
                'r_squared': round(r_value ** 2, 3),
                'percentage_change': round(pct_change, 2),
                'trend_strength': 'Strong' if abs(r_value) > 0.7 else 'Moderate' if abs(r_value) > 0.4 else 'Weak'
            }
        except:
            return None
    
    def _calculate_kpis(self) -> Dict:
        """Calculate domain-specific KPIs based on column names"""
        kpis = {}
        
        # Convert column names to lowercase for matching
        col_lower = {col: col.lower() for col in self.df.columns}
        reverse_map = {v: k for k, v in col_lower.items()}
        
        # Revenue/Sales KPIs
        revenue_cols = [col for col in col_lower.values() if any(keyword in col for keyword in ['revenue', 'sales', 'amount', 'total', 'price'])]
        if revenue_cols and revenue_cols[0] in reverse_map:
            actual_col = reverse_map[revenue_cols[0]]
            if actual_col in self.numeric_cols:
                kpis['Total Revenue'] = f"${self.df[actual_col].sum():,.2f}"
                kpis['Average Order Value'] = f"${self.df[actual_col].mean():,.2f}"
                kpis['Max Transaction'] = f"${self.df[actual_col].max():,.2f}"
        
        # Count-based KPIs
        kpis['Total Records'] = f"{len(self.df):,}"
        
        # Customer KPIs
        customer_cols = [col for col in col_lower.values() if any(keyword in col for keyword in ['customer', 'client', 'user'])]
        if customer_cols and customer_cols[0] in reverse_map:
            actual_col = reverse_map[customer_cols[0]]
            kpis['Unique Customers'] = f"{self.df[actual_col].nunique():,}"
        
        # Quantity KPIs
        qty_cols = [col for col in col_lower.values() if any(keyword in col for keyword in ['quantity', 'qty', 'count', 'units'])]
        if qty_cols and qty_cols[0] in reverse_map:
            actual_col = reverse_map[qty_cols[0]]
            if actual_col in self.numeric_cols:
                kpis['Total Units'] = f"{int(self.df[actual_col].sum()):,}"
        
        # Profit KPIs
        profit_cols = [col for col in col_lower.values() if 'profit' in col]
        if profit_cols and profit_cols[0] in reverse_map:
            actual_col = reverse_map[profit_cols[0]]
            if actual_col in self.numeric_cols:
                kpis['Total Profit'] = f"${self.df[actual_col].sum():,.2f}"
                kpis['Average Profit'] = f"${self.df[actual_col].mean():,.2f}"
        
        return kpis
    
    def _detect_trends(self) -> List[str]:
        """Detect and describe key trends in the data"""
        trends = []
        
        # Analyze numeric columns for trends
        for col in self.numeric_cols:
            data = self.df[col].dropna()
            
            if len(data) > 0:
                mean_val = data.mean()
                median_val = data.median()
                std_val = data.std()
                
                # High variability
                if std_val > mean_val:
                    trends.append(f"{col} shows high variability (std > mean)")
                
                # Skewed distribution
                skew = data.skew()
                if abs(skew) > 1:
                    direction = "right" if skew > 0 else "left"
                    trends.append(f"{col} is heavily skewed to the {direction}")
        
        # Analyze categorical columns
        for col in self.categorical_cols:
            value_counts = self.df[col].value_counts()
            if len(value_counts) > 0:
                top_pct = (value_counts.iloc[0] / len(self.df)) * 100
                if top_pct > 50:
                    trends.append(f"{col} is dominated by '{value_counts.index[0]}' ({top_pct:.1f}%)")
        
        return trends
