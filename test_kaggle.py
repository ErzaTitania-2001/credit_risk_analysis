# Quick Kaggle Test Script
import os
import sys

print("="*50)
print("KAGGLE API TEST")
print("="*50)

# Check kaggle.json
kaggle_json = os.path.expanduser("~/.kaggle/kaggle.json")
if os.path.exists(kaggle_json):
    print(f"✓ Found kaggle.json at: {kaggle_json}")
    
    import json
    with open(kaggle_json) as f:
        config = json.load(f)
        print(f"  Username: {config.get('username')}")
        if config.get('username') == 'YOUR_KAGGLE_USERNAME':
            print("\n⚠ ERROR: You need to update your username in kaggle.json!")
            print("\nSteps:")
            print("1. Go to https://www.kaggle.com/account")
            print("2. Find your username (top of page)")
            print(f"3. Edit: {kaggle_json}")
            print("4. Replace YOUR_KAGGLE_USERNAME with your actual username")
            sys.exit(1)
else:
    print(f"✗ kaggle.json not found at: {kaggle_json}")
    sys.exit(1)

# Test Kaggle API
print("\nTesting Kaggle API...")
try:
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    print("✓ Kaggle API authenticated successfully!")
    
    print("\nFetching first 3 datasets...")
    datasets = api.dataset_list(page=1, max_size=100)[:3]
    for ds in datasets:
        print(f"  - {ds.ref}")
    
    print("\n" + "="*50)
    print("SUCCESS! Kaggle API is working!")
    print("="*50)
    print("\nYou can now run:")
    print("  python load_kaggle_data.py")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nMake sure:")
    print("1. Your username is correct in kaggle.json")
    print("2. Your API key is valid")
    print("3. You have internet connection")
