# Process existing Kaggle Lending Club data
import pandas as pd
import numpy as np

print("="*60)
print("PROCESSING LENDING CLUB DATA")
print("="*60)

# Load both accepted and rejected loans
print("\n1. Loading ACCEPTED loans (accepted_2007_to_2018Q4.csv.gz)...")
df_accepted = pd.read_csv('./kaggle_data/accepted_2007_to_2018Q4.csv.gz', compression='gzip', low_memory=False, nrows=100000)
print(f"   Loaded {len(df_accepted)} accepted loans, {len(df_accepted.columns)} columns")

print("\n2. Loading REJECTED loans (rejected_2007_to_2018Q4.csv.gz)...")
df_rejected = pd.read_csv('./kaggle_data/rejected_2007_to_2018Q4.csv.gz', compression='gzip', low_memory=False, nrows=100000)
print(f"   Loaded {len(df_rejected)} rejected loans, {len(df_rejected.columns)} columns")

print(f"\nAccepted columns: {list(df_accepted.columns[:20])}...")
print(f"Rejected columns: {list(df_rejected.columns[:10])}...")

# Process ACCEPTED loans
print("\n3. Processing ACCEPTED loans...")
accepted_map = {
    'id': 'member_id',
    'loan_amnt': 'loan_amnt', 
    'annual_inc': 'annual_inc',
    'fico_range_high': 'fico_range_high',
    'loan_status': 'loan_status'
}
accepted_available = {k: v for k, v in accepted_map.items() if k in df_accepted.columns}
df_accepted_filtered = df_accepted[list(accepted_available.keys())].copy()
df_accepted_filtered.columns = [accepted_available[col] for col in df_accepted_filtered.columns]
df_accepted_filtered['loan_status'] = df_accepted_filtered.get('loan_status', 'Fully Paid')
print(f"   Mapped {len(df_accepted_filtered)} accepted records")

# Process REJECTED loans
print("\n4. Processing REJECTED loans...")
# Rejected loans have different column names
rejected_map = {
    'Amount Requested': 'loan_amnt',
    'Loan Title': 'loan_status',  # Will set to 'Declined'
}

# Check for Risk_Score or FICO columns in rejected data
if 'Risk_Score' in df_rejected.columns:
    # Use Risk_Score to estimate FICO (higher risk = lower FICO)
    df_rejected['fico_range_high'] = (100 - df_rejected['Risk_Score']) * 6 + 300
    df_rejected['fico_range_high'] = df_rejected['fico_range_high'].clip(300, 850)

# Estimate annual income from debt-to-income ratio if available
if 'Amount Requested' in df_rejected.columns and 'Debt-To-Income Ratio' in df_rejected.columns:
    # Parse DTI (format: "27.65%")
    df_rejected['dti_numeric'] = df_rejected['Debt-To-Income Ratio'].str.rstrip('%').astype(float) / 100
    # Estimate income: loan_amnt / DTI (rough approximation)
    df_rejected['annual_inc'] = (df_rejected['Amount Requested'] / df_rejected['dti_numeric']).clip(upper=500000)
elif 'Amount Requested' in df_rejected.columns:
    # Fallback: estimate based on loan amount (loan is typically 0.5-2x annual income)
    df_rejected['annual_inc'] = df_rejected['Amount Requested'] * np.random.uniform(0.8, 2.5, len(df_rejected))

# Build rejected dataframe
rejected_cols = []
if 'Amount Requested' in df_rejected.columns:
    rejected_cols.append('Amount Requested')
if 'annual_inc' in df_rejected.columns:
    rejected_cols.append('annual_inc')
if 'fico_range_high' in df_rejected.columns:
    rejected_cols.append('fico_range_high')

if rejected_cols:
    df_rejected_filtered = df_rejected[rejected_cols].copy()
    df_rejected_filtered.columns = ['loan_amnt' if c == 'Amount Requested' else c for c in df_rejected_filtered.columns]
    # Add member_id (use negative numbers to distinguish from accepted)
    df_rejected_filtered['member_id'] = range(-1, -len(df_rejected_filtered)-1, -1)
    df_rejected_filtered['loan_status'] = 'Declined'
    print(f"   Mapped {len(df_rejected_filtered)} rejected records")
else:
    df_rejected_filtered = pd.DataFrame()
    print("   ⚠ Could not map rejected loans (missing columns)")

