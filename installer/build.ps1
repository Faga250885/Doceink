# Rebuild the Windows installer; this script never flashes a device.
$ErrorActionPreference='Stop'
$project=Split-Path -Parent $PSScriptRoot
$version='0.75.149.1'
$payload=Join-Path $PSScriptRoot 'payload'
$venv=Join-Path $PSScriptRoot '.venv'
Push-Location -LiteralPath $project
try {
    if(-not(Test-Path -LiteralPath $venv)) { py -m venv $venv; if($LASTEXITCODE -ne 0){throw 'Could not create environment'} }
    $python=Join-Path $venv 'Scripts/python.exe'
    & $python -m pip install -r (Join-Path $PSScriptRoot 'requirements-lock.txt')
    if($LASTEXITCODE -ne 0){throw 'Dependency installation failed'}
    New-Item -ItemType Directory -Path $payload -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $project 'assets/doceink-symbol.png') -Destination $payload
    & $python (Join-Path $PSScriptRoot 'prepare_notices.py')
    if($LASTEXITCODE -ne 0){throw 'License preparation failed'}
    & $python (Join-Path $PSScriptRoot 'test_installer.py')
    if($LASTEXITCODE -ne 0){throw 'Installer tests failed'}
    & $python (Join-Path $PSScriptRoot 'test_download.py')
    if($LASTEXITCODE -ne 0){throw 'Download tests failed'}
    # Only static artwork and license notices are bundled. Firmware is fetched at install time.
    & $python -m PyInstaller --noconfirm --clean --onefile --noupx --windowed --name "DoceInk-Setup-$version" --icon (Join-Path $project 'assets/doceink.ico') --add-data "$(Join-Path $payload 'doceink-symbol.png');payload" --add-data "$(Join-Path $payload 'THIRD-PARTY.txt');payload" --collect-all esptool --copy-metadata esptool --distpath (Join-Path $PSScriptRoot 'dist') --workpath (Join-Path $PSScriptRoot 'build') --specpath $PSScriptRoot (Join-Path $PSScriptRoot 'app.py')
    if($LASTEXITCODE -ne 0){throw 'Packaging failed'}
} finally { Pop-Location }
