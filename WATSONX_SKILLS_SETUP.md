# Watsonx Orchestrate Skills Setup Guide

## Overview
This guide explains how to configure skills in IBM Watsonx Orchestrate to support **both** workflows:
1. **Member-based workflow**: Lookup borrower by ID → Calculate risk → Calculate ECL
2. **Direct calculation**: Provide FICO + Income directly → Calculate risk → Calculate ECL

## Updated OpenAPI Specification

The `credit-api.json` file has been enhanced with:
- ✅ Better descriptions for each operation
- ✅ Required fields marked clearly
- ✅ Example values for all parameters
- ✅ Clear min/max ranges for FICO (300-850) and risk scores (0-100)
- ✅ Renamed `getRisk` to `calculateRisk` for clarity

## Skills Configuration in Watsonx

### Option 1: Import Updated OpenAPI (Recommended)

1. **Update your Ngrok URL** in `credit-api.json` if needed
2. **Re-import** the updated OpenAPI spec into Watsonx Orchestrate
3. Watsonx will now understand **3 independent skills**:
   - `getData` - For member lookup
   - `calculateRisk` - For direct FICO/income input
   - `calculateECL` - For loss calculation

### Option 2: Create Separate Skills

If you want more control, create these as separate skills:

#### Skill 1: "Get Borrower Data"
- **Operation**: `getData`
- **Trigger phrases**: "look up member", "get borrower data", "find member"
- **Input**: member_id (integer)
- **Output**: fico_range_high, annual_inc, loan_amnt, loan_status

#### Skill 2: "Calculate Credit Risk"
- **Operation**: `calculateRisk`
- **Trigger phrases**: "calculate risk", "assess credit", "what's the risk for FICO X and income Y"
- **Input**: fico_range_high (300-850), annual_inc (USD)
- **Output**: risk_score (0-100), risk_category (Low/Medium/High)

#### Skill 3: "Calculate Expected Credit Loss"
- **Operation**: `calculateECL`
- **Trigger phrases**: "calculate loss", "expected credit loss", "ECL for loan"
- **Input**: loan_amnt (USD), risk_score (0-100)
- **Output**: expected_credit_loss (USD)

## Prompt Examples for Both Workflows

### 🔹 Member-Based Workflow (Chain of 3 skills)
```
"Analyze credit risk for member 63044350"
→ Watsonx calls: getData → calculateRisk → calculateECL

"Evaluate loan application for member -76653"
→ Watsonx calls: getData → calculateRisk → calculateECL

"Complete risk assessment for borrower 63044350"
→ Watsonx calls: getData → calculateRisk → calculateECL
```

### 🔹 Direct Calculation Workflow (Start with calculateRisk)
```
"Calculate risk for FICO score 600 and annual income $45,000"
→ Watsonx calls: calculateRisk (directly)
→ Returns: {"risk_score": 45.5, "risk_category": "Medium"}

"What's the credit risk for someone with FICO 720 and income $80,000?"
→ Watsonx calls: calculateRisk
→ Returns: {"risk_score": 22.8, "risk_category": "Low"}

"Assess risk: FICO 350, income $25,000"
→ Watsonx calls: calculateRisk
→ Returns: {"risk_score": 78.2, "risk_category": "High"}
```

### 🔹 Complete Direct Workflow (Manual chaining)
```
"Calculate risk for FICO 600 and income $45,000, then calculate ECL for a $10,000 loan"
→ Watsonx calls: calculateRisk → calculateECL
→ First returns: {"risk_score": 45.5, "risk_category": "Medium"}
→ Then returns: {"expected_credit_loss": 4550.0}
```

## Risk Calculation Formula

**Risk Score** = `100 - (fico_range_high / 10) + (50000 / (annual_inc + 1))`

**Risk Categories**:
- **Low**: risk_score < 30 (Good FICO, Stable income)
- **Medium**: 30 ≤ risk_score ≤ 60 (Average FICO, Moderate income)
- **High**: risk_score > 60 (Poor FICO, Low income)

**Expected Credit Loss (ECL)** = `loan_amnt × (risk_score / 100)`

## Test Scenarios

### Scenario 1: Low Risk Borrower
```
FICO: 780, Income: $95,000
Risk Score: ~22.5 → Low Risk
Loan: $15,000 → ECL: ~$3,375
```

