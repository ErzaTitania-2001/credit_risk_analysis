# Expected Watsonx Orchestrate Outputs

## 📋 **What to Expect from Each Prompt**

---

## 🎯 **SCENARIO 1: Member-Based Analysis (Low Risk)**

### **Your Prompt:**
```
Analyze credit risk for member 63044350
```

### **Expected Watsonx Response:**
```
Let me analyze the credit risk for member 63044350.

Step 1: Retrieved borrower data
- Member ID: 63044350
- FICO Score: 779
- Annual Income: $96,000
- Loan Amount: $15,000
- Loan Status: Current

Step 2: Calculated risk score
- Risk Score: 0.00
- Risk Category: Low

Step 3: Expected Credit Loss
- Expected Credit Loss: $0.00
- Loan Amount: $15,000
- Risk Score: 0.0

Summary: This borrower has excellent credit (FICO 779) with strong income 
($96,000). The risk is minimal (0.00), categorized as Low risk. The expected 
credit loss is $0, making this an ideal loan candidate.
```

### **API Calls Made by Watsonx:**
1. **POST /get_data** → `{"member_id": 63044350}`
2. **POST /risk_score** → `{"fico_range_high": 779, "annual_inc": 96000}`
3. **POST /calc_ecl** → `{"loan_amnt": 15000, "risk_score": 0.0}`

---

## 🎯 **SCENARIO 2: Member-Based Analysis (High Risk)**

### **Your Prompt:**
```
Evaluate loan application for member -76653
```

### **Expected Watsonx Response:**
```
Let me evaluate the loan application for member -76653.

Step 1: Retrieved borrower data
- Member ID: -76653
- FICO Score: 300
- Annual Income: $69,558
- Loan Amount: $17,000
- Loan Status: Declined

Step 2: Calculated risk score
- Risk Score: 64.71
- Risk Category: High

Step 3: Expected Credit Loss
- Expected Credit Loss: $11,000.70
- Loan Amount: $17,000
- Risk Score: 64.71

Summary: This borrower has very poor credit (FICO 300) despite moderate income 
($69,558). The risk score is 64.71, categorized as High risk. The expected 
credit loss is $11,000.70 on a $17,000 loan, representing a 64.7% loss rate. 
This application was previously declined.
```

### **API Calls Made by Watsonx:**
1. **POST /get_data** → `{"member_id": -76653}`
2. **POST /risk_score** → `{"fico_range_high": 300, "annual_inc": 69558}`
3. **POST /calc_ecl** → `{"loan_amnt": 17000, "risk_score": 64.71}`

---

## 🎯 **SCENARIO 3: Direct Calculation (Medium Risk)**

### **Your Prompt:**
```
Calculate credit risk for a borrower with FICO score 600 and annual income $45,000
```

### **Expected Watsonx Response:**
```
Let me calculate the credit risk for those parameters.

Risk Assessment:
- FICO Score: 600
- Annual Income: $45,000
- Risk Score: 29.41
- Risk Category: Low (borderline Medium)

Analysis: With a FICO score of 600 and income of $45,000, this borrower 
presents moderate risk. The calculated risk score is 29.41, which falls in 
the Low category but is close to the Medium threshold (30). This borrower 
would require careful underwriting.
```

### **API Calls Made by Watsonx:**
1. **POST /risk_score** → `{"fico_range_high": 600, "annual_inc": 45000}`

### **Actual API Response:**
```json
{
  "fico_range_high": 600.0,
  "annual_inc": 45000.0,
  "risk_score": 29.41,
  "risk_category": "Low"
}
```

---

## 🎯 **SCENARIO 4: Complete Custom Assessment**

### **Your Prompt:**
```
I need a complete risk assessment: FICO is 650, income is $55,000, and loan amount is $15,000
```

