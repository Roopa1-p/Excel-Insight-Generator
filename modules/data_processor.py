"""
Data Processor Module
Handles data ingestion, cleaning, and preprocessing
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List
import re

class DataProcessor:
    """
    Automated data cleaning and preprocessing pipeline
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize DataProcessor with a DataFrame
        
        Args:
            df: Input pandas DataFrame
        """
        self.df = df.copy()
        self.original_shape = df.shape
        self.transformations = []
        
    def clean_data(self) -> Tuple[pd.DataFrame, Dict]:
        """
        Execute complete data cleaning pipeline
        
        Returns:
            Tuple of (cleaned_df, cleaning_report)
        """
        # Remove duplicate rows
        self._remove_duplicates()
        
        # Handle missing values
        self._handle_missing_values()
        
        # Clean column names
        self._clean_column_names()
        
        # Infer and convert data types
        self._infer_data_types()
        
        # Remove outliers (optional, flagged only)
        outliers_info = self._detect_outliers()
        
        # Generate cleaning report
        report = self._generate_report(outliers_info)
        
        return self.df, report
    
    def _remove_duplicates(self):
        """Remove duplicate rows"""
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_rows - len(self.df)
        
        if removed > 0:
            self.transformations.append(f"Removed {removed} duplicate rows")
    
    def _handle_missing_values(self):
        """Handle missing values intelligently"""
        missing_count = 0
        
        for column in self.df.columns:
            missing = self.df[column].isnull().sum()
            
            if missing > 0:
                missing_pct = (missing / len(self.df)) * 100
                
                # Drop column if >50% missing
                if missing_pct > 50:
                    self.df = self.df.drop(columns=[column])
                    self.transformations.append(f"Dropped column '{column}' ({missing_pct:.1f}% missing)")
                    missing_count += missing
                    continue
                
                # Handle numeric columns
                if self.df[column].dtype in ['int64', 'float64']:
                    # Use median for skewed data, mean for normal
                    if abs(self.df[column].skew()) > 1:
                        fill_value = self.df[column].median()
                        method = "median"
                    else:
                        fill_value = self.df[column].mean()
                        method = "mean"
                    
                    self.df[column].fillna(fill_value, inplace=True)
                    self.transformations.append(f"Filled {missing} missing values in '{column}' with {method}")
                    missing_count += missing
                
                # Handle categorical columns
                else:
                    mode_value = self.df[column].mode()
                    if len(mode_value) > 0:
                        self.df[column].fillna(mode_value[0], inplace=True)
                        self.transformations.append(f"Filled {missing} missing values in '{column}' with mode")
                        missing_count += missing
                    else:
                        self.df[column].fillna("Unknown", inplace=True)
                        self.transformations.append(f"Filled {missing} missing values in '{column}' with 'Unknown'")
                        missing_count += missing
        
        return missing_count
    
    def _clean_column_names(self):
        """Standardize column names"""
        original_columns = self.df.columns.tolist()
        
        # Remove special characters, convert to snake_case
        new_columns = []
        for col in self.df.columns:
            # Remove special characters
            clean_col = re.sub(r'[^a-zA-Z0-9\s]', '', str(col))
            # Replace spaces with underscores
            clean_col = clean_col.strip().replace(' ', '_')
            # Convert to lowercase
            clean_col = clean_col.lower()
            new_columns.append(clean_col)
        
        self.df.columns = new_columns
        
        if original_columns != new_columns:
            self.transformations.append("Standardized column names to snake_case")
    
    def _infer_data_types(self):
        """Intelligently infer and convert data types"""
        for column in self.df.columns:
            # Try to convert to numeric
            if self.df[column].dtype == 'object':
                # Check if it's a currency value
                if self.df[column].astype(str).str.contains(r'[\$€£¥]', regex=True, na=False).any():
                    self.df[column] = self.df[column].astype(str).str.replace(r'[\$€£¥,]', '', regex=True)
                    try:
                        self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
                        self.transformations.append(f"Converted '{column}' from currency to numeric")
                    except:
                        pass
                
                # Check if it's a percentage
                elif self.df[column].astype(str).str.contains('%', na=False).any():
                    self.df[column] = self.df[column].astype(str).str.replace('%', '', regex=False)
                    try:
                        self.df[column] = pd.to_numeric(self.df[column], errors='coerce') / 100
                        self.transformations.append(f"Converted '{column}' from percentage to decimal")
                    except:
                        pass
                
                # Try to parse as datetime
                elif self._is_likely_date(column):
                    try:
                        self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
                        self.transformations.append(f"Converted '{column}' to datetime")
                    except:
                        pass
                
                # Try general numeric conversion
                else:
                    try:
                        converted = pd.to_numeric(self.df[column], errors='coerce')
                        # Only convert if most values are numeric
                        if converted.notna().sum() / len(self.df) > 0.8:
                            self.df[column] = converted
                            self.transformations.append(f"Converted '{column}' to numeric")
                    except:
                        pass
    
    def _is_likely_date(self, column: str) -> bool:
        """Check if column name suggests it's a date"""
        date_keywords = ['date', 'time', 'day', 'month', 'year', 'timestamp', 'created', 'updated']
        return any(keyword in column.lower() for keyword in date_keywords)
    
    def _detect_outliers(self) -> Dict:
        """Detect outliers using IQR method"""
        outliers_info = {}
        
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
            
            if len(outliers) > 0:
                outliers_info[column] = {
                    'count': len(outliers),
                    'percentage': (len(outliers) / len(self.df)) * 100,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
        
        return outliers_info
    
    def _generate_report(self, outliers_info: Dict) -> Dict:
        """Generate comprehensive cleaning report"""
        report = {
            'original_shape': self.original_shape,
            'final_shape': self.df.shape,
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'columns_cleaned': len(self.df.columns),
            'missing_handled': sum(1 for t in self.transformations if 'Filled' in t or 'Dropped' in t),
            'transformations': self.transformations,
            'outliers_detected': outliers_info,
            'data_types': self.df.dtypes.astype(str).to_dict(),
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        }
        
        return report
