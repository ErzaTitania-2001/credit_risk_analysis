# IBM Watsonx Orchestrate - Demo Prompts

## ✅ Skills Imported Successfully
- **step_1_get_user_info** (getData) - Lookup member by ID
- **step_2_calculate_risk** (calculateRisk) - Direct FICO/income risk calculation
- **step_3_calculate_loss** (calculateECL) - Calculate expected credit loss

---

## 🎯 **WORKFLOW 1: Member-Based Analysis (Full Automation)**

### Low Risk Example
```
Analyze credit risk for member 63044350
```
**Expected Flow:**
1. Watsonx calls `step_1_get_user_info` with member_id: 63044350
2. Gets: FICO 779, Income $96,000, Loan $12,000
3. Automatically chains to `step_2_calculate_risk`
4. Returns: Risk Score ~15, Category: Low
5. Chains to `step_3_calculate_loss`
6. Returns: ECL ~$180

---

### Medium Risk Example
```
What's the credit risk for member 105?
```
**Expected:**
- FICO ~650-700
- Risk Category: Medium
- Risk Score: 30-60

---

### High Risk Example
```
Evaluate loan application for member -76653
```
**Expected Flow:**
1. Gets: FICO 300, Income $69,558, Status: Declined
2. Risk Score ~95, Category: High
3. ECL will be significant

---

## 🎯 **WORKFLOW 2: Direct Calculation (No Member Lookup)**

### Test Scenario 1: Medium Risk Borrower
```
Calculate credit risk for a borrower with FICO score 600 and annual income $45,000
```
**Expected:**
- Watsonx calls `step_2_calculate_risk` directly
- Input: {"fico_range_high": 600, "annual_inc": 45000}
- Output: Risk Score ~60, Risk Category: Medium

---

### Test Scenario 2: Low Risk Borrower
```
What's the risk for someone with FICO 750 and income $80,000?
```
**Expected:**
- Risk Score ~18
- Risk Category: Low

---

### Test Scenario 3: High Risk Borrower
```
Assess risk for FICO 500 and annual income $30,000
```
**Expected:**
- Risk Score ~85
- Risk Category: High

---

## 🎯 **WORKFLOW 3: Complete Custom Calculation**

### Full Risk Assessment
```
I need a complete risk assessment: FICO is 650, income is $55,000, and loan amount is $15,000
```

**Expected Watsonx Orchestration:**
1. Calls `step_2_calculate_risk` with FICO 650, income $55,000
   - Gets risk_score (e.g., 45)
2. Then calls `step_3_calculate_loss` with loan $15,000, risk_score 45
   - Gets expected_credit_loss (e.g., $675)

**Final Answer Should Include:**
- Risk Score: ~45
- Risk Category: Medium
- Expected Credit Loss: ~$675

---

## 🎯 **WORKFLOW 4: Loss Calculation Only**

### Direct ECL Calculation
```
Calculate expected credit loss for a $20,000 loan with risk score 35
```
**Expected:**
- Watsonx calls `step_3_calculate_loss` directly
- Input: {"loan_amnt": 20000, "risk_score": 35}
- Output: ECL ~$700

---

## 📊 **Quick Reference: Sample Members**

| Member ID | FICO | Income | Status | Risk |
|-----------|------|--------|--------|------|
| 63044350 | 779 | $96,000 | Current | Low |
| -76653 | 300 | $69,558 | Declined | High |
| 105 | ~650-700 | Varies | - | Medium |

---

## 🎬 **Recommended Demo Flow**

### 1. Start with Member Lookup (Shows Full Automation)
```
Analyze credit risk for member 63044350
```
*"This demonstrates our automated workflow - from member lookup through risk calculation to expected loss estimation."*

---

### 2. Show Direct Calculation (Flexibility)
```
Calculate credit risk for a borrower with FICO score 600 and annual income $45,000
```
*"Watsonx can also calculate risk directly from credit parameters without needing an existing member."*

---

### 3. Complete Custom Assessment (Power User)
```
I need a complete risk assessment: FICO is 650, income is $55,000, and loan amount is $15,000
```
*"The AI agent intelligently orchestrates multiple skills to provide comprehensive analysis."*

---

### 4. High Risk Example (Show Range)
```
Evaluate loan application for member -76653
```
*"Our system accurately identifies high-risk applications from rejected loan data."*

---

## 🔧 **Testing Individual Skills**

If Watsonx asks for specific input parameters:

### For step_2_calculate_risk:
```json
{
  "fico_range_high": 600,
  "annual_inc": 45000
}
```

### For step_3_calculate_loss:
```json
{
  "loan_amnt": 15000,
  "risk_score": 45
}
```

### For step_1_get_user_info:
```json
{
  "member_id": 63044350
}
```

---

## 💡 **Tips for Best Results**

1. **Use natural language** - Watsonx understands conversational prompts
2. **Be specific with numbers** - Include actual FICO scores and income amounts
3. **Ask follow-up questions** - "What if the income was higher?" to show adaptability
4. **Compare scenarios** - "Compare member 63044350 with member -76653"
5. **Request explanations** - "Why is this considered high risk?"

---

## 🚨 **Troubleshooting**

If Watsonx says "beyond my capacity":
- ✅ Make your prompt more specific with actual numbers
- ✅ Use phrases like "calculate", "assess", "evaluate"
- ✅ Include the word "risk" in your prompt
- ✅ Reference the skill names if needed

If skills don't chain automatically:
- ✅ Start with member ID to trigger getData workflow
- ✅ For direct calculation, explicitly mention FICO and income
- ✅ Ask Watsonx to "use step_2_calculate_risk" if needed

---

## 🎯 **Success Criteria**

✅ Watsonx recognizes skill names and maps them to operations
✅ Member-based queries trigger full automated workflow
✅ Direct FICO/income inputs work without member lookup
✅ Skills chain together intelligently based on context
✅ Natural language prompts execute the right skills

**Your API is ready for the hackathon demo! 🚀**
