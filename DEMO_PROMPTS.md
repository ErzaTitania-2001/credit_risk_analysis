# 🎯 Watsonx Demo Prompts - Quick Reference

## ✅ Member-Based Prompts (Automatic Skill Chain)

### Low Risk Example
```
"Analyze credit risk for member 63044350"
"Complete risk assessment for borrower 63044350"
"Evaluate member 63044350"
```
**Expected Result**: FICO 779, Income $96k, Low Risk (~22), ECL low

---

### High Risk Example
```
"Analyze credit risk for member -76653"
"Evaluate loan application for member -76653"
"Complete assessment for borrower -76653"
```
**Expected Result**: FICO 300, Income $69k, High Risk (~72), ECL high

---

## ✅ Direct Calculation Prompts (Flexible Input)

### Medium Risk Scenario
```
"Calculate risk for FICO score 600 and annual income $45,000"
"What's the credit risk for FICO 600 and income $45,000?"
"Assess risk: FICO 600, income $45,000"
```
**Expected Result**: Risk Score ~45.5, Medium Risk

---

### Low Risk Scenario
```
"Calculate risk for FICO score 720 and annual income $80,000"
"Risk assessment for FICO 720 and income $80,000"
```
**Expected Result**: Risk Score ~22.8, Low Risk

---

### High Risk Scenario
```
"Calculate risk for FICO score 350 and annual income $25,000"
"What's the risk for FICO 350 and income $25,000?"
```
**Expected Result**: Risk Score ~78, High Risk

---

## ✅ Complete Direct Workflow (Multi-Step)

```
"Calculate risk for FICO 600 and income $45,000, then calculate ECL for a $10,000 loan"
```
**Expected Result**: 
1. Risk Score: 45.5 (Medium)
2. ECL: $4,550

---

## ✅ Conversational Follow-Up

```
User: "Calculate risk for FICO 650 and income $55,000"
Watsonx: [Returns Medium Risk, score 38.2]

User: "Now calculate the expected loss for a $12,000 loan"
Watsonx: [Should remember risk_score and return ECL: $4,584]
```

---

## 📊 Quick Risk Reference

| FICO Range | Income Range | Risk Category | Risk Score |
|------------|--------------|---------------|------------|
| 720-850    | $70k+        | **Low**       | < 30       |
| 580-719    | $40k-$70k    | **Medium**    | 30-60      |
| 300-579    | < $40k       | **High**      | > 60       |

---

## 🎬 Demo Flow Recommendation

1. **Start with Member Lookup** (Shows automation):
   ```
   "Analyze member 63044350"
   ```
   → Demonstrates automatic skill chaining (getData → calculateRisk → calculateECL)

2. **Show Flexibility with Direct Input**:
   ```
   "Calculate risk for FICO 600 and income $45,000"
   ```
   → Demonstrates system can work without pre-existing member data

3. **Show Complete Workflow**:
   ```
   "For FICO 350 and income $25,000, calculate risk and ECL for a $5,000 loan"
   ```
   → Demonstrates end-to-end calculation from raw inputs

---

## 🔧 Testing Checklist

- [ ] Member 63044350 returns Low Risk
- [ ] Member -76653 returns High Risk  
- [ ] Direct FICO 600, Income $45k returns Medium Risk (~45.5)
- [ ] Direct FICO 720, Income $80k returns Low Risk (~22.8)
- [ ] Direct FICO 350, Income $25k returns High Risk (~78)
- [ ] ECL calculation works with manual risk_score input
- [ ] Skill chaining works (getData → calculateRisk → calculateECL)
- [ ] Direct calculation works (calculateRisk standalone)

---

## 💡 Key Talking Points for Judges

1. **Dual Workflow Support**: "Our system supports both member lookup for existing customers AND direct calculation for new applicants"

2. **Automated Orchestration**: "Watsonx automatically chains three skills together - data retrieval, risk calculation, and loss estimation"

3. **Flexible Input**: "Users can provide either a member ID or raw FICO/income data, and the system adapts"

4. **Real Data**: "Using 200 real borrower records from Kaggle's Lending Club dataset (2007-2018)"

5. **Risk Diversity**: "70% low risk, 20% medium risk, 10% high risk - mirrors real-world distribution"

6. **Production-Ready**: "Error handling, logging, input validation, comprehensive API documentation"