### **Expected Watsonx Response:**
```
Let me provide a complete risk assessment for those parameters.

Step 1: Calculate Risk Score
- FICO Score: 650
- Annual Income: $55,000
- Risk Score: 23.53
- Risk Category: Low

Step 2: Calculate Expected Credit Loss
- Loan Amount: $15,000
- Risk Score: 23.53
- Expected Credit Loss: $3,529.50

Complete Assessment:
This borrower with FICO 650 and income $55,000 presents Low risk (score 23.53). 
For a $15,000 loan, the expected credit loss would be $3,529.50, representing 
a 23.5% potential loss rate. This is within acceptable risk parameters for 
standard lending practices.
```

### **API Calls Made by Watsonx:**
1. **POST /risk_score** → `{"fico_range_high": 650, "annual_inc": 55000}`
2. **POST /calc_ecl** → `{"loan_amnt": 15000, "risk_score": 23.53}`

### **Actual API Responses:**
**Risk Calculation:**
```json
{
  "fico_range_high": 650.0,
  "annual_inc": 55000.0,
  "risk_score": 23.53,
  "risk_category": "Low"
}
```

**ECL Calculation:**
```json
{
  "loan_amnt": 15000.0,
  "risk_score": 23.53,
  "expected_credit_loss": 3529.5
}
```

---

## 🎯 **SCENARIO 5: Direct ECL Calculation**

### **Your Prompt:**
```
Calculate expected credit loss for a $20,000 loan with risk score 35
```

### **Expected Watsonx Response:**
```
Let me calculate the expected credit loss.

Expected Credit Loss Calculation:
- Loan Amount: $20,000
- Risk Score: 35
- Expected Credit Loss: $7,000.00

Analysis: For a $20,000 loan with a risk score of 35 (Medium risk category), 
the expected credit loss is $7,000, representing a 35% loss rate. This would 
require appropriate pricing and risk management strategies.
```

### **API Calls Made by Watsonx:**
1. **POST /calc_ecl** → `{"loan_amnt": 20000, "risk_score": 35}`

### **Actual API Response:**
```json
{
  "loan_amnt": 20000.0,
  "risk_score": 35.0,
  "expected_credit_loss": 7000.0
}
```

---

## 🎯 **SCENARIO 6: High Risk Direct Calculation**

### **Your Prompt:**
```
What's the risk for someone with FICO 500 and income $30,000?
```

### **Expected Watsonx Response:**
```
Let me assess the risk for those credit parameters.

Risk Assessment:
- FICO Score: 500
- Annual Income: $30,000
- Risk Score: 50.00
- Risk Category: Medium

Analysis: A FICO score of 500 combined with $30,000 annual income results in 
a risk score of 50.00, placing this borrower in the Medium risk category. 
This profile would require enhanced underwriting, potentially higher interest 
rates, or additional collateral requirements.
```

### **API Calls Made by Watsonx:**
1. **POST /risk_score** → `{"fico_range_high": 500, "annual_inc": 30000}`

### **Actual API Response:**
```json
{
  "fico_range_high": 500.0,
  "annual_inc": 30000.0,
  "risk_score": 50.0,
  "risk_category": "Medium"
}
```

---

## 🎯 **SCENARIO 7: Excellent Credit Profile**

### **Your Prompt:**
```
Calculate credit risk for a borrower with FICO score 750 and annual income $80,000
```

### **Expected Watsonx Response:**
```
Let me calculate the credit risk for those parameters.

Risk Assessment:
- FICO Score: 750
- Annual Income: $80,000
- Risk Score: 8.82
- Risk Category: Low

Analysis: This is an excellent credit profile. With a FICO score of 750 and 
income of $80,000, the risk score is just 8.82, well within the Low risk 
category. This borrower qualifies for premium lending rates and favorable terms.
```

### **API Calls Made by Watsonx:**
1. **POST /risk_score** → `{"fico_range_high": 750, "annual_inc": 80000}`

---

## 📊 **Risk Score Interpretation Guide**

Watsonx should interpret results as follows:

| Risk Score | Category | Interpretation |
|-----------|----------|----------------|
| 0 - 29 | **Low** | Excellent to good credit, minimal default risk |
| 30 - 59 | **Medium** | Fair credit, moderate risk, requires careful review |
| 60 - 100 | **High** | Poor credit, significant risk, may decline |

