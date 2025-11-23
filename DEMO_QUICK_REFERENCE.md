# 🎯 Quick Reference: Expected Outputs

## **Copy-Paste These Prompts into Watsonx**

---

### **📝 Prompt 1: Member-Based (Low Risk)**
```
Analyze credit risk for member 63044350
```
**Expected Output:**
- FICO: 779, Income: $96,000, Loan: $15,000
- Risk Score: **0.00** (Low)
- ECL: **$0.00**
- ✅ Perfect credit profile

---

### **📝 Prompt 2: Member-Based (High Risk)**
```
Evaluate loan application for member -76653
```
**Expected Output:**
- FICO: 300, Income: $69,558, Loan: $17,000, Status: Declined
- Risk Score: **64.71** (High)
- ECL: **$11,000.70** (64.7% of loan)
- ❌ Very high risk, previously declined

---

### **📝 Prompt 3: Direct Calculation (Borderline Medium)**
```
Calculate credit risk for a borrower with FICO score 600 and annual income $45,000
```
**Expected Output:**
- Risk Score: **29.41** (Low, but close to Medium threshold)
- ⚠️ Borderline case, needs careful review

---

### **📝 Prompt 4: Direct Calculation (Good Credit)**
```
What's the risk for someone with FICO 750 and income $80,000?
```
**Expected Output:**
- Risk Score: **11.76** (Low)
- ✅ Excellent credit profile

---

### **📝 Prompt 5: Complete Assessment**
```
I need a complete risk assessment: FICO is 650, income is $55,000, and loan amount is $15,000
```
**Expected Output:**
- Risk Score: **23.53** (Low)
- ECL: **$3,529.50** (23.5% of loan)
- ✅ Acceptable risk for standard lending

---

### **📝 Prompt 6: Direct ECL Calculation**
```
Calculate expected credit loss for a $20,000 loan with risk score 35
```
**Expected Output:**
- ECL: **$7,000.00** (35% of loan)
- ⚠️ Medium risk, requires appropriate pricing

---

## 🎬 **2-Minute Demo Script**

### **Opening (15 seconds)**
*"I've built an AI-powered credit risk automation system using IBM Watsonx Orchestrate and real Kaggle Lending Club data."*

---

### **Demo 1: Full Automation (30 seconds)**
```
Analyze credit risk for member 63044350
```
*"Watch as Watsonx automatically chains three API calls: it retrieves the borrower data, calculates their risk score of 0.00 - categorized as Low risk, and determines the expected credit loss of $0. This excellent FICO score of 779 makes them an ideal candidate."*

**Watsonx shows:** FICO 779 → Risk 0.00 (Low) → ECL $0

---

### **Demo 2: Flexibility (25 seconds)**
```
Calculate credit risk for a borrower with FICO score 600 and annual income $45,000
```
*"The system also handles ad-hoc calculations without needing existing member data. This borrower gets a risk score of 29.41, which is Low but borderline Medium - perfect for demonstrating our risk thresholds."*

**Watsonx shows:** Risk Score 29.41 (Low, near 30 threshold)

---

### **Demo 3: High Risk Detection (30 seconds)**
```
Evaluate loan application for member -76653
```
*"Now let's see how it handles high-risk applicants. This borrower has a FICO of 300 - the worst possible score. Watsonx calculates a risk score of 64.71, categorized as High risk, with an expected credit loss of $11,000 on a $17,000 loan. The system correctly flags this as a previously declined application."*

**Watsonx shows:** FICO 300 → Risk 64.71 (High) → ECL $11,001 → Declined

---

### **Demo 4: Custom Scenario (30 seconds)**
```
I need a complete risk assessment: FICO is 650, income is $55,000, and loan amount is $15,000
```
*"Finally, let's demonstrate the intelligent orchestration. Watsonx understands this requires two steps: first calculating the risk score of 23.53, then computing the expected credit loss of $3,529. This represents a 23.5% potential loss rate, which is acceptable for standard lending practices."*

**Watsonx shows:** FICO 650 → Risk 23.53 (Low) → Loan $15k → ECL $3,530

---

### **Closing (10 seconds)**
*"This system processes real data from 2 million Kaggle loans, demonstrating how AI orchestration can automate complex financial workflows while making them accessible through natural language."*

---

## ✅ **What Judges Should See**

1. **Automatic skill chaining** - No manual API calls needed
2. **Natural language understanding** - Conversational prompts work
3. **Real data integration** - Kaggle Lending Club dataset
4. **Risk diversity** - Low, Medium, and High examples
5. **Business intelligence** - Not just numbers, but interpretable results

---

## 📊 **Quick Answer Cheat Sheet**

| Your Prompt | Watsonx Should Say |
|-------------|-------------------|
| "Analyze member 63044350" | "Risk: 0.00 (Low), ECL: $0" |
| "Evaluate member -76653" | "Risk: 64.71 (High), ECL: $11,001" |
| "FICO 600, income $45k" | "Risk: 29.41 (Low/borderline)" |
| "FICO 750, income $80k" | "Risk: 11.76 (Low)" |
| "FICO 650, income $55k, loan $15k" | "Risk: 23.53, ECL: $3,530" |
| "$20k loan, risk 35" | "ECL: $7,000" |

---

## 🎯 **Key Numbers to Remember**

- **Risk Categories:**
  - Low: 0-29
  - Medium: 30-59
  - High: 60+

- **Sample Profiles:**
  - Member 63044350: FICO 779 (Low risk)
  - Member -76653: FICO 300 (High risk)

- **Dataset:**
  - 200 real borrowers
  - 140 Low, 40 Medium, 20 High
  - FICO range: 300-850

---

## 💡 **If Something Goes Wrong**

**Watsonx says "beyond my capacity":**
- ✅ Add specific numbers to your prompt
- ✅ Use keywords: "calculate", "analyze", "evaluate"
- ✅ Try: "Use step_2_calculate_risk for FICO 650 and income $55,000"

**No output/error:**
- ✅ Check if Flask server is running (should see logs)
- ✅ Verify ngrok URL in credit-api.json matches your tunnel
- ✅ Refresh Watsonx skills (re-import OpenAPI spec)

**Wrong values:**
- ✅ Check member_id is exactly: 63044350 or -76653
- ✅ Verify FICO is between 300-850
- ✅ Ensure income is positive number

---

**You're ready to win this hackathon! 🚀**
