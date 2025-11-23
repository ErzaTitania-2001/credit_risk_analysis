# 🎯 Hackathon Demo Checklist

## Pre-Demo Setup (5 minutes before)

### 1. Server Setup
- [ ] Open PowerShell terminal
- [ ] Navigate to project: `cd C:\Users\puppy\credit_risk_analysis`
- [ ] Start Flask server: `python app.py`
- [ ] Verify startup message shows "Loaded 100 borrower records"
- [ ] Keep this terminal window visible

### 2. Ngrok Setup
- [ ] Open second PowerShell terminal
- [ ] Run: `ngrok http 5000`
- [ ] Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.app`)
- [ ] Update `credit-api.json` servers URL with Ngrok URL
- [ ] Keep this terminal window visible

### 3. Test Connectivity
- [ ] Open third PowerShell terminal
- [ ] Run: `.\test_api.ps1`
- [ ] Verify all 8 tests pass
- [ ] Check for "ALL TESTS COMPLETED SUCCESSFULLY!"

### 4. Watsonx Integration
- [ ] Log into IBM Watsonx Orchestrate
- [ ] Go to Skills → Import Skills
- [ ] Upload `credit-api.json`
- [ ] Verify three skills appear:
  - [ ] getData - Get User Info
  - [ ] getRisk - Calculate Risk
  - [ ] getECL - Calculate Loss

### 5. Browser Demo (Optional)
- [ ] Open browser to `http://localhost:5000/demo.html`
- [ ] Test one complete workflow
- [ ] Keep browser tab open

---

## Demo Flow (4 minutes)

### Slide 1: Introduction (30 seconds)
**Say:**
> "We've built a Credit Risk Automation System that demonstrates IBM Watsonx Orchestrate's ability to coordinate multiple microservices for automated lending decisions."

**Show:**
- Architecture diagram (Watsonx → Flask API → Data)

### Slide 2: The Problem (20 seconds)
**Say:**
> "Credit bureaus process millions of loan applications. Each requires retrieving borrower data, calculating risk scores, and estimating potential losses. This typically takes hours of manual work."

### Slide 3: Our Solution (20 seconds)
**Say:**
> "Our system automates this entire workflow using three API endpoints that Watsonx Orchestrate calls sequentially."

**Show:**
- Endpoints list:
  1. /get_data - Retrieve borrower info
  2. /risk_score - Calculate risk (0-100)
  3. /calc_ecl - Calculate expected loss

### Live Demo: Watsonx (90 seconds)

#### Part 1: Simple Query
**Do:**
1. Open Watsonx Orchestrate interface
2. Type in chat: `"Analyze credit risk for member 68407277"`
3. Press Enter

**Say while waiting:**
> "Watch as Watsonx automatically calls our three APIs in sequence. First, it retrieves the borrower's data..."

**Point out:**
- First API call: getData shows member info
- Second API call: getRisk calculates risk score
- Third API call: getECL calculates potential loss

**Expected Result:**
```
Member 68407277
- Income: $55,000
- FICO Score: 679
- Requested Loan: $3,600
- Risk Score: 20.12 (Low)
- Expected Loss: $724.32
- Recommendation: APPROVE
```

#### Part 2: Different Profile
**Do:**
1. Type: `"What's the risk for member 66310712?"`

**Say:**
> "Let's try a different profile with higher income and better credit..."

**Expected Result:**
```
Member 66310712
- Income: $110,000
- FICO Score: 789
- Requested Loan: $35,000
- Risk Score: 0.00 (Low)
- Expected Loss: $0.00
- Recommendation: APPROVE (Excellent Profile)
```

### Slide 4: Technical Deep Dive (30 seconds)

**Switch to VS Code:**

**Show `app.py` lines 28-70:**
> "Our Flask API includes robust error handling, input validation, and professional logging. Every endpoint validates its inputs before processing."

**Show running test_api.ps1 results:**
> "We have a comprehensive test suite with 8 tests covering all endpoints and error cases - all passing."

**Show `demo.html` in browser:**
> "We also built an interactive demo interface for manual testing and debugging."

### Slide 5: Business Impact (20 seconds)
**Say:**
> "This automation reduces loan processing time from hours to seconds, while maintaining consistency and accuracy. The modular API design means each component can be independently scaled and monitored."

**Highlight:**
- Processing time: Hours → Seconds
- Accuracy: Human variability → Consistent algorithm
- Scalability: Single instance → Distributed microservices
- Auditability: Manual logs → Structured logging

### Slide 6: Architecture & Tech Stack (20 seconds)

**Show diagram:**
```
┌──────────────────────┐
│ Watsonx Orchestrate  │ ← Agent/UI Layer
└──────────┬───────────┘
           │ HTTPS (Ngrok)
           ▼
┌──────────────────────┐
│ Flask REST API       │ ← Business Logic
│ - Error Handling     │
│ - Input Validation   │
│ - Logging            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Pandas DataFrame     │ ← Mock Database
│ (100 real records)   │
└──────────────────────┘
```

