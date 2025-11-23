# Credit Risk Automation System - API Documentation

## Overview
A Flask-based microservice that mimics a Credit Bureau's automated decision engine for the IBM Watsonx Orchestrate Hackathon.

## Tech Stack
- **Language**: Python 3.9+
- **Libraries**: Flask, flask_cors, pandas
- **Integration**: OpenAPI 3.0 (Swagger)
- **Orchestration**: IBM Watsonx Orchestrate
- **Tunneling**: Ngrok (for local-to-cloud exposure)

## Architecture
```
┌─────────────────────┐
│ Watsonx Orchestrate │ ← UI/Agent Layer
└──────────┬──────────┘
           │ HTTPS (via Ngrok)
           ▼
┌─────────────────────┐
│   Flask API Server  │ ← Business Logic
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Pandas DataFrame    │ ← Mock Database
│ (borrowers.csv)     │
└─────────────────────┘
```

## Data Schema
The application uses `borrowers.csv` with 100 real loan records:

| Column           | Type  | Description                    |
|------------------|-------|--------------------------------|
| member_id        | int   | Unique User ID                 |
| annual_inc       | float | Annual Income (USD)            |
| fico_range_high  | int   | Credit Score (300-850)         |
| loan_amnt        | float | Requested Loan Amount (USD)    |
| loan_status      | str   | Loan Status (informational)    |

## API Endpoints

### 1. Health Check
**Endpoint**: `GET /health`

**Purpose**: Verify the service is running and data is loaded

**Response**:
```json
{
  "status": "healthy",
  "service": "Credit Risk API",
  "records_loaded": 100
}
```

---

### 2. Get User Data
**Endpoint**: `POST /get_data`

**Purpose**: Retrieve credit data for a specific member

**Request Body**:
```json
{
  "member_id": 68407277
}
```

**Response** (200 OK):
```json
{
  "member_id": 68407277,
  "annual_inc": 55000.0,
  "fico_range_high": 679,
  "loan_amnt": 3600.0,
  "loan_status": "Fully Paid"
}
```

**Error Responses**:
- `400`: Missing or invalid member_id
- `404`: User not found
- `500`: Internal server error

---

### 3. Calculate Risk Score
**Endpoint**: `POST /risk_score`

**Purpose**: Calculate risk score (0-100) based on FICO and income

**Algorithm**:
```
Base Score = 100 - (FICO / 8.5)
If Income > $80,000: Base Score -= 15
Final Score = clamp(Base Score, 0, 100)

Risk Categories:
- Low: 0-30
- Medium: 30-60
- High: 60-100
```

**Request Body**:
```json
{
  "fico_range_high": 679,
  "annual_inc": 55000
}
```

**Response** (200 OK):
```json
{
  "risk_score": 20.12,
  "risk_category": "Low"
}
```

**Error Responses**:
- `400`: Missing required fields or invalid values
- `500`: Internal server error

---

### 4. Calculate Expected Credit Loss (ECL)
**Endpoint**: `POST /calc_ecl`

**Purpose**: Calculate potential monetary loss on a loan

**Formula**:
```
Expected Credit Loss = Loan Amount × (Risk Score / 100)
```

**Request Body**:
```json
{
  "loan_amnt": 3600,
  "risk_score": 20.12
}
```

**Response** (200 OK):
```json
{
  "expected_credit_loss": 724.32,
  "currency": "USD"
}
```

**Error Responses**:
- `400`: Missing required fields, invalid values, or out-of-range risk_score
- `500`: Internal server error

---

## Setup Instructions

### 1. Install Dependencies
```powershell
pip install flask flask-cors pandas
```

### 2. Start the Server
```powershell
python app.py
```

The server will start on `http://0.0.0.0:5000`

### 3. Test Locally
```powershell
# Run the comprehensive test suite
.\test_api.ps1
```

### 4. Expose via Ngrok (for Watsonx)
```powershell
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://xyz.ngrok-free.app`) and update `credit-api.json` in the `servers` section.

---

## Complete Workflow Example

### Scenario: Evaluate member 68407277

**Step 1**: Get user data
```powershell
$body = @{member_id=68407277} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/get_data" -Method POST -Body $body -ContentType "application/json"
```

**Result**:
```json
{
  "member_id": 68407277,
  "annual_inc": 55000.0,
  "fico_range_high": 679,
  "loan_amnt": 3600.0
}
```

---

**Step 2**: Calculate risk score
```powershell
$body = @{fico_range_high=679; annual_inc=55000} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json"
```

