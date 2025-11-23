# 🧪 Failure Test Cases for Watsonx AI Agent

## **Test the AI Agent's Error Handling**

These prompts are designed to test edge cases, invalid inputs, and error handling capabilities of your credit risk system.

---

## ❌ **CATEGORY 1: Invalid Member IDs**

### **Test 1.1: Non-existent Member**
```
Analyze credit risk for member 999999999
```
**Expected Behavior:**
- ✅ API returns 200 with: `{"found": false, "message": "User not found"}`
- ✅ Watsonx should gracefully respond: "Member 999999999 not found in database"

---

### **Test 1.2: Invalid Member ID Format**
```
Get data for member ABC123
```
**Expected Behavior:**
- ❌ API returns 400: Invalid input
- ✅ Watsonx should handle: "Invalid member ID format. Must be numeric."

---

### **Test 1.3: Zero Member ID**
```
Analyze credit risk for member 0
```
**Expected Behavior:**
- ❌ API returns 404: "User not found"
- ✅ Should handle gracefully

---

## ❌ **CATEGORY 2: Invalid FICO Scores**

### **Test 2.1: FICO Score Too Low**
```
Calculate credit risk for FICO score 200 and income $50,000
```
**Expected Behavior:**
- ❌ API returns 400: "FICO score must be between 300 and 850"
- ✅ Watsonx should explain: "Invalid FICO score. Valid range is 300-850."

---

### **Test 2.2: FICO Score Too High**
```
What's the risk for someone with FICO 900 and income $100,000?
```
**Expected Behavior:**
- ❌ API returns 400: "FICO score must be between 300 and 850"
- ✅ Should handle validation error

---

### **Test 2.3: Negative FICO Score**
```
Calculate risk for FICO -500 and income $40,000
```
**Expected Behavior:**
- ❌ API returns 400: Invalid FICO
- ✅ Should reject negative values

---

### **Test 2.4: Non-numeric FICO**
```
Assess credit risk for FICO score "excellent" and income $60,000
```
**Expected Behavior:**
- ❌ Watsonx may fail to parse or send invalid request
- ✅ Should explain: "FICO must be a numeric value between 300-850"

---

## ❌ **CATEGORY 3: Invalid Income Values**

### **Test 3.1: Negative Income**
```
Calculate credit risk for FICO 700 and annual income -$50,000
```
**Expected Behavior:**
- ❌ API returns 400: "Income must be positive"
- ✅ Should reject negative income

---

### **Test 3.2: Zero Income**
```
What's the risk for FICO 650 and income $0?
```
**Expected Behavior:**
- ⚠️ API may accept (edge case for unemployed/retired)
- Risk score will be very high
- ✅ Should flag as unusual: "Zero income detected, high risk"

---

### **Test 3.3: Unrealistic Income**
```
Calculate risk for FICO 600 and income $10,000,000,000
```
**Expected Behavior:**
- ⚠️ API may accept but produce low risk score
- ✅ Should process but may note it's unusual

---

## ❌ **CATEGORY 4: Invalid Loan Amounts**

### **Test 4.1: Negative Loan Amount**
```
Calculate ECL for a -$10,000 loan with risk score 30
```
**Expected Behavior:**
- ❌ API returns 400: "Loan amount must be positive"
- ✅ Should reject negative loans

---

### **Test 4.2: Zero Loan Amount**
```
What's the expected credit loss for a $0 loan with risk score 50?
```
**Expected Behavior:**
- ✅ API returns ECL: $0 (technically valid)
- Should process: "ECL is $0 for a $0 loan"

---

### **Test 4.3: Extremely Large Loan**
```
Calculate ECL for a $1,000,000,000 loan with risk score 60
```
**Expected Behavior:**
- ✅ API processes: ECL = $600,000,000
- Should return massive loss amount

---

## ❌ **CATEGORY 5: Invalid Risk Scores**

### **Test 5.1: Risk Score > 100**
```
Calculate expected credit loss for a $15,000 loan with risk score 150
```
**Expected Behavior:**
- ❌ API returns 400: "Risk score must be between 0 and 100"
- ✅ Should reject invalid risk score

