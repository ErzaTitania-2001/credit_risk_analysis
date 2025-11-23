# Step-by-Step Guide: Connect Kaggle Database to Your Credit Risk API

## Prerequisites
- Kaggle account
- Kaggle API key
- Python with pandas

---

## 🚀 Quick Start (5 minutes)

### 1. Install Kaggle CLI
```powershell
pip install kaggle
```

### 2. Get Your Kaggle API Key

1. Go to: https://www.kaggle.com/account
2. Scroll down to **API** section
3. Click **"Create New Token"**
4. Download `kaggle.json`

### 3. Set Up Credentials

**Windows:**
```powershell
# Create .kaggle directory
mkdir C:\Users\puppy\.kaggle

# Move your kaggle.json there
Move-Item .\kaggle.json C:\Users\puppy\.kaggle\

# Verify
Test-Path C:\Users\puppy\.kaggle\kaggle.json
```

### 4. Download Credit Dataset

**Option A: Lending Club (Best for Credit Risk)**
```powershell
# Download dataset
kaggle datasets download -d wordsforthewise/lending-club

# Extract
Expand-Archive -Path lending-club.zip -DestinationPath ./kaggle_data
```

**Option B: Credit Card Default**
```powershell
kaggle datasets download -d uciml/default-of-credit-card-clients-dataset
```

### 5. Process and Load Data

```powershell
# Run the loader script
python load_kaggle_data.py
```

This will:
- Load the Kaggle dataset
- Map columns to your API schema
- Sample diverse risk profiles (low/medium/high)
- Save to `borrowers.csv`
- Ready to use!

### 6. Restart Your Server

```powershell
python app.py
```

You'll see:
```
Successfully loaded borrowers.csv with 200 records
```

---

## 📊 Popular Credit Datasets on Kaggle

### 1. Lending Club Loan Data ⭐ RECOMMENDED
- **Dataset**: `wordsforthewise/lending-club`
- **Size**: 2+ million loans
- **Columns**: loan_amnt, annual_inc, fico_range_high, loan_status
- **Perfect match for your API!**

```powershell
kaggle datasets download -d wordsforthewise/lending-club
```

### 2. Home Credit Default Risk
- **Dataset**: `c/home-credit-default-risk`
- **Size**: 300k+ applications
- **Use case**: Credit default prediction

```powershell
kaggle datasets download -d c/home-credit-default-risk
```

### 3. Credit Card Default
- **Dataset**: `uciml/default-of-credit-card-clients-dataset`
- **Size**: 30k records
- **Columns**: LIMIT_BAL, SEX, EDUCATION, AGE, PAY_0-6

```powershell
kaggle datasets download -d uciml/default-of-credit-card-clients-dataset
```

---

## 🔧 Manual Method (If Kaggle API Doesn't Work)

### Option 1: Browser Download
1. Go to https://www.kaggle.com/datasets
2. Search: "lending club" or "credit risk"
3. Click **Download** button
4. Extract to `./kaggle_data/`
5. Run: `python load_kaggle_data.py`

### Option 2: Direct CSV Upload
1. Download CSV from Kaggle website
2. Place in project folder
3. Modify the script to point to your CSV:

```python
df = pd.read_csv('your_kaggle_file.csv')
```

---

## 🎯 What the Loader Script Does

1. **Downloads** dataset from Kaggle (or loads existing)
2. **Maps** Kaggle columns to your API schema:
   - `id` → `member_id`
   - `loan_amnt` → `loan_amnt`
   - `annual_inc` → `annual_inc`
   - `fico_range_high` → `fico_range_high`
3. **Cleans** data:
   - Removes missing values
   - Filters unrealistic FICO scores
   - Validates income/loan amounts
4. **Samples** diverse profiles:
   - 70% Low risk (auto-approve)
   - 20% Medium risk (manual review)
   - 10% High risk (decline)
5. **Saves** to `borrowers.csv`

---

## 📝 Customize the Loader

Edit `load_kaggle_data.py` to change:

### Change Sample Size
```python
df_sampled = loader.sample_diverse_data(df, n=500)  # Get 500 records
```

### Change Risk Distribution
```python
low_risk = df[df['risk_score'] < 30].sample(400)      # 80% low risk
medium_risk = df[...].sample(80)                      # 16% medium risk
high_risk = df[df['risk_score'] >= 60].sample(20)     # 4% high risk
```

### Filter by Loan Status
```python
df_approved = df[df['loan_status'] == 'Fully Paid']
df_defaulted = df[df['loan_status'] == 'Charged Off']
```

---

## 🧪 Test After Loading

```powershell
# Check new dataset
python analyze_dataset.py

# Test API
.\test_api.ps1

# Open demo interface
# Browser: http://localhost:5000/demo.html
```

---

## 🚨 Troubleshooting

### "401 Unauthorized" Error
```powershell
# Check if kaggle.json exists
Test-Path C:\Users\puppy\.kaggle\kaggle.json

# Re-download token from Kaggle
```

### "Dataset not found" Error
```powershell
# List available datasets
kaggle datasets list -s "lending club"

# Use exact dataset name
kaggle datasets download -d wordsforthewise/lending-club
```

### "Permission denied" on kaggle.json
```powershell
# Fix permissions (Windows)
icacls C:\Users\puppy\.kaggle\kaggle.json /inheritance:r /grant:r "$($env:USERNAME):F"
```

### Script can't find CSV
```python
# Modify load_kaggle_data.py line 32
# Add your actual CSV path
df = pd.read_csv('./kaggle_data/your_actual_file.csv')
```

---

## 🎬 Complete Workflow Example

```powershell
# 1. Install Kaggle CLI
pip install kaggle

# 2. Set up credentials (one-time)
# Download kaggle.json from Kaggle website
mkdir C:\Users\puppy\.kaggle
Move-Item .\kaggle.json C:\Users\puppy\.kaggle\

# 3. Download dataset
kaggle datasets download -d wordsforthewise/lending-club

# 4. Extract
Expand-Archive -Path lending-club.zip -DestinationPath ./kaggle_data

# 5. Process and load
python load_kaggle_data.py

# 6. Verify
python analyze_dataset.py

# 7. Start server with new data
python app.py

# 8. Test
.\test_api.ps1
```

---

## 💡 Alternative: Use Kaggle Directly in app.py

Modify `app.py` to load from Kaggle on startup:

```python
# Add at top of app.py
from load_kaggle_data import KaggleDataLoader

try:
    df = pd.read_csv('borrowers.csv')
except:
    # Fallback: Load from Kaggle
    print("Loading data from Kaggle...")
    loader = KaggleDataLoader()
    df = loader.download_lending_club()
    df_sampled = loader.sample_diverse_data(df, n=200)
    loader.save_to_csv(df_sampled)
    df = pd.read_csv('borrowers.csv')
```

---

## 📚 Resources

- **Kaggle API Docs**: https://github.com/Kaggle/kaggle-api
- **Lending Club Dataset**: https://www.kaggle.com/datasets/wordsforthewise/lending-club
- **Your Loader Script**: `load_kaggle_data.py`
- **Dataset Analyzer**: `analyze_dataset.py`

---

## ✅ Success Checklist

After running the loader:
- [ ] `borrowers.csv` has 200+ records
- [ ] FICO scores range 300-850
- [ ] Mix of Low/Medium/High risk borrowers
- [ ] Server starts without errors
- [ ] Test suite passes
- [ ] Demo shows varied risk profiles

---

**🎯 TIP**: For your hackathon, having real Kaggle data adds credibility. Mention: "We're using actual Lending Club data from Kaggle with over 2 million historical loans."**
