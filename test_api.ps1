# Credit Risk API Test Script
# This script tests all endpoints with real data from borrowers.csv

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CREDIT RISK API - TEST SUITE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET
    Write-Host "Status: $($health.status)" -ForegroundColor Green
    Write-Host "Records Loaded: $($health.records_loaded)" -ForegroundColor Green
}
catch {
    Write-Host "Health check failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 2: Get Data - Valid Member
Write-Host "Test 2: Get User Data (member_id: 68407277)" -ForegroundColor Yellow
try {
    $body = @{member_id=68407277} | ConvertTo-Json
    $userData = Invoke-RestMethod -Uri "http://localhost:5000/get_data" -Method POST -Body $body -ContentType "application/json"
    Write-Host "Member ID: $($userData.member_id)" -ForegroundColor Green
    Write-Host "Annual Income: $($userData.annual_inc)" -ForegroundColor Green
    Write-Host "FICO Score: $($userData.fico_range_high)" -ForegroundColor Green
    Write-Host "Loan Amount: $($userData.loan_amnt)" -ForegroundColor Green
}
catch {
    Write-Host "Get data failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 3: Get Data - Invalid Member
Write-Host "Test 3: Get User Data - Invalid ID (Expected 404)" -ForegroundColor Yellow
try {
    $body = @{member_id=99999} | ConvertTo-Json
    $userData = Invoke-RestMethod -Uri "http://localhost:5000/get_data" -Method POST -Body $body -ContentType "application/json" -ErrorAction Stop
    Write-Host "Should have returned 404 error" -ForegroundColor Red
}
catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 404) {
        Write-Host "Correctly returned 404 for invalid member_id" -ForegroundColor Green
    } else {
        Write-Host "Unexpected error: $($_.Exception.Message)" -ForegroundColor Red
    }
}
Write-Host ""

# Test 4: Calculate Risk Score
Write-Host "Test 4: Calculate Risk Score" -ForegroundColor Yellow
try {
    $body = @{
        fico_range_high = 679
        annual_inc = 55000
    } | ConvertTo-Json
    $riskData = Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json"
    Write-Host "Risk Score: $($riskData.risk_score)" -ForegroundColor Green
    Write-Host "Risk Category: $($riskData.risk_category)" -ForegroundColor Green
}
catch {
    Write-Host "Risk score calculation failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 5: Calculate Risk Score - High Income Adjustment
Write-Host "Test 5: Risk Score with High Income (>80k adjustment)" -ForegroundColor Yellow
try {
    $body = @{
        fico_range_high = 789
        annual_inc = 110000
    } | ConvertTo-Json
    $riskData = Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json"
    Write-Host "Risk Score: $($riskData.risk_score) (Should be lower due to high income)" -ForegroundColor Green
    Write-Host "Risk Category: $($riskData.risk_category)" -ForegroundColor Green
}
catch {
    Write-Host "Risk score calculation failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 6: Calculate Expected Credit Loss
Write-Host "Test 6: Calculate Expected Credit Loss" -ForegroundColor Yellow
try {
    $body = @{
        loan_amnt = 10000
        risk_score = 20.12
    } | ConvertTo-Json
    $eclData = Invoke-RestMethod -Uri "http://localhost:5000/calc_ecl" -Method POST -Body $body -ContentType "application/json"
    Write-Host "Expected Credit Loss: $($eclData.expected_credit_loss) $($eclData.currency)" -ForegroundColor Green
}
catch {
    Write-Host "ECL calculation failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 7: Missing Required Field
Write-Host "Test 7: Missing Required Field (Expected 400)" -ForegroundColor Yellow
try {
    $body = @{fico_range_high=700} | ConvertTo-Json
    $result = Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json" -ErrorAction Stop
    Write-Host "Should have returned 400 error for missing field" -ForegroundColor Red
}
catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 400) {
        Write-Host "Correctly returned 400 for missing required field" -ForegroundColor Green
    } else {
        Write-Host "Unexpected error: $($_.Exception.Message)" -ForegroundColor Red
    }
}
Write-Host ""

# Test 8: Complete Flow with Real CSV Data
Write-Host "Test 8: Complete Flow - Member 66310712" -ForegroundColor Yellow
try {
    # Step 1: Get user data
    $body = @{member_id=66310712} | ConvertTo-Json
    $user = Invoke-RestMethod -Uri "http://localhost:5000/get_data" -Method POST -Body $body -ContentType "application/json"
    Write-Host "  Step 1 - Retrieved user data" -ForegroundColor Cyan
    
    # Step 2: Calculate risk
    $body = @{
        fico_range_high = $user.fico_range_high
        annual_inc = $user.annual_inc
    } | ConvertTo-Json
    $risk = Invoke-RestMethod -Uri "http://localhost:5000/risk_score" -Method POST -Body $body -ContentType "application/json"
    Write-Host "  Step 2 - Calculated risk score: $($risk.risk_score)" -ForegroundColor Cyan
    
    # Step 3: Calculate ECL
    $body = @{
        loan_amnt = $user.loan_amnt
        risk_score = $risk.risk_score
    } | ConvertTo-Json
    $ecl = Invoke-RestMethod -Uri "http://localhost:5000/calc_ecl" -Method POST -Body $body -ContentType "application/json"
    Write-Host "  Step 3 - Expected Credit Loss: $($ecl.expected_credit_loss) $($ecl.currency)" -ForegroundColor Cyan
    
    Write-Host "Complete workflow executed successfully!" -ForegroundColor Green
    Write-Host "  Summary:" -ForegroundColor White
    Write-Host "    Loan Amount: `$$($user.loan_amnt)" -ForegroundColor White
    Write-Host "    Risk Score: $($risk.risk_score) ($($risk.risk_category))" -ForegroundColor White
    Write-Host "    Expected Loss: `$$($ecl.expected_credit_loss)" -ForegroundColor White
}
catch {
    Write-Host "Complete flow failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ALL TESTS COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
