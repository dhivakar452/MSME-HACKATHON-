import pandas as pd
import numpy as np
from typing import Tuple, Optional

def clean_factory_data_csv(df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[str]]:
    """
    Cleans and preprocesses uploaded factory data CSV using Pandas.
    Uses: isnull(), fillna(), dropna(), astype(), read_csv() (simulated from dataframe).
    """
    try:
        # Standardize column names (lowercase and strip whitespace)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('electricity_bill', 'electricity_bill')
        
        # Verify required columns exist
        required_cols = [
            'date', 'sales', 'production', 'electricity_bill', 
            'raw_material_cost', 'salary', 'inventory', 
            'machine_running_hours', 'machine_downtime', 'profit'
        ]
        
        # Map synonyms to standardize if columns differ slightly (e.g. electricity vs electricity_bill)
        synonyms = {
            'electricity': 'electricity_bill',
            'raw_material': 'raw_material_cost',
            'running_hours': 'machine_running_hours',
            'downtime': 'machine_downtime'
        }
        for syn, target in synonyms.items():
            if syn in df.columns and target not in df.columns:
                df = df.rename(columns={syn: target})
                
        # Double check missing columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return df, f"Missing required columns: {', '.join(missing_cols)}"

        # 1. Drop rows where date, sales, or production is missing (critical fields) using dropna()
        critical_cols = ['date', 'sales', 'production']
        df = df.dropna(subset=critical_cols)
        
        # 2. Check for missing values in other fields using isnull() and fillna()
        # Default missing costs, inventory, or downtime to 0.0 or sensible averages
        numeric_fill_cols = [
            'electricity_bill', 'raw_material_cost', 'salary', 
            'inventory', 'machine_running_hours', 'machine_downtime'
        ]
        
        for col in numeric_fill_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(0.0)
                
        # 3. Calculate profit if it's missing or null
        if 'profit' not in df.columns or df['profit'].isnull().any():
            calculated_profit = df['sales'] - (df['raw_material_cost'] + df['salary'] + df['electricity_bill'])
            if 'profit' not in df.columns:
                df['profit'] = calculated_profit
            else:
                df['profit'] = df['profit'].fillna(calculated_profit)

        # 4. Enforce strict data types using astype()
        # Dates should be formatted string YYYY-MM-DD
        try:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        except Exception:
            return df, "Invalid date format. Dates must be parseable (e.g., YYYY-MM-DD)."
            
        df['date'] = df['date'].astype(str)
        
        numeric_types = {
            'sales': float,
            'production': float,
            'electricity_bill': float,
            'raw_material_cost': float,
            'salary': float,
            'inventory': float,
            'machine_running_hours': float,
            'machine_downtime': float,
            'profit': float
        }
        
        for col, dtype in numeric_types.items():
            df[col] = df[col].astype(dtype)
            
        # Drop duplicates based on date
        df = df.drop_duplicates(subset=['date'], keep='last')
        
        # Sort values by date to ensure proper timeline
        df = df.sort_values(by='date')
        
        return df, None
        
    except Exception as e:
        return df, f"Unexpected error during cleaning process: {str(e)}"
