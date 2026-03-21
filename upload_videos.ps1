$files = Get-ChildItem -Filter *.mp4
foreach ($file in $files) {
    Write-Host "Uploading $($file.Name)..."
    git add $file.Name
    git commit -m "Upload $($file.Name)"
    $retry = 0
    $success = $false
    while (-not $success -and $retry -lt 3) {
        git push origin master --force
        if ($LASTEXITCODE -eq 0) {
            $success = $true
            Write-Host "Successfully pushed $($file.Name)"
        } else {
            $retry++
            Write-Host "Push failed for $($file.Name). Retrying ($retry/3)..."
            Start-Sleep -Seconds 5
        }
    }
}
git add .
git commit -m "Upload remaining files"
git push origin master --force
Write-Host "All done!"
