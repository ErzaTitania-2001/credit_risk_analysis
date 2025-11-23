# Quick Start Guide - Credit Risk API

## Prerequisites
- Python 3.9+
- pip installed
- PowerShell (Windows)

## 1. Install Dependencies
```powershell
pip install flask flask-cors pandas
```

## 2. Start the Server
```powershell
cd C:\Users\puppy\credit_risk_analysis
python app.py
```

You should see:
```
==================================================
CREDIT RISK API SERVER STARTING
==================================================
Loaded 100 borrower records
Endpoints available:
  GET  /health      - Health check
  POST /get_data    - Retrieve user data
  POST /risk_score  - Calculate risk score
  POST /calc_ecl    - Calculate expected credit loss
==================================================
 * Running on http://127.0.0.1:5000
```

## 3. Test the API
Open a new PowerShell terminal and run:
```powershell
.\test_api.ps1
```

This runs all 8 test cases and verifies everything works.

## 4. Expose via Ngrok (for Watsonx)
```powershell
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.app`)

## 5. Update OpenAPI Spec
Edit `credit-api.json` and update the `servers` section:
```json
"servers": [
  {
    "url": "https://your-ngrok-url-here.ngrok-free.dev"
  }
]
```

## 6. Import to Watsonx Orchestrate
1. Log into IBM Watsonx Orchestrate
2. Go to Skills > Import Skills
3. Upload `credit-api.json`
4. The three endpoints will be available as skills:
   - `getData` - Get User Info
   - `getRisk` - Calculate Risk
   - `getECL` - Calculate Loss

## Manual Testing Examples

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET
```

### Get User Data
```powershell
$body = @{member_id=68407277} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/get_data" -Method POST -Body $body -ContentType "application/json"
```

### Calculate Risk
```powershell
$body = @{fico_range_high=679; annual_inc=55000} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json"
```

### Calculate ECL
```powershell
$body = @{loan_amnt=10000; risk_score=20.12} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/calc_ecl" -Method POST -Body $body -ContentType "application/json"
```

## Troubleshooting

### Port 5000 already in use
```powershell
# Find process using port 5000
Get-NetTCPConnection -LocalPort 5000
# Kill the process
Stop-Process -Id <PID>
```

### Can't connect to server
- Check if server is running: Look for "Running on http://127.0.0.1:5000"
- Check firewall settings
- Try `http://localhost:5000/health` in your browser

### CSV not loading
The app will automatically fall back to mock data if `borrowers.csv` is missing or corrupted.

## Sample Member IDs

| Member ID | Description                        |
|-----------|------------------------------------|
| 68407277  | Standard borrower (Low risk)       |
| 66310712  | Excellent profile (Very low risk)  |
| 68577849  | High FICO, high income             |
| 67849662  | Charged off loan (history)         |

## Watsonx Demo Flow

1. User asks: "Analyze credit risk for member 68407277"
2. Watsonx calls `getData(68407277)`
3. Extracts FICO and income
4. Calls `getRisk(fico, income)`
5. Extracts risk_score
6. Calls `getECL(loan_amnt, risk_score)`
7. Presents comprehensive analysis to user

## Next Steps
- See `README.md` for comprehensive documentation
- See `app.py` for implementation details
- See `credit-api.json` for OpenAPI specification
