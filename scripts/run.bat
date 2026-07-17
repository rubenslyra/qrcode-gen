@echo off
chcp 65001 >nul
title Gerador QR Code

set "ROOT=%~dp0.."
set "PYTHON=python"

"%PYTHON%" -c "import qrcode, PIL" 2>nul
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    "%PYTHON%" -m pip install qrcode[pil] pillow
)

cls
echo.
echo   ______ ___   ___ ____      _    ___   ____
echo  / __  // _ \ / _ / _  |    / \  | _ \ / ___|
echo / / / // // /// // __||   / _ \ |   /| |  _
echo \ \/ // ___// __\__ \| |_/ ___ \| |\ \| |_| |
echo  \__//_/   \___/___/ \___/_/   \_\_| \_\\____|
echo.
echo         Gerador de QR Code — Rubinho Lyra
echo.
echo     Produzido por Rubinho Lyra (@rubinholyra)
echo.
"%PYTHON%" "%ROOT%\src\qrcode_gen.py"
if %errorlevel% neq 0 (
    echo.
    echo Pressione qualquer tecla para sair...
    pause >nul
)
