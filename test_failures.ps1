# Failure Test Suite for Credit Risk API
# Tests error handling and edge cases

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "FAILURE & EDGE CASE TEST SUITE" -ForegroundColor Magenta
Write-Host "========================================`n" -ForegroundColor Magenta

$baseUrl = "http://localhost:5000"
$testsPassed = 0
$testsFailed = 0

# Helper function to test API endpoint
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [hashtable]$Body,
        [bool]$ShouldFail = $false
    )
    
    Write-Host "`n$Name" -ForegroundColor Cyan
    Write-Host "Payload: $($Body | ConvertTo-Json -Compress)" -ForegroundColor Gray
    
    $jsonBody = $Body | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $Url -Method POST -Body $jsonBody -ContentType "application/json" -ErrorAction Stop
        
        if ($ShouldFail) {
            Write-Host "❌ UNEXPECTED SUCCESS - This should have failed!" -ForegroundColor Red
            $script:testsFailed++
        } else {
            Write-Host "✅ PASSED" -ForegroundColor Green
            $response | Format-List
            $script:testsPassed++
        }
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        $errorMessage = $_.Exception.Message
        
        if ($ShouldFail) {
            Write-Host "✅ PASSED - Failed as expected (HTTP $statusCode)" -ForegroundColor Green
            Write-Host "   Error: $errorMessage" -ForegroundColor Gray
            $script:testsPassed++
        } else {
            Write-Host "❌ UNEXPECTED FAILURE" -ForegroundColor Red
            Write-Host "   Error: $errorMessage" -ForegroundColor Red
            $script:testsFailed++
        }
    }
}

Write-Host "=== CATEGORY 1: Invalid Member IDs ===" -ForegroundColor Yellow

Test-Endpoint -Name "Test 1.1: Non-existent member (999999999)" `
    -Url "$baseUrl/get_data" `
    -Body @{member_id=999999999} `
    -ShouldFail $true

Test-Endpoint -Name "Test 1.2: Zero member ID" `
    -Url "$baseUrl/get_data" `
    -Body @{member_id=0} `
    -ShouldFail $true

Test-Endpoint -Name "Test 1.3: Negative member ID" `
    -Url "$baseUrl/get_data" `
    -Body @{member_id=-999999} `
    -ShouldFail $true

Write-Host "`n=== CATEGORY 2: Invalid FICO Scores ===" -ForegroundColor Yellow

Test-Endpoint -Name "Test 2.1: FICO too low (200)" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=200; annual_inc=50000} `
    -ShouldFail $true

Test-Endpoint -Name "Test 2.2: FICO too high (900)" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=900; annual_inc=50000} `
    -ShouldFail $true

Test-Endpoint -Name "Test 2.3: Negative FICO (-500)" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=-500; annual_inc=40000} `
    -ShouldFail $true

Test-Endpoint -Name "Test 2.4: Zero FICO" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=0; annual_inc=50000} `
    -ShouldFail $true

Write-Host "`n=== CATEGORY 3: Invalid Income Values ===" -ForegroundColor Yellow

Test-Endpoint -Name "Test 3.1: Negative income (-50000)" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=700; annual_inc=-50000} `
    -ShouldFail $true

Test-Endpoint -Name "Test 3.2: Zero income (edge case)" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=650; annual_inc=0} `
    -ShouldFail $false

Write-Host "`n=== CATEGORY 4: Invalid Loan Amounts ===" -ForegroundColor Yellow

Test-Endpoint -Name "Test 4.1: Negative loan (-10000)" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{loan_amnt=-10000; risk_score=30} `
    -ShouldFail $true

Test-Endpoint -Name "Test 4.2: Zero loan (edge case)" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{loan_amnt=0; risk_score=50} `
    -ShouldFail $false

Write-Host "`n=== CATEGORY 5: Invalid Risk Scores ===" -ForegroundColor Yellow

