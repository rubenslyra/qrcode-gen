#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== Instalando dependencias ==="
pip install --user --break-system-packages -r requirements.txt 2>/dev/null || \
pip install --user -r requirements.txt

echo ""
echo "=== Compilando com PyInstaller ==="
pyinstaller --onefile --windowed \
  --name "QRCodeGenerator" \
  --noconfirm \
  --clean \
  --distpath dist \
  --workpath build_temp \
  --specpath . \
  src/qrcode_gen.py

echo ""
echo "=== Limpando ==="
rm -rf build_temp QRCodeGenerator.spec

echo ""
echo "=== PRONTO! ==="
echo "Executavel em: dist/QRCodeGenerator"
ls -lh dist/QRCodeGenerator
