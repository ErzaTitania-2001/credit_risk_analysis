import pandas as pd

df = pd.read_csv('borrowers.csv')

print("=" * 50)
print("DATASET ANALYSIS")
print("=" * 50)

print("\nFICO Score Statistics:")
print(df['fico_range_high'].describe())

print("\nFICO Score Distribution:")
print(f"Minimum FICO: {df['fico_range_high'].min()}")
print(f"Maximum FICO: {df['fico_range_high'].max()}")
print(f"Mean FICO: {df['fico_range_high'].mean():.2f}")
print(f"Median FICO: {df['fico_range_high'].median():.2f}")

print("\nIncome Statistics:")
print(f"Minimum Income: ${df['annual_inc'].min():,.2f}")
print(f"Maximum Income: ${df['annual_inc'].max():,.2f}")
print(f"Mean Income: ${df['annual_inc'].mean():,.2f}")

print("\n" + "=" * 50)
print("RISK SCORE SIMULATION")
print("=" * 50)

# Calculate risk scores for all borrowers
risk_scores = []
for _, row in df.iterrows():
    fico = row['fico_range_high']
    income = row['annual_inc']
    
    base_score = 100 - (fico / 8.5)
    if income > 80000:
        base_score -= 15
    
    final_score = max(0, min(100, base_score))
    risk_scores.append(final_score)

df['calculated_risk_score'] = risk_scores

print(f"\nRisk Score Statistics:")
print(f"Minimum Risk: {df['calculated_risk_score'].min():.2f}")
print(f"Maximum Risk: {df['calculated_risk_score'].max():.2f}")
print(f"Mean Risk: {df['calculated_risk_score'].mean():.2f}")

print("\nRisk Category Distribution:")
df['risk_category'] = df['calculated_risk_score'].apply(
    lambda x: 'Low' if x < 30 else ('Medium' if x < 60 else 'High')
)
print(df['risk_category'].value_counts())

print("\n" + "=" * 50)
print("SAMPLE BORROWERS")
print("=" * 50)

# Show worst cases (highest risk)
print("\nTop 5 Highest Risk Borrowers:")
worst = df.nlargest(5, 'calculated_risk_score')[['member_id', 'fico_range_high', 'annual_inc', 'loan_amnt', 'calculated_risk_score', 'risk_category']]
print(worst.to_string(index=False))

# Show best cases (lowest risk)
print("\nTop 5 Lowest Risk Borrowers:")
best = df.nsmallest(5, 'calculated_risk_score')[['member_id', 'fico_range_high', 'annual_inc', 'loan_amnt', 'calculated_risk_score', 'risk_category']]
print(best.to_string(index=False))

print("\n" + "=" * 50)
print("CONCLUSION")
print("=" * 50)

high_risk_count = len(df[df['calculated_risk_score'] >= 60])
medium_risk_count = len(df[(df['calculated_risk_score'] >= 30) & (df['calculated_risk_score'] < 60)])
low_risk_count = len(df[df['calculated_risk_score'] < 30])

print(f"\nTotal Borrowers: {len(df)}")
print(f"Low Risk (< 30): {low_risk_count} ({low_risk_count/len(df)*100:.1f}%)")
print(f"Medium Risk (30-60): {medium_risk_count} ({medium_risk_count/len(df)*100:.1f}%)")
print(f"High Risk (>= 60): {high_risk_count} ({high_risk_count/len(df)*100:.1f}%)")

if low_risk_count == len(df):
    print("\n⚠️ WARNING: ALL borrowers are LOW RISK!")
    print("This dataset contains only high-quality borrowers.")
    print("In real scenarios, you would have more risk diversity.")
