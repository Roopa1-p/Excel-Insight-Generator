"""
Generate sample sales dataset for testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate dates
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=x) for x in range(365)]

# Generate sample data
n_records = 1000

data = {
    'Date': np.random.choice(dates, n_records),
    'Product': np.random.choice(['Widget A', 'Widget B', 'Widget C', 'Widget D', 'Product E'], n_records),
    'Region': np.random.choice(['North America', 'Europe', 'Asia', 'South America'], n_records),
    'Sales_Amount': np.random.uniform(50, 5000, n_records).round(2),
    'Quantity': np.random.randint(1, 100, n_records),
    'Customer_ID': np.random.randint(1000, 5000, n_records),
    'Category': np.random.choice(['Electronics', 'Furniture', 'Clothing', 'Food'], n_records),
    'Discount_Percent': np.random.choice([0, 5, 10, 15, 20], n_records),
    'Shipping_Cost': np.random.uniform(5, 50, n_records).round(2),
    'Profit': np.random.uniform(-100, 1000, n_records).round(2)
}

# Create DataFrame
df = pd.DataFrame(data)

# Add some missing values (5%)
for col in ['Sales_Amount', 'Quantity', 'Profit']:
    mask = np.random.random(n_records) < 0.05
    df.loc[mask, col] = np.nan

# Sort by date
df = df.sort_values('Date').reset_index(drop=True)

# Save to Excel
df.to_excel('sample_data/sales_data_2023.xlsx', index=False)
print(f"Sample dataset created: {len(df)} records")
print(f"Columns: {', '.join(df.columns)}")
print(f"\nFirst few rows:")
print(df.head())