Test-Endpoint -Name "Test 5.1: Risk score > 100 (150)" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{loan_amnt=15000; risk_score=150} `
    -ShouldFail $true

Test-Endpoint -Name "Test 5.2: Negative risk score (-25)" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{loan_amnt=20000; risk_score=-25} `
    -ShouldFail $true

Write-Host "`n=== CATEGORY 6: Missing Required Parameters ===" -ForegroundColor Yellow

Test-Endpoint -Name "Test 6.1: Missing FICO score" `
    -Url "$baseUrl/risk_score" `
    -Body @{annual_inc=50000} `
    -ShouldFail $true

Test-Endpoint -Name "Test 6.2: Missing income" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=700} `
    -ShouldFail $true

Test-Endpoint -Name "Test 6.3: Missing loan amount" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{risk_score=30} `
    -ShouldFail $true

Test-Endpoint -Name "Test 6.4: Missing risk score" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{loan_amnt=15000} `
    -ShouldFail $true

Test-Endpoint -Name "Test 6.5: Missing member_id" `
    -Url "$baseUrl/get_data" `
    -Body @{} `
    -ShouldFail $true

Write-Host "`n=== CATEGORY 7: Boundary Values ===" -ForegroundColor Yellow

Test-Endpoint -Name "Test 7.1: Minimum valid FICO (300)" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=300; annual_inc=1} `
    -ShouldFail $false

Test-Endpoint -Name "Test 7.2: Maximum valid FICO (850)" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=850; annual_inc=1} `
    -ShouldFail $false

Test-Endpoint -Name "Test 7.3: Risk score exactly 30 (boundary)" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{loan_amnt=10000; risk_score=30} `
    -ShouldFail $false

Test-Endpoint -Name "Test 7.4: Risk score exactly 60 (boundary)" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{loan_amnt=10000; risk_score=60} `
    -ShouldFail $false

Test-Endpoint -Name "Test 7.5: Risk score 0 (minimum)" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{loan_amnt=15000; risk_score=0} `
    -ShouldFail $false

Test-Endpoint -Name "Test 7.6: Risk score 100 (maximum)" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{loan_amnt=15000; risk_score=100} `
    -ShouldFail $false

Write-Host "`n=== CATEGORY 8: Extreme Values ===" -ForegroundColor Yellow

Test-Endpoint -Name "Test 8.1: Extremely high income (10 billion)" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=600; annual_inc=10000000000} `
    -ShouldFail $false

Test-Endpoint -Name "Test 8.2: Extremely large loan (1 billion)" `
    -Url "$baseUrl/calc_ecl" `
    -Body @{loan_amnt=1000000000; risk_score=60} `
    -ShouldFail $false

Test-Endpoint -Name "Test 8.3: Income = 1 dollar" `
    -Url "$baseUrl/risk_score" `
    -Body @{fico_range_high=300; annual_inc=1} `
    -ShouldFail $false

Write-Host "`n=== CATEGORY 9: Valid Member Tests ===" -ForegroundColor Yellow

Test-Endpoint -Name "Test 9.1: Valid low-risk member (63044350)" `
    -Url "$baseUrl/get_data" `
    -Body @{member_id=63044350} `
    -ShouldFail $false

Test-Endpoint -Name "Test 9.2: Valid high-risk member (-76653)" `
    -Url "$baseUrl/get_data" `
    -Body @{member_id=-76653} `
    -ShouldFail $false

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "TEST SUMMARY" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "✅ Tests Passed: $testsPassed" -ForegroundColor Green
Write-Host "❌ Tests Failed: $testsFailed" -ForegroundColor Red
Write-Host "Total Tests: $($testsPassed + $testsFailed)" -ForegroundColor White

if ($testsFailed -eq 0) {
    Write-Host "`n🎉 ALL TESTS PASSED! Your API has robust error handling." -ForegroundColor Green
} else {
    Write-Host "`n⚠️  Some tests failed. Review the errors above." -ForegroundColor Yellow
}

Write-Host "`n========================================`n" -ForegroundColor Magenta
