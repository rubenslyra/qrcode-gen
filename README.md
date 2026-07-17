# QR Code Generator

![screenshot](screenshot_app.png)

<p align="center">
  <img src="https://img.shields.io/badge/python-3.13+-3776AB?style=flat&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/license-GPLv3-blue?style=flat">
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20linux-lightgrey?style=flat">
  <img src="https://img.shields.io/github/v/release/rubenslyra/qrcode-gen?style=flat">
  <img src="https://img.shields.io/badge/made%20by-Rubinho%20Lyra-ff69b4?style=flat">
</p>

**Produzido por [Rubinho Lyra](https://github.com/rubenslyra)**  
YouTube / TikTok / Instagram: **@rubinholyra**

---

Crie QR Codes estilizados com interface gráfica moderna em Python/Tkinter.

### Funcionalidades

- Geração de QR Codes a partir de texto ou URL
- 6 estilos de módulos: Quadrado, Círculo, Arredondado, Barras, etc.
- Cores personalizáveis (QR Code e fundo)
- Gradientes experimental (Radial, Horizontal, Vertical, Quadrado)
- Preview ao vivo
- Exportação para PNG, JPEG e BMP

### Download

Baixe a versão mais recente na [página de releases](https://github.com/rubenslyra/qrcode-gen/releases).

| Plataforma | Arquivo |
|-----------|---------|
| Windows | `QRCodeGenerator.exe` |
| Linux | `QRCodeGenerator` (ELF 64-bit) |

### Como usar (dev)

```bash
pip install -r requirements.txt
python src/qrcode_gen.py
```

Ou use os scripts em `scripts/`:

```bash
scripts\run.bat      # Windows
scripts/run.ps1      # PowerShell
```

### Build

**Windows:**
```bash
scripts\build_windows.bat
```

**Linux:**
```bash
chmod +x scripts/build_linux.sh
./scripts/build_linux.sh
```

Gera executável único em `dist/`.
