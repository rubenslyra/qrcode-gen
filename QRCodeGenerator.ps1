$python = "D:\laragon\bin\python\python-3.13\python.exe"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$script = Join-Path $scriptDir "qrcode_gen.py"

try {
    & $python -c "import qrcode, PIL" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Instalando dependencias..." -ForegroundColor Yellow
        & $python -m pip install qrcode[pil] pillow pyinstaller
    }
}
catch {
    Write-Host "Verificando dependencias..." -ForegroundColor Yellow
    & $python -m pip install qrcode[pil] pillow
}

Write-Host ""
Write-Host "  ______ ___   ___ ____      _    ___   ____" -ForegroundColor DarkYellow
Write-Host " / __  // _ \ / _ / _  |    / \  | _ \ / ___|" -ForegroundColor DarkYellow
Write-Host "/ / / // // /// // __||   / _ \ |   /| |  _" -ForegroundColor DarkYellow
Write-Host "\ \/ // ___// __\__ \| |_/ ___ \| |\ \| |_| |" -ForegroundColor DarkYellow
Write-Host " \__//_/   \___/___/ \___/_/   \_\_| \_\\____|" -ForegroundColor DarkYellow
Write-Host ""
Write-Host "        Gerador de QR Code - Rubinho Lyra" -ForegroundColor DarkYellow
Write-Host ""
Write-Host "    Produzido por Rubinho Lyra (@rubinholyra)" -ForegroundColor DarkYellow
Write-Host ""

& $python $script

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Pressione qualquer tecla para sair..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