---

## 🔢 **Quick Reference: Sample Test Values**

### **Low Risk Examples:**
- FICO 750, Income $80,000 → Risk Score: ~8.82 (Low)
- FICO 700, Income $70,000 → Risk Score: ~14.71 (Low)
- FICO 779, Income $96,000 → Risk Score: 0.00 (Low)

### **Medium Risk Examples:**
- FICO 650, Income $55,000 → Risk Score: 23.53 (Low, near Medium)
- FICO 600, Income $45,000 → Risk Score: 29.41 (Low, borderline Medium)
- FICO 550, Income $35,000 → Risk Score: ~41.18 (Medium)

### **High Risk Examples:**
- FICO 500, Income $30,000 → Risk Score: 50.00 (Medium)
- FICO 400, Income $25,000 → Risk Score: ~73.53 (High)
- FICO 300, Income $69,558 → Risk Score: 64.71 (High)

---

## 💡 **What Makes Watsonx Smart?**

Watsonx should demonstrate:

1. **Skill Chaining**: Automatically calling multiple APIs in sequence
2. **Context Understanding**: Recognizing when to use member lookup vs direct calculation
3. **Natural Language**: Understanding conversational prompts
4. **Summarization**: Providing business-friendly interpretations
5. **Data Extraction**: Pulling relevant values from API responses

---

## 🚨 **If Watsonx Says "Beyond My Capacity"**

### **Problem:** Prompt too vague
**Solution:** Be more specific with numbers
```
❌ "What's the risk for a borrower?"
✅ "Calculate credit risk for FICO 600 and income $45,000"
```

### **Problem:** Missing skill keywords
**Solution:** Use action verbs
```
❌ "Tell me about member 63044350"
✅ "Analyze credit risk for member 63044350"
```

### **Problem:** Skills not linked properly
**Solution:** Reference the skill explicitly
```
❌ "Check this person's creditworthiness"
✅ "Use step_2_calculate_risk for FICO 650 and income $55,000"
```

---

## ✅ **Success Indicators**

Your demo is working correctly when:

✅ Watsonx recognizes member IDs and calls getData
✅ Direct FICO/income prompts work without member lookup
✅ Multiple skills chain together automatically
✅ Results include risk scores, categories, and ECL values
✅ Watsonx provides natural language summaries

---

## 🎬 **Recommended Demo Script**

### **Opening (30 seconds)**
"Let me demonstrate our AI-powered credit risk automation system..."

### **Demo 1: Full Automation (45 seconds)**
```
Prompt: "Analyze credit risk for member 63044350"
Show: Full workflow from data retrieval → risk → ECL
```

### **Demo 2: Flexibility (30 seconds)**
```
Prompt: "Calculate credit risk for FICO 600 and income $45,000"
Show: Direct calculation without database lookup
```

### **Demo 3: High Risk Detection (30 seconds)**
```
Prompt: "Evaluate loan application for member -76653"
Show: System identifying high-risk borrower
```

### **Demo 4: Custom Scenario (45 seconds)**
```
Prompt: "Complete assessment: FICO 650, income $55,000, loan $15,000"
Show: Multi-step orchestration with business insights
```

### **Closing (30 seconds)**
"As you can see, IBM Watsonx Orchestrate intelligently chains our credit risk 
APIs to provide comprehensive loan assessments, whether working from existing 
member data or ad-hoc credit parameters."

**Total Time: 3 minutes**

---

## 📝 **Notes for Judges**

**Highlight these points:**
- Real Kaggle Lending Club data (2M+ records)
- 200-record dataset with diverse risk profiles (70% Low, 20% Medium, 10% High)
- FICO scores from 300-850 (full credit spectrum)
- Automated skill chaining reduces manual work
- Both database-driven and on-demand calculations supported
- Natural language interface makes it accessible to non-technical users

**Your API is production-ready! 🚀**
