param(
    [Parameter(Mandatory = $true)]
    [string]$OvaPath,

    [string]$OutputDirectory
)

$ErrorActionPreference = "Stop"
$ova = Get-Item -LiteralPath $OvaPath

if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $ova.DirectoryName "release-assets"
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null

$ovaHash = (Get-FileHash -LiteralPath $ova.FullName -Algorithm SHA256).Hash.ToLower()
$ovaHashFile = Join-Path $OutputDirectory ($ova.Name + ".sha256")
"$ovaHash  $($ova.Name)" | Set-Content -LiteralPath $ovaHashFile -Encoding ascii

$partLimit = 1900MB
Write-Host "OVA: $($ova.FullName)"
Write-Host "Tamanho: $($ova.Length) bytes"
Write-Host "SHA-256: $ovaHash"

if ($ova.Length -lt $partLimit) {
    Write-Host "A OVA cabe em um único ativo de Release."
    Write-Host "Envie a OVA original e $ovaHashFile"
    exit 0
}

$sevenZip = Get-Command "7z.exe" -ErrorAction SilentlyContinue
if (-not $sevenZip) {
    $defaultSevenZip = "C:\Program Files\7-Zip\7z.exe"
    if (Test-Path -LiteralPath $defaultSevenZip) {
        $sevenZipPath = $defaultSevenZip
    } else {
        throw "7-Zip não encontrado. Instale-o ou informe 7z.exe no PATH."
    }
} else {
    $sevenZipPath = $sevenZip.Source
}

$baseName = [System.IO.Path]::GetFileNameWithoutExtension($ova.Name)
$archivePath = Join-Path $OutputDirectory ($baseName + ".7z")

& $sevenZipPath a -t7z -mx=0 -v1900m $archivePath $ova.FullName
if ($LASTEXITCODE -ne 0) {
    throw "O 7-Zip terminou com o código $LASTEXITCODE."
}

$parts = Get-ChildItem -LiteralPath $OutputDirectory -Filter ($baseName + ".7z.*") |
    Where-Object { -not $_.PSIsContainer } |
    Sort-Object Name

$partsHashFile = Join-Path $OutputDirectory ($baseName + ".7z.parts.sha256")
$hashLines = foreach ($part in $parts) {
    $hash = (Get-FileHash -LiteralPath $part.FullName -Algorithm SHA256).Hash.ToLower()
    "$hash  $($part.Name)"
}
$hashLines | Set-Content -LiteralPath $partsHashFile -Encoding ascii

Write-Host "Partes criadas em: $OutputDirectory"
Write-Host "Envie todas as partes, $ovaHashFile e $partsHashFile para a mesma Release."
Write-Host "Para extrair, coloque todas as partes na mesma pasta e abra somente o arquivo .7z.001 com o 7-Zip."
