import pandas as pd
import numpy as np
from scipy import stats
import re

def clean_column_names(df):
    """Clean column names by removing special characters and converting to lowercase"""
    df.columns = [re.sub(r'[^a-zA-Z0-9]', '_', col).lower() for col in df.columns]
    return df

def handle_missing_values(df, strategy='mean'):
    """Handle missing values based on specified strategy"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if strategy == 'mean':
        for col in numeric_cols:
            df[col].fillna(df[col].mean(), inplace=True)
    elif strategy == 'median':
        for col in numeric_cols:
            df[col].fillna(df[col].median(), inplace=True)
    elif strategy == 'drop':
        df.dropna(inplace=True)
    
    # For categorical columns, fill with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
    
    return df

def detect_and_handle_outliers(df, threshold=3):
    """Detect and handle outliers using Z-score method"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        z_scores = np.abs(stats.zscore(df[col]))
        outlier_indices = np.where(z_scores > threshold)[0]
        if len(outlier_indices) > 0:
            # Replace outliers with median
            median_val = df[col].median()
            df.loc[outlier_indices, col] = median_val
    
    return df

def convert_date_columns(df):
    """Attempt to convert object columns to datetime"""
    for col in df.select_dtypes(include=['object']).columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except (ValueError, TypeError):
            continue
    return df

def preprocess_data(df):
    """Main preprocessing function"""
    df = clean_column_names(df)
    df = convert_date_columns(df)
    df = handle_missing_values(df, strategy='mean')
    df = detect_and_handle_outliers(df)
    df.drop_duplicates(inplace=True)
    return df

def perform_eda(df):
    """Perform exploratory data analysis"""
    eda_results = {}
    
    # Basic statistics
    eda_results['shape'] = df.shape
    eda_results['dtypes'] = df.dtypes.to_dict()
    eda_results['describe'] = df.describe().to_dict()
    eda_results['null_counts'] = df.isnull().sum().to_dict()
    
    # Correlation matrix
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        eda_results['correlation'] = numeric_df.corr().to_dict()
    
    # Top categories for object columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    eda_results['value_counts'] = {}
    for col in categorical_cols:
        eda_results['value_counts'][col] = df[col].value_counts().head(10).to_dict()
    
    return eda_results