**Result**:
```json
{
  "risk_score": 20.12,
  "risk_category": "Low"
}
```

---

**Step 3**: Calculate expected loss
```powershell
$body = @{loan_amnt=3600; risk_score=20.12} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/calc_ecl" -Method POST -Body $body -ContentType "application/json"
```

**Result**:
```json
{
  "expected_credit_loss": 724.32,
  "currency": "USD"
}
```

---

## Features Implemented

✅ **Robust Error Handling**
- Validates all inputs (missing fields, invalid types, out-of-range values)
- Returns appropriate HTTP status codes (400, 404, 500)
- Clear error messages for debugging

✅ **Comprehensive Logging**
- INFO level: Successful operations, calculations
- WARNING level: User not found, out-of-range values
- ERROR level: Missing fields, invalid inputs, exceptions

✅ **CORS Enabled**
- Allows cross-origin requests from Watsonx Orchestrate

✅ **Type Safety**
- Handles pandas/numpy type conversions for JSON serialization
- Validates numeric inputs

✅ **Health Monitoring**
- `/health` endpoint for service verification
- Reports number of loaded records

✅ **Production Ready**
- Clean JSON responses matching OpenAPI spec
- Consistent response format
- Handles edge cases (NaN values, type conversions)

---

## Testing

### Quick Test
```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET
```

### Comprehensive Test Suite
```powershell
.\test_api.ps1
```

This runs 8 tests covering:
1. Health check
2. Valid member lookup
3. Invalid member (404 handling)
4. Risk calculation (standard)
5. Risk calculation (high income adjustment)
6. ECL calculation
7. Missing required fields (400 handling)
8. Complete end-to-end workflow

---

## Watsonx Integration

1. Start the Flask server locally
2. Expose via Ngrok: `ngrok http 5000`
3. Update `credit-api.json` with your Ngrok URL
4. Import the OpenAPI spec into Watsonx Orchestrate
5. Configure skills for each endpoint:
   - `getData` → Step 1
   - `getRisk` → Step 2
   - `getECL` → Step 3

### Example Watsonx Flow
```
User: "Analyze credit risk for member 68407277"

Watsonx:
1. Call getData(member_id=68407277)
2. Extract fico_range_high and annual_inc
3. Call getRisk(fico_range_high, annual_inc)
4. Extract risk_score
5. Call getECL(loan_amnt, risk_score)
6. Present final analysis to user
```

---

## Sample Member IDs for Testing

| Member ID | FICO | Income    | Loan Amount | Notes                  |
|-----------|------|-----------|-------------|------------------------|
| 68407277  | 679  | $55,000   | $3,600      | Low risk, standard     |
| 66310712  | 789  | $110,000  | $35,000     | Very low risk, high $  |
| 67849662  | 729  | $35,000   | $4,225      | Charged off (history)  |
| 68577849  | 804  | $112,000  | $18,000     | Excellent profile      |
| 66624733  | 669  | $150,000  | $18,000     | High income, lower FICO|

---

## Troubleshooting

### Server won't start
- Check if port 5000 is already in use: `Get-NetTCPConnection -LocalPort 5000`
- Verify dependencies: `pip list | Select-String "flask"`

### CSV not loading
- Ensure `borrowers.csv` is in the same directory as `app.py`
- Check file permissions
- The app will fall back to mock data if CSV is missing

### Ngrok issues
- Ensure ngrok is authenticated: `ngrok config add-authtoken <token>`
- Use the HTTPS URL (not HTTP) for Watsonx

### CORS errors
- CORS is enabled by default for all origins
- If issues persist, check browser console for specific errors

---

## Project Structure
```
credit_risk_analysis/
├── app.py              # Main Flask application
├── borrowers.csv       # Mock database (100 records)
├── credit-api.json     # OpenAPI 3.0 specification
├── test_api.ps1        # PowerShell test suite
└── README.md           # This file
```

---

## Next Steps for Production

1. **Database Integration**: Replace DataFrame with PostgreSQL/MongoDB
2. **Authentication**: Add API keys or OAuth
3. **Rate Limiting**: Prevent abuse
4. **Caching**: Redis for frequently accessed data
5. **Monitoring**: Prometheus + Grafana
6. **Deployment**: Docker + Kubernetes or AWS Lambda
7. **Enhanced Risk Model**: Machine learning integration

---

## License
MIT License - Hackathon Project

## Contact
For questions about this Hackathon project, contact your team lead.