---

### **Test 5.2: Negative Risk Score**
```
What's the ECL for a $20,000 loan with risk score -25?
```
**Expected Behavior:**
- ❌ API returns 400: Invalid risk score
- ✅ Should reject negative risk

---

## ❌ **CATEGORY 6: Missing Required Parameters**

### **Test 6.1: Missing FICO Score**
```
Calculate credit risk for annual income $50,000
```
**Expected Behavior:**
- ❌ API returns 400: "Missing required parameter: fico_range_high"
- ✅ Watsonx should prompt: "Please provide FICO score"

---

### **Test 6.2: Missing Income**
```
Calculate risk for FICO score 700
```
**Expected Behavior:**
- ❌ API returns 400: "Missing required parameter: annual_inc"
- ✅ Should request missing income

---

### **Test 6.3: Missing Both Parameters**
```
Calculate credit risk for a borrower
```
**Expected Behavior:**
- ❌ Watsonx may not know what to do
- ✅ Should ask: "Please provide FICO score and annual income"

---

## ❌ **CATEGORY 7: Ambiguous Prompts**

### **Test 7.1: Vague Request**
```
Tell me about credit
```
**Expected Behavior:**
- ❌ Watsonx says "beyond my capacity"
- No specific action to take

---

### **Test 7.2: Multiple Conflicting Values**
```
Calculate risk for FICO 600, no wait 700, and income $50,000 or maybe $60,000
```
**Expected Behavior:**
- ⚠️ Watsonx may pick one value or get confused
- May need clarification

---

### **Test 7.3: Wrong Terminology**
```
What's the danger level for someone with credit score 650?
```
**Expected Behavior:**
- ⚠️ May not recognize "danger level" or "credit score" (vs FICO)
- Watsonx might still work if it interprets correctly

---

## ❌ **CATEGORY 8: Wrong Endpoint Combinations**

### **Test 8.1: ECL Without Prior Risk Calculation**
```
Calculate expected credit loss for member 63044350
```
**Expected Behavior:**
- ⚠️ Needs both loan amount AND risk score
- Watsonx should call getData, then calculate risk, then ECL
- May work if it chains properly

---

### **Test 8.2: Risk Without Income**
```
What's the risk for member 12345?
```
**Expected Behavior:**
- ❌ If member doesn't exist, fails
- ✅ If member exists, should retrieve data and calculate

---

## ❌ **CATEGORY 9: Boundary Values**

### **Test 9.1: Minimum Valid FICO**
```
Calculate risk for FICO 300 and income $1
```
**Expected Behavior:**
- ✅ Should process (both at minimum)
- Risk score: 64.71 (High)
- Extreme risk scenario

---

### **Test 9.2: Maximum Valid FICO**
```
Calculate risk for FICO 850 and income $1
```
**Expected Behavior:**
- ✅ Should process
- Low risk score despite low income
- Unusual combination

---

### **Test 9.3: Risk Score Exactly 30 (Boundary)**
```
Calculate ECL for $10,000 loan with risk score 30
```
**Expected Behavior:**
- ✅ ECL = $3,000
- Boundary between Low and Medium risk

---

### **Test 9.4: Risk Score Exactly 60 (Boundary)**
```
Calculate ECL for $10,000 loan with risk score 60
```
**Expected Behavior:**
- ✅ ECL = $6,000
- Boundary between Medium and High risk

---

## ❌ **CATEGORY 10: Type Mismatches**

### **Test 10.1: String Instead of Number**
```
Calculate risk for FICO "seven hundred" and income "fifty thousand dollars"
```
**Expected Behavior:**
- ❌ Watsonx may fail to parse
- API would reject if strings are sent

---

### **Test 10.2: Boolean Values**
```
Get data for member true
```
**Expected Behavior:**
- ❌ Invalid member ID type
- Should fail

---

## ❌ **CATEGORY 11: Special Characters**

### **Test 11.1: SQL Injection Attempt**
```
Analyze credit risk for member 1 OR 1=1
```
**Expected Behavior:**
- ✅ Should be safe (pandas DataFrame lookup, not SQL)
- May fail to find member or interpret as string

