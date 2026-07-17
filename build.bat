@echo off
chcp 65001 >nul
title Gerador QR Code - Build

echo === Instalando dependencias ===
pip install -r requirements.txt

echo.
echo === Gerando icone ===
python -c "
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (64, 64), (15, 17, 22))
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([2, 2, 61, 61], radius=10, fill=(200, 144, 50))
draw.text((10, 8), 'QR', fill=(0, 0, 0), font=ImageFont.load_default())
img.save('icon.ico', format='ICO', sizes=[(64, 64)])
print('Icon created.')
"

echo.
echo === Compilando com PyInstaller ===
pyinstaller --onefile --windowed ^
  --icon icon.ico ^
  --add-data "icon.ico;." ^
  --name "QRCodeGenerator" ^
  --noconfirm ^
  --clean ^
  --distpath dist ^
  --workpath build_temp ^
  --specpath . ^
  --version-file version_info.txt ^
  --manifest manifest.xml ^
  qrcode_gen.py

echo.
echo === Limpando ===
if exist "build_temp" rmdir /s /q build_temp
if exist "icon.ico" del icon.ico
if exist "icon.png" del icon.png 2>nul
if exist "QRCodeGenerator.spec" del QRCodeGenerator.spec

echo.
echo === PRONTO! ===
echo Executavel em: dist\QRCodeGenerator.exe
pause
