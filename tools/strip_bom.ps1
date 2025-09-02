# tools\strip_bom.ps1
$folder = "tests\conversations"
$pattern = "*.json"
$files = Get-ChildItem -Path $folder -Filter $pattern -File -Recurse
$removed = 0
foreach ($f in $files) {
  $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
  if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    $new = $bytes[3..($bytes.Length-1)]
    [System.IO.File]::WriteAllBytes($f.FullName, $new)
    Write-Host "Removed BOM -> $($f.FullName)"
    $removed++
  }
}
Write-Host "Done. BOMs removed: $removed"