---

### **Test 11.2: Script Injection**
```
Calculate risk for FICO <script>alert('xss')</script> and income $50000
```
**Expected Behavior:**
- ✅ Should be safe (Flask/pandas sanitize)
- Will fail validation

---

## ❌ **CATEGORY 12: System Limitations**

### **Test 12.1: Server Down**
*Stop the Flask server, then try:*
```
Analyze credit risk for member 63044350
```
**Expected Behavior:**
- ❌ Connection error
- Watsonx should report: "Unable to connect to API"

---

### **Test 12.2: Wrong URL in OpenAPI Spec**
*Use expired ngrok URL:*
```
Calculate risk for FICO 700 and income $60,000
```
**Expected Behavior:**
- ❌ Connection timeout
- Should fail gracefully

---

## 🧪 **PowerShell Test Script for API Validation**

Run these direct API tests to verify error handling:

```powershell
# Test 1: Non-existent member
Write-Host "`n1. Non-existent member:" -ForegroundColor Yellow
$body = @{member_id=999999999} | ConvertTo-Json
try { Invoke-RestMethod -Uri "http://localhost:5000/get_data" -Method POST -Body $body -ContentType "application/json" } catch { Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red }

# Test 2: Invalid FICO (too low)
Write-Host "`n2. FICO too low (200):" -ForegroundColor Yellow
$body = @{fico_range_high=200; annual_inc=50000} | ConvertTo-Json
try { Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json" } catch { Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red }

# Test 3: Invalid FICO (too high)
Write-Host "`n3. FICO too high (900):" -ForegroundColor Yellow
$body = @{fico_range_high=900; annual_inc=50000} | ConvertTo-Json
try { Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json" } catch { Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red }

# Test 4: Negative income
Write-Host "`n4. Negative income:" -ForegroundColor Yellow
$body = @{fico_range_high=700; annual_inc=-50000} | ConvertTo-Json
try { Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json" } catch { Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red }

# Test 5: Invalid risk score
Write-Host "`n5. Risk score > 100:" -ForegroundColor Yellow
$body = @{loan_amnt=15000; risk_score=150} | ConvertTo-Json
try { Invoke-RestMethod -Uri "http://localhost:5000/calc_ecl" -Method POST -Body $body -ContentType "application/json" } catch { Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red }

# Test 6: Missing parameters
Write-Host "`n6. Missing FICO parameter:" -ForegroundColor Yellow
$body = @{annual_inc=50000} | ConvertTo-Json
try { Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json" } catch { Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red }

# Test 7: Boundary - FICO 300 (minimum)
Write-Host "`n7. Minimum FICO (300):" -ForegroundColor Yellow
$body = @{fico_range_high=300; annual_inc=1} | ConvertTo-Json
try { Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json" | Format-List } catch { Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red }

# Test 8: Boundary - FICO 850 (maximum)
Write-Host "`n8. Maximum FICO (850):" -ForegroundColor Yellow
$body = @{fico_range_high=850; annual_inc=1} | ConvertTo-Json
try { Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json" | Format-List } catch { Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red }
```

---

## 📊 **Expected Failure Summary**

| Test Category | Should Fail | Should Handle Gracefully |
|--------------|-------------|--------------------------|
| Non-existent Member | ✅ 404 | ✅ "Member not found" |
| Invalid FICO (<300 or >850) | ✅ 400 | ✅ Validation message |
| Negative Income | ✅ 400 | ✅ "Income must be positive" |
| Invalid Risk Score | ✅ 400 | ✅ "Risk must be 0-100" |
| Missing Parameters | ✅ 400 | ✅ "Missing required field" |
| Vague Prompts | ⚠️ Confusion | ⚠️ May say "beyond capacity" |
| Server Down | ✅ Connection Error | ✅ Connection message |

---

## 💡 **How to Demonstrate Robust Error Handling**

During your demo, briefly mention:

> "The system includes comprehensive error handling. For example, if someone tries to use an invalid FICO score like 900, the API returns a clear validation error. If a member doesn't exist, it gracefully handles the 404 error rather than crashing."

**This shows your system is production-ready, not just a happy-path demo! 🛡️**
