# 🎯 Watsonx Demo Prompts - With Risk Diversity

## ✅ Updated Dataset (107 borrowers)
- **Low Risk**: 102 borrowers (95.3%) - Original quality borrowers
- **Medium Risk**: 4 borrowers (3.7%) - Marginal credit profiles
- **High Risk**: 1 borrower (0.9%) - Should be declined

---

## 🟢 LOW RISK Examples (Approve)

### Prompt 1: Standard Approval
```
"Analyze credit risk for member 68407277"
```
**Expected**: FICO 679, Income $55k, Risk 20.12 (Low) → **APPROVE**

### Prompt 2: Excellent Profile
```
"Evaluate member 66310712"
```
**Expected**: FICO 789, Income $110k, Risk 0.00 (Low) → **APPROVE**

---

## 🟡 MEDIUM RISK Examples (Marginal)

### Prompt 3: Borderline Case
```
"What's the risk for member 999001?"
```
**Expected**: FICO 550, Income $25k, Risk 35.29 (Medium) → **CAUTION - Manual Review Needed**

### Prompt 4: Subprime Borrower
```
"Analyze member 999002"
```
**Expected**: FICO 580, Income $30k, Risk 31.76 (Medium) → **CAUTION - Manual Review Needed**

---

## 🔴 HIGH RISK Example (Decline)

### Prompt 5: Clear Rejection
```
"Should we approve member 999901?"
```
**Expected**: FICO 320, Income $22k, Risk 62.35 (High) → **DECLINE**

---

## 🎪 Recommended Demo Flow

### Act 1: The Success Story (30 sec)
```
"Analyze credit risk for member 68407277"
```
**Narration**: "Here's a typical applicant with good credit. The system automatically retrieves their data, calculates a risk score of 20.12 - which is Low risk - and recommends approval. Expected loss is only $724 on a $3,600 loan."

### Act 2: The Premium Client (20 sec)
```
"Now check member 66310712"
```
**Narration**: "This borrower has excellent credit - FICO 789 and $110k income. Risk score is 0.00. These are your best customers."

### Act 3: The Marginal Case (30 sec)
```
"What about member 999001?"
```
**Narration**: "Now here's where it gets interesting. This borrower has a FICO of 550 and lower income. The risk score jumps to 35.29 - that's Medium risk territory. The system flags this for manual review rather than auto-approving."

### Act 4: The Clear Rejection (20 sec)
```
"Should we approve member 999901?"
```
**Narration**: "And finally, a high-risk case. FICO 320, high debt-to-income ratio. Risk score is 62 - that's High risk. This would be declined automatically."

---

## 📊 Quick Reference Table

| Member ID | FICO | Income  | Loan    | Risk Score | Category | Recommendation          |
|-----------|------|---------|---------|------------|----------|-------------------------|
| 68407277  | 679  | $55k    | $3.6k   | 20.12      | Low      | ✅ APPROVE              |
| 66310712  | 789  | $110k   | $35k    | 0.00       | Low      | ✅ APPROVE              |
| 68577849  | 804  | $112k   | $18k    | 0.00       | Low      | ✅ APPROVE              |
| 999003    | 620  | $35k    | $10k    | 27.06      | Low      | ✅ APPROVE (borderline) |
| 999001    | 550  | $25k    | $15k    | 35.29      | Medium   | ⚠️ MANUAL REVIEW        |
| 999002    | 580  | $30k    | $20k    | 31.76      | Medium   | ⚠️ MANUAL REVIEW        |
| 999005    | 560  | $28k    | $8k     | 34.12      | Medium   | ⚠️ MANUAL REVIEW        |
| 999902    | 350  | $18k    | $50k    | 58.82      | Medium   | ⚠️ HIGH CAUTION         |
| 999901    | 320  | $22k    | $30k    | 62.35      | High     | ❌ DECLINE              |

---

## 🎬 Full Comparison Demo Script

```
Prompt: "Compare the risk of members 68407277, 999001, and 999901"
```

**What happens**:
- Member 68407277: Low risk (20.12) - Safe borrower
- Member 999001: Medium risk (35.29) - Marginal 
- Member 999901: High risk (62.35) - Decline

**Narration**: "You can see how the system differentiates between quality tiers. From auto-approve, to manual review, to auto-decline. This is the power of automated risk scoring."

---

## 💡 Why This Dataset Now Works Better

**Before**: 
- All 100 borrowers were Low Risk
- No demonstration of risk differentiation
- Unrealistic for credit decisioning

**After**:
- 95% Low Risk (realistic - these are funded loans)
- 4% Medium Risk (shows the system catches borderline cases)
- 1% High Risk (demonstrates clear declines)
- More realistic distribution
- Better showcases the API's value

---

## 🎯 Best Opening Line

**Use this:**
```
"Let me show you three borrowers across the risk spectrum: 
68407277, 999001, and 999901"
```

Then show:
1. First: Low risk → Approve
2. Second: Medium risk → Manual review
3. Third: High risk → Decline

This immediately demonstrates the system's ability to differentiate risk levels.

---

## 🚀 Ready to Demo!

Your dataset now has:
- ✅ Real-world distribution
- ✅ Approval cases (Low risk)
- ✅ Borderline cases (Medium risk)
- ✅ Decline cases (High risk)
- ✅ Shows system's decision-making range

**Start the server and test with the new member IDs!**
