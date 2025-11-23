# Kaggle Dataset Loader for Credit Risk API
# This script downloads and prepares Kaggle credit datasets

import os
import pandas as pd
from pathlib import Path

class KaggleDataLoader:
    """Load and prepare credit datasets from Kaggle"""
    
    def __init__(self, kaggle_dir='./kaggle_data'):
        self.kaggle_dir = kaggle_dir
        Path(kaggle_dir).mkdir(exist_ok=True)
    
    def download_lending_club(self):
        """Download Lending Club dataset from Kaggle"""
        print("Downloading Lending Club dataset...")
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            import zipfile
            
            api = KaggleApi()
            api.authenticate()
            
            # Download dataset
            api.dataset_download_files('wordsforthewise/lending-club', 
                                      path=self.kaggle_dir, 
                                      unzip=True)
            print("✓ Download complete!")
            return self.load_lending_club()
            
        except Exception as e:
            print(f"Error downloading: {e}")
            print("Please download manually from https://www.kaggle.com/datasets/wordsforthewise/lending-club")
            raise
    
    def load_lending_club(self):
        """Load and prepare Lending Club data"""
        # Try different possible filenames
        possible_files = [
            './kaggle_data/accepted_2007_to_2018Q4.csv',
            './kaggle_data/lending_club.csv',
            './kaggle_data/loan.csv'
        ]
        
        for filepath in possible_files:
            if os.path.exists(filepath):
                print(f"Loading {filepath}...")
                df = pd.read_csv(filepath, low_memory=False)
                return self.prepare_data(df)
        
        raise FileNotFoundError("No Lending Club dataset found")
    
    def prepare_data(self, df):
        """Prepare Kaggle data to match our API schema"""
        print(f"Original dataset: {len(df)} rows, {len(df.columns)} columns")
        
        # Map Kaggle columns to our schema
        column_mapping = {
            'id': 'member_id',
            'loan_amnt': 'loan_amnt',
            'annual_inc': 'annual_inc',
            'loan_status': 'loan_status',
            'fico_range_high': 'fico_range_high'
        }
        
        # Select and rename columns
        required_cols = ['member_id', 'loan_amnt', 'annual_inc', 'loan_status', 'fico_range_high']
        
        # Try to find matching columns
        if 'id' in df.columns:
            df = df.rename(columns={'id': 'member_id'})
        
        # Filter for required columns
        available_cols = [col for col in required_cols if col in df.columns]
        df_filtered = df[available_cols].copy()
        
        # Remove rows with missing critical data
        df_filtered = df_filtered.dropna(subset=['member_id', 'loan_amnt', 'annual_inc', 'fico_range_high'])
        
        # Convert types
        df_filtered['member_id'] = df_filtered['member_id'].astype(int)
        df_filtered['loan_amnt'] = df_filtered['loan_amnt'].astype(float)
        df_filtered['annual_inc'] = df_filtered['annual_inc'].astype(float)
        df_filtered['fico_range_high'] = df_filtered['fico_range_high'].astype(int)
        
        # Filter for reasonable values
        df_filtered = df_filtered[
            (df_filtered['fico_range_high'] >= 300) & 
            (df_filtered['fico_range_high'] <= 850) &
            (df_filtered['annual_inc'] > 0) &
            (df_filtered['loan_amnt'] > 0)
        ]
        
        print(f"Prepared dataset: {len(df_filtered)} rows")
        return df_filtered
    
    def sample_diverse_data(self, df, n=200):
        """Sample diverse risk profiles for demo"""
        # Create risk score column
        df['risk_score'] = 100 - (df['fico_range_high'] / 8.5)
        df.loc[df['annual_inc'] > 80000, 'risk_score'] -= 15
        df['risk_score'] = df['risk_score'].clip(0, 100)
        
        # Sample from different risk tiers
        low_risk = df[df['risk_score'] < 30].sample(min(140, len(df[df['risk_score'] < 30])))
        medium_risk = df[(df['risk_score'] >= 30) & (df['risk_score'] < 60)].sample(min(40, len(df[(df['risk_score'] >= 30) & (df['risk_score'] < 60)])))
        high_risk = df[df['risk_score'] >= 60].sample(min(20, len(df[df['risk_score'] >= 60])))
        
        sampled = pd.concat([low_risk, medium_risk, high_risk])
        sampled = sampled.drop('risk_score', axis=1)
        
        return sampled.reset_index(drop=True)
    
    def save_to_csv(self, df, filename='borrowers.csv'):
        """Save prepared data to CSV"""
        df.to_csv(filename, index=False)
        print(f"Saved {len(df)} records to {filename}")

# Example usage
if __name__ == "__main__":
    loader = KaggleDataLoader()
    
    # Option 1: Download from Kaggle (requires API key)
    try:
        df = loader.download_lending_club()
    except:
        # Option 2: Load existing Kaggle data
        try:
            df = loader.load_lending_club()
        except:
            print("No Kaggle data found. Please download manually.")
            exit(1)
    
    # Sample diverse data for demo (200 records with risk variety)
    df_sampled = loader.sample_diverse_data(df, n=200)
    
    # Show statistics
    print("\n" + "="*50)
    print("DATASET STATISTICS")
    print("="*50)
    print(f"\nFICO Range: {df_sampled['fico_range_high'].min()} - {df_sampled['fico_range_high'].max()}")
    print(f"Income Range: ${df_sampled['annual_inc'].min():,.0f} - ${df_sampled['annual_inc'].max():,.0f}")
    print(f"Loan Range: ${df_sampled['loan_amnt'].min():,.0f} - ${df_sampled['loan_amnt'].max():,.0f}")
    
    # Save to borrowers.csv
    loader.save_to_csv(df_sampled, 'borrowers.csv')
    
    print("\n✅ Dataset ready! Restart your Flask server to use it.")