**Mention:**
- Python 3.9+ with Flask
- OpenAPI 3.0 specification
- CORS-enabled for cross-origin
- 100 real loan records

### Slide 7: What's Next (10 seconds)
**Say:**
> "Future enhancements include machine learning risk models, real database integration, and authentication for production deployment."

---

## Emergency Backup Plans

### If Watsonx is Down
**Use demo.html:**
1. Open browser to `http://localhost:5000/demo.html`
2. Enter member ID: 68407277
3. Click "Run Complete Analysis"
4. Show the step-by-step execution
5. Explain: "This is the same workflow Watsonx automates"

### If Server Crashes
**Have this ready:**
1. In terminal: `python app.py`
2. Wait 2 seconds for startup
3. If still fails, use mock data mode (automatic)

### If Network Issues
**Show pre-recorded video:**
- Have screen recording of successful demo
- Narrate over the recording

---

## Sample Member IDs (Keep handy)

| Member ID | Profile Type          | Risk  | Notes                    |
|-----------|-----------------------|-------|--------------------------|
| 68407277  | Standard              | Low   | Demo primary example     |
| 66310712  | Excellent             | Low   | High income, high FICO   |
| 68577849  | Premium               | Low   | 804 FICO, $112k income   |
| 67849662  | Charged Off History   | Low   | Show historical data     |
| 68466924  | Medium Loan           | Low   | $21k loan, $47k income   |

---

## Questions & Answers Prep

### Q: "How does the risk calculation work?"
**A:** "We use a formula: base score of 100 minus FICO divided by 8.5. Higher FICO scores result in lower risk. We also adjust down by 15 points for borrowers earning over $80,000, as higher income correlates with better repayment ability."

### Q: "Can this scale to millions of records?"
**A:** "The current implementation uses Pandas for rapid prototyping. For production scale, we'd replace it with PostgreSQL or a distributed database like MongoDB. The API design is database-agnostic."

### Q: "What about security?"
**A:** "For production, we'd add OAuth 2.0 authentication, API rate limiting, and encrypt sensitive data. The current demo focuses on the orchestration workflow."

### Q: "How long did this take to build?"
**A:** "The core API took about 2 hours. We spent additional time on error handling, testing, and documentation to make it production-quality."

### Q: "Why Watsonx Orchestrate?"
**A:** "Watsonx eliminates the need for custom UI and workflow logic. It provides natural language interface, handles the sequential API calls, and manages error states - all out of the box."

---

## Post-Demo Actions

### Immediate (During Q&A)
- [ ] Answer questions confidently
- [ ] Show code if technical questions arise
- [ ] Reference test results if questioned about reliability
- [ ] Offer to send GitHub repo link

### Follow-up
- [ ] Push code to GitHub
- [ ] Share demo recording
- [ ] Send OpenAPI spec to interested parties
- [ ] Connect with IBM Watsonx team

---

## Technical Details (For Deep Questions)

### API Response Times
- `/get_data`: ~10ms (DataFrame lookup)
- `/risk_score`: ~5ms (simple calculation)
- `/calc_ecl`: ~5ms (simple calculation)
- **Total workflow**: ~20-30ms

### Error Handling Coverage
- Missing JSON body → 400
- Missing required fields → 400
- Invalid data types → 400
- Out-of-range values → 400 with warning
- User not found → 404
- Server errors → 500 with logging

### Data Statistics
- 100 loan records
- FICO range: 669-839
- Income range: $20k-$195k
- Loan range: $1.4k-$35k
- Status distribution:
  - Fully Paid: 73%
  - Current: 15%
  - Charged Off: 11%
  - In Grace Period: 1%

---

## Success Metrics

### Demo is Successful if:
- ✅ All three APIs execute in Watsonx
- ✅ Results display correctly
- ✅ At least 2 member IDs demonstrated
- ✅ One question answered technically
- ✅ Judges understand the value proposition

### Bonus Points:
- 🌟 Show error handling (invalid member ID)
- 🌟 Show the test suite running
- 🌟 Demonstrate the HTML interface
- 🌟 Explain the risk algorithm clearly
- 🌟 Connect to real-world use case

---

## Confidence Boosters

### Remember:
1. **You've tested this** - 8/8 tests passing
2. **The code is solid** - Error handling on every endpoint
3. **The docs are complete** - Three documentation files
4. **The data is real** - 100 actual loan records
5. **The demo works** - You've run it successfully

### If Nervous:
- Take a deep breath
- Remember: Judges want you to succeed
- Focus on the problem you're solving
- Let your enthusiasm show
- The technical quality speaks for itself

---

**🎤 Break a leg! You've got this! 🚀**

**Last Checked**: [Current Date]  
**Status**: ✅ READY FOR DEMO
