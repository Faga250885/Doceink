# Rebuild the Windows installer; this script never flashes a device.
param([string]$FirmwareZip)
$ErrorActionPreference='Stop'
$project=Split-Path -Parent $PSScriptRoot
$version='0.75.147'
$payload=Join-Path $PSScriptRoot 'payload'
$venv=Join-Path $PSScriptRoot '.venv'
Push-Location -LiteralPath $project
try {
    if(-not(Test-Path -LiteralPath $venv)) { py -m venv $venv; if($LASTEXITCODE -ne 0){throw 'Could not create environment'} }
    $python=Join-Path $venv 'Scripts/python.exe'
    & $python -m pip install -r (Join-Path $PSScriptRoot 'requirements-lock.txt')
    if($LASTEXITCODE -ne 0){throw 'Dependency installation failed'}
    if(-not $FirmwareZip){
        $FirmwareZip=Join-Path $PSScriptRoot "Metalio-$version-instalacion-limpia.zip"
        Invoke-WebRequest -Uri "https://github.com/Faga250885/Doceink/releases/download/v$version/Metalio-$version-instalacion-limpia.zip" -OutFile $FirmwareZip
    }
    New-Item -ItemType Directory -Path $payload -Force | Out-Null
    Expand-Archive -LiteralPath $FirmwareZip -DestinationPath $payload -Force
    Copy-Item -LiteralPath (Join-Path $project 'assets/doceink-symbol.png') -Destination $payload
    & $python (Join-Path $PSScriptRoot 'prepare_notices.py')
    if($LASTEXITCODE -ne 0){throw 'License preparation failed'}
    & $python (Join-Path $PSScriptRoot 'test_installer.py')
    if($LASTEXITCODE -ne 0){throw 'Installer tests failed'}
    & $python -m PyInstaller --noconfirm --clean --onefile --windowed --name "DoceInk-Setup-$version" --icon (Join-Path $project 'assets/doceink.ico') --add-data "$payload;payload" --collect-all esptool --copy-metadata esptool --distpath (Join-Path $PSScriptRoot 'dist') --workpath (Join-Path $PSScriptRoot 'build') --specpath $PSScriptRoot (Join-Path $PSScriptRoot 'app.py')
    if($LASTEXITCODE -ne 0){throw 'Packaging failed'}
} finally { Pop-Location }
