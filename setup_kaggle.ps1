# Kaggle Setup Script
# Run this after you've updated kaggle.json with your username

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "KAGGLE API SETUP VERIFICATION" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if kaggle.json exists
$kaggleJsonPath = "C:\Users\puppy\.kaggle\kaggle.json"

if (Test-Path $kaggleJsonPath) {
    Write-Host "kaggle.json found at: $kaggleJsonPath" -ForegroundColor Green
    
    # Read and display (masked)
    $content = Get-Content $kaggleJsonPath | ConvertFrom-Json
    Write-Host "  Username: $($content.username)" -ForegroundColor Yellow
    Write-Host "  Key: $($content.key.Substring(0,10))..." -ForegroundColor Yellow
    
    if ($content.username -eq "YOUR_KAGGLE_USERNAME") {
        Write-Host ""
        Write-Host "WARNING: You need to update your Kaggle username!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Instructions:" -ForegroundColor Yellow
        Write-Host "1. Go to https://www.kaggle.com/account" -ForegroundColor White
        Write-Host "2. Your username is at the top" -ForegroundColor White
        Write-Host "3. Edit C:\Users\puppy\.kaggle\kaggle.json" -ForegroundColor White
        Write-Host "4. Replace YOUR_KAGGLE_USERNAME with your actual username" -ForegroundColor White
        Write-Host "5. Save the file" -ForegroundColor White
        Write-Host ""
        
        # Open in notepad
        Write-Host "Opening kaggle.json in Notepad..." -ForegroundColor Cyan
        notepad $kaggleJsonPath
        exit 1
    }
    
}
else {
    Write-Host "kaggle.json not found!" -ForegroundColor Red
    Write-Host "Creating template at: $kaggleJsonPath" -ForegroundColor Yellow
    
    $kaggleDir = Split-Path $kaggleJsonPath
    if (!(Test-Path $kaggleDir)) {
        New-Item -ItemType Directory -Path $kaggleDir -Force | Out-Null
    }
    
    $jsonContent = @"
{
  "username": "YOUR_KAGGLE_USERNAME",
  "key": "KGAT_824fefd4e35f940e05c92a3f2398bc90"
}
"@
    
    $jsonContent | Out-File -FilePath $kaggleJsonPath -Encoding UTF8
    Write-Host "Template created. Opening in Notepad..." -ForegroundColor Green
    notepad $kaggleJsonPath
    exit 1
}

Write-Host ""
Write-Host "Testing Kaggle API connection..." -ForegroundColor Cyan

try {
    # Test Kaggle API
    kaggle datasets list --max-size 1 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Kaggle API is working!" -ForegroundColor Green
        Write-Host ""
        Write-Host "==================================================" -ForegroundColor Green
        Write-Host "READY TO DOWNLOAD DATASETS!" -ForegroundColor Green
        Write-Host "==================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Run: python load_kaggle_data.py" -ForegroundColor White
        Write-Host "   OR" -ForegroundColor White
        Write-Host "2. Run: kaggle datasets download -d wordsforthewise/lending-club" -ForegroundColor White
        Write-Host ""
    }
    else {
        Write-Host "Kaggle API test failed" -ForegroundColor Red
        Write-Host "Make sure your username is correct in kaggle.json" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "Error testing Kaggle API" -ForegroundColor Red
}