**Prompts**:
- Member-based: `"Analyze member 63044350"`
- Direct: `"Calculate risk for FICO 780 and income $95,000"`

### Scenario 2: Medium Risk Borrower
```
FICO: 600, Income: $45,000
Risk Score: ~45.5 → Medium Risk
Loan: $10,000 → ECL: ~$4,550
```

**Prompts**:
- Direct: `"What's the risk for FICO 600 and income $45,000?"`
- With loan: `"Risk for FICO 600, income $45k, loan $10k"`

### Scenario 3: High Risk Borrower
```
FICO: 300, Income: $25,000
Risk Score: ~72.0 → High Risk
Loan: $5,000 → ECL: ~$3,600
```

**Prompts**:
- Member-based: `"Evaluate member -76653"`
- Direct: `"Calculate risk for FICO 300 and income $25,000"`

## Watsonx Orchestrate Configuration Tips

### 1. **Enable Skill Chaining**
Configure Watsonx to automatically chain skills when outputs match inputs:
- `getData` output (fico, income) → `calculateRisk` input
- `calculateRisk` output (risk_score) + user context (loan_amnt) → `calculateECL` input

### 2. **Natural Language Understanding**
Train Watsonx to recognize these patterns:
- "FICO X and income Y" → Extract X as fico_range_high, Y as annual_inc
- "member N" / "borrower N" → Extract N as member_id
- "loan of $X" / "$X loan" → Extract X as loan_amnt

### 3. **Contextual Memory**
Enable Watsonx to remember values across conversation:
```
User: "Calculate risk for FICO 650 and income $55,000"
Watsonx: [Returns risk_score: 38.2, Medium Risk]
User: "Now calculate ECL for a $12,000 loan"
Watsonx: [Uses stored risk_score 38.2] → ECL: $4,584
```

### 4. **Error Handling**
Configure fallback responses:
- Invalid FICO (not 300-850): "FICO score must be between 300 and 850"
- Missing member_id: "Please provide a member ID or FICO/income values"
- Invalid loan amount: "Loan amount must be greater than 0"

## API Testing Before Watsonx Import

Test each endpoint locally before importing to Watsonx:

```powershell
# Test direct risk calculation
$body = @{fico_range_high=600; annual_inc=45000} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json"

# Test member lookup
$body = @{member_id=63044350} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/get_data" -Method POST -Body $body -ContentType "application/json"

# Test ECL calculation
$body = @{loan_amnt=10000; risk_score=45.5} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/calc_ecl" -Method POST -Body $body -ContentType "application/json"
```

## Deployment Checklist

- [ ] Flask server running on localhost:5000
- [ ] Ngrok tunnel active and URL updated in `credit-api.json`
- [ ] `borrowers.csv` loaded (200 records)
- [ ] All API endpoints tested locally
- [ ] OpenAPI spec imported to Watsonx Orchestrate
- [ ] Skills configured with proper trigger phrases
- [ ] Skill chaining enabled (getData → calculateRisk → calculateECL)
- [ ] Direct calculation skill tested (calculateRisk standalone)
- [ ] Natural language prompts tested in Watsonx
- [ ] Demo scenarios prepared

## Troubleshooting

### Issue: "This question beyond my capacity"
**Solution**: Watsonx needs clearer trigger phrases. Try:
- Instead of: "What's the risk assessment for..."
- Use: "Calculate risk for FICO 600 and income $45,000"

### Issue: Skills not chaining automatically
**Solution**: Check skill dependencies in Watsonx configuration:
1. Open skill settings
2. Enable "Auto-chain with related skills"
3. Map output parameters to input parameters

### Issue: FICO/Income extraction not working
**Solution**: Add explicit parameter names in prompts:
- "Calculate risk for **FICO score** 600 and **annual income** $45,000"

## Next Steps

1. **Import** the updated `credit-api.json` into Watsonx Orchestrate
2. **Configure** skills with the trigger phrases from this guide
3. **Test** both member-based and direct calculation workflows
4. **Refine** natural language understanding based on test results
5. **Prepare** demo with diverse scenarios (low/medium/high risk)

---

**For Hackathon Demo**: Show both workflows to demonstrate flexibility:
1. Start with member lookup: "Analyze member 63044350" (automated chain)
2. Then direct calculation: "Calculate risk for FICO 600 and income $45,000" (flexible input)
3. Highlight the versatility of the system!