# Combine accepted and rejected
print("\n5. Combining datasets...")
if not df_rejected_filtered.empty:
    df_filtered = pd.concat([df_accepted_filtered, df_rejected_filtered], ignore_index=True)
    print(f"   Total: {len(df_filtered)} records ({len(df_accepted_filtered)} accepted + {len(df_rejected_filtered)} rejected)")
else:
    df_filtered = df_accepted_filtered
    print(f"   Using only accepted: {len(df_filtered)} records")

# Clean data
print("\nCleaning data...")
print(f"  Before cleaning: {len(df_filtered)} rows")

# Remove rows with missing critical data
df_filtered = df_filtered.dropna(subset=['member_id', 'loan_amnt', 'annual_inc', 'fico_range_high'])

# Convert types
df_filtered['member_id'] = df_filtered['member_id'].astype(int)
df_filtered['loan_amnt'] = pd.to_numeric(df_filtered['loan_amnt'], errors='coerce')
df_filtered['annual_inc'] = pd.to_numeric(df_filtered['annual_inc'], errors='coerce')
df_filtered['fico_range_high'] = pd.to_numeric(df_filtered['fico_range_high'], errors='coerce')

# Remove any rows where conversion failed
df_filtered = df_filtered.dropna()

# Filter for reasonable values
df_filtered = df_filtered[
    (df_filtered['fico_range_high'] >= 300) & 
    (df_filtered['fico_range_high'] <= 850) &
    (df_filtered['annual_inc'] > 0) &
    (df_filtered['annual_inc'] < 10000000) &  # Remove outliers
    (df_filtered['loan_amnt'] > 0)
]

print(f"  After cleaning: {len(df_filtered)} rows")

# Calculate risk scores for sampling
print("\nCalculating risk scores...")
df_filtered['risk_score'] = 100 - (df_filtered['fico_range_high'] / 8.5)
df_filtered.loc[df_filtered['annual_inc'] > 80000, 'risk_score'] -= 15
df_filtered['risk_score'] = df_filtered['risk_score'].clip(0, 100)

# Sample diverse profiles
print("\nSampling diverse risk profiles...")
low_risk = df_filtered[df_filtered['risk_score'] < 30]
medium_risk = df_filtered[(df_filtered['risk_score'] >= 30) & (df_filtered['risk_score'] < 60)]
high_risk = df_filtered[df_filtered['risk_score'] >= 60]

print(f"  Low risk available: {len(low_risk)}")
print(f"  Medium risk available: {len(medium_risk)}")
print(f"  High risk available: {len(high_risk)}")

# Sample 200 records with diversity
n_low = min(140, len(low_risk))
n_medium = min(40, len(medium_risk))
n_high = min(20, len(high_risk))

sampled = pd.concat([
    low_risk.sample(n_low) if n_low > 0 else pd.DataFrame(),
    medium_risk.sample(n_medium) if n_medium > 0 else pd.DataFrame(),
    high_risk.sample(n_high) if n_high > 0 else pd.DataFrame()
])

# Drop the risk_score column (it was just for sampling)
sampled = sampled.drop('risk_score', axis=1).reset_index(drop=True)

# Show statistics
print("\n" + "="*60)
print("FINAL DATASET STATISTICS")
print("="*60)
print(f"\nTotal records: {len(sampled)}")
print(f"  Low risk: {n_low}")
print(f"  Medium risk: {n_medium}")
print(f"  High risk: {n_high}")

print(f"\nFICO Range: {sampled['fico_range_high'].min():.0f} - {sampled['fico_range_high'].max():.0f}")
print(f"Mean FICO: {sampled['fico_range_high'].mean():.2f}")

print(f"\nIncome Range: ${sampled['annual_inc'].min():,.0f} - ${sampled['annual_inc'].max():,.0f}")
print(f"Mean Income: ${sampled['annual_inc'].mean():,.0f}")

print(f"\nLoan Range: ${sampled['loan_amnt'].min():,.0f} - ${sampled['loan_amnt'].max():,.0f}")
print(f"Mean Loan: ${sampled['loan_amnt'].mean():,.0f}")

# Save to borrowers.csv
output_file = 'borrowers.csv'
sampled.to_csv(output_file, index=False)

print(f"\n✓ Saved {len(sampled)} records to {output_file}")
print("\n" + "="*60)
print("SUCCESS! Dataset ready for your API")
print("="*60)
print("\nNext steps:")
print("  1. Restart your Flask server: python app.py")
print("  2. Test: .\\test_api.ps1")
print("  3. Your API now uses real Kaggle Lending Club data!")
