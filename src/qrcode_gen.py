import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer,
    RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    SolidFillColorMask, RadialGradiantColorMask, SquareGradiantColorMask,
    HorizontalGradiantColorMask, VerticalGradiantColorMask
)
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter
import os, sys, io, math


BG = "#0f1116"
FG = "#efe9db"
CARD = "#14181f"
CARD2 = "#191f28"
MUTED = "#a8a090"
PRIMARY = "#c89032"
PRIMARY_GLOW = "#e8b84c"
ACCENT_DEEP = "#263e66"
ACCENT_BURGUNDY = "#6f3540"
ACCENT_WARM = "#d47238"
BORDER = "#232a36"
INPUT_BG = "#1b212a"
RADIUS = 12
FONT_FAMILY = "Segoe UI"
FONT_HEADING = "Segoe UI"


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def _rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


def _lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


STYLES = {
    "Quadrado": SquareModuleDrawer,
    "Quadrado c/ Gap": GappedSquareModuleDrawer,
    "C\u00edrculo": CircleModuleDrawer,
    "Arredondado": RoundedModuleDrawer,
    "Barras Verticais": VerticalBarsDrawer,
    "Barras Horizontais": HorizontalBarsDrawer,
}


def _apply_theme():
    style = ttk.Style()
    style.theme_use("clam")
    bg = BG
    fg = FG
    select_bg = PRIMARY
    select_fg = "#000000"
    style.configure(".", background=bg, foreground=fg, font=(FONT_FAMILY, 10))
    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=fg, font=(FONT_FAMILY, 10))
    style.configure("TEntry",
        fieldbackground=INPUT_BG, foreground=fg, insertcolor=fg,
        borderwidth=0, focuscolor=PRIMARY, padding=(12, 10, 12, 10),
        font=(FONT_FAMILY, 10))
    style.map("TEntry",
        fieldbackground=[("focus", CARD2)],
        bordercolor=[("focus", PRIMARY)])
    style.configure("TCombobox",
        fieldbackground=INPUT_BG, foreground=fg, arrowcolor=PRIMARY,
        selectbackground=INPUT_BG, selectforeground=fg,
        borderwidth=0, padding=(10, 8, 10, 8), font=(FONT_FAMILY, 10))
    style.map("TCombobox",
        fieldbackground=[("readonly", INPUT_BG)],
        selectbackground=[("readonly", INPUT_BG)],
        selectforeground=[("readonly", fg)])
    style.configure("TSpinbox",
        fieldbackground=INPUT_BG, foreground=fg, arrowcolor=PRIMARY,
        borderwidth=0, padding=(8, 6, 8, 6), font=(FONT_FAMILY, 10))
    style.map("TSpinbox",
        fieldbackground=[("focus", CARD2)])

    style.configure("Card.TFrame", background=CARD, relief="flat", borderwidth=1)
    style.configure("Header.TLabel", font=(FONT_HEADING, 18, "bold"), foreground=PRIMARY, background=BG)
    style.configure("Subtitle.TLabel", font=(FONT_FAMILY, 9), foreground=MUTED)
    style.configure("Status.TLabel", font=(FONT_FAMILY, 8), foreground=MUTED)
    style.configure("Section.TLabelframe", background=BG, foreground=PRIMARY, font=(FONT_FAMILY, 9, "bold"), borderwidth=0)
    style.configure("Section.TLabelframe.Label", background=BG, foreground=PRIMARY, font=(FONT_FAMILY, 9, "bold"))

    style.configure("Gold.Horizontal.TProgressbar", background=PRIMARY, troughcolor=INPUT_BG, borderwidth=0, thickness=3)

    style.configure("TButton",
        background=PRIMARY, foreground="#000000", font=(FONT_FAMILY, 10, "bold"),
        borderwidth=0, padding=(16, 10, 16, 10))
    style.map("TButton",
        background=[("active", PRIMARY_GLOW), ("disabled", "#3a3a3a")],
        foreground=[("disabled", "#666666")])

    style.configure("Secondary.TButton",
        background=CARD2, foreground=FG, font=(FONT_FAMILY, 10),
        borderwidth=1, bordercolor=BORDER, padding=(14, 9, 14, 9))
    style.map("Secondary.TButton",
        background=[("active", BORDER)],
        bordercolor=[("active", PRIMARY)])

    style.configure("Danger.TButton",
        background=ACCENT_BURGUNDY, foreground=FG, font=(FONT_FAMILY, 10),
        borderwidth=0, padding=(14, 9, 14, 9))
    style.map("Danger.TButton",
        background=[("active", "#8a4250")])

    style.configure("TMenubutton", background=INPUT_BG, foreground=fg, font=(FONT_FAMILY, 10))

    style.layout("TButton", [
        ("Button.button", {"children": [("Button.focus", {"children": [("Button.padding",
            {"children": [("Button.label", {"sticky": "nswe"})]})]})]})])

    return style


def _round_rect(canvas, x1, y1, x2, y2, r=12, **kwargs):
    points = []
    points.extend([x1+r, y1, x2-r, y1])
    points.extend([x2-r, y1, x2, y1, x2, y1+r])
    points.extend([x2, y2-r, x2, y2, x2-r, y2])
    points.extend([x1+r, y2, x1, y2, x1, y2-r])
    points.extend([x1, y1+r, x1, y1, x1+r, y1])
    return canvas.create_polygon(points, smooth=True, **kwargs)


class GradientButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=180, height=38, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0, bg=BG)
        self.command = command
        self.text = text
        self.btn_w = width
        self.btn_h = height
        self.disabled = False
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)
        self._draw_idle()

    def _draw_idle(self, hover=False, press=False):
        self.delete("all")
        x, y, w, h = 0, 0, self.btn_w, self.btn_h
        r = RADIUS
        if self.disabled:
            fill = "#2a2a2a"
        elif press:
            fill = "#b07a28"
        elif hover:
            fill = PRIMARY_GLOW
        else:
            fill = PRIMARY
        _round_rect(self, x+1, y+1, w-1, h-1, r, fill=fill, outline="")
        offset = 1 if press else 0
        self.create_text(w//2, h//2 + offset, text=self.text,
            fill="#000000", font=(FONT_FAMILY, 10, "bold"), anchor="center")

    def _on_enter(self, e):
        if not self.disabled:
            self._draw_idle(hover=True)

    def _on_leave(self, e):
        if not self.disabled:
            self._draw_idle()

    def _on_click(self, e):
        if not self.disabled and self.command:
            self._draw_idle(press=True)

    def _on_release(self, e):
        if not self.disabled:
            self._draw_idle(hover=True)
            if self.command:
                self.command()

    def set_state(self, state):
        self.disabled = state == "disabled"
        self._draw_idle()


class ColorSwatch(tk.Canvas):
    def __init__(self, parent, color="#000000", command=None, size=32, **kwargs):
        super().__init__(parent, width=size, height=size, highlightthickness=0, bd=0, bg=BG)
        self.color = color
        self.command = command
        self.s = size
        self.bind("<Button-1>", lambda e: command() if command else None)
        self._draw()

    def _draw(self):
        self.delete("all")
        s = self.s
        r = 6
        offset = 1
        _round_rect(self, offset, offset, s-offset, s-offset, r, fill=self.color, outline=BORDER, width=1)

    def set_color(self, color):
        self.color = color
        self._draw()


class ColorButton(tk.Frame):
    def __init__(self, parent, label="Cor", color="#000000", command=None, **kwargs):
        super().__init__(parent, bg=BG, **kwargs)
        self.color = color
        self.command = command
        self.label_text = label
        self.swatch = ColorSwatch(self, color=color, command=command, size=28)
        self.swatch.pack(side=tk.LEFT, padx=(0, 6))
        self.label = tk.Label(self, text=label, bg=BG, fg=MUTED, font=(FONT_FAMILY, 9))
        self.label.pack(side=tk.LEFT)

    def set_color(self, color):
        self.color = color
        self.swatch.set_color(color)

    def get_color(self):
        return self.color


class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de QR Code — Rubinho Lyra")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.root.producer = "Rubinho Lyra"

        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass

        self.fg_color = "#c89032"
        self.bg_color = "#0f1116"
        self.preview_photo = None
        self.last_qr_pil = None
        self.last_text = ""
        self.gradient_mode = tk.StringVar(value="none")
        self.gradient_from = "#c89032"
        self.gradient_to = "#d47238"

        _apply_theme()

        self.root.option_add("*Dialog.msg.font", (FONT_FAMILY, 10))
        self.root.option_add("*Dialog.btn.font", (FONT_FAMILY, 10))

        self._build_ui()

    def _build_ui(self):
        container = tk.Frame(self.root, bg=BG)
        container.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(container, bg=BG, height=72)
        header.pack(fill=tk.X, padx=28, pady=(24, 0))
        header.pack_propagate(False)

        title_canvas = tk.Canvas(header, bg=BG, highlightthickness=0, bd=0, height=40)
        title_canvas.pack(fill=tk.X)
        title_canvas.create_text(0, 18, text="QR Code Generator",
            fill=PRIMARY, font=(FONT_HEADING, 22, "bold"), anchor="w", tags="title")
        subtitle_text = "Crie QR Codes estilizados com a paleta Rubinho Lyra"
        title_canvas.create_text(0, 44, text=subtitle_text,
            fill=MUTED, font=(FONT_FAMILY, 9), anchor="w", tags="sub")

        producer_text = "Produzido por Rubinho Lyra — @rubinholyra"
        title_canvas.create_text(500, 18, text=producer_text,
            fill=MUTED, font=(FONT_FAMILY, 8), anchor="e", tags="prod")

        sep = tk.Frame(container, bg=BORDER, height=1)
        sep.pack(fill=tk.X, padx=28, pady=(18, 0))

        content = tk.Frame(container, bg=BG)
        content.pack(fill=tk.BOTH, expand=True, padx=28, pady=(16, 20))

        left = tk.Frame(content, bg=BG)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 16))

        right = tk.Frame(content, bg=BG, width=310)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)

        self._build_input_section(left)
        self._build_style_section(left)
        self._build_color_section(left)
        self._build_gradient_section(left)
        self._build_preview_section(right)

        self.status_var = tk.StringVar(value="Pronto. Insira um texto e clique em Gerar.")
        status_frame = tk.Frame(container, bg=BG)
        status_frame.pack(fill=tk.X, padx=28, pady=(0, 10))

        status_bar = tk.Label(status_frame, textvariable=self.status_var,
            bg=BG, fg=MUTED, font=(FONT_FAMILY, 8), anchor="w")
        status_bar.pack(side=tk.LEFT)

        producer_label = tk.Label(status_frame,
            text="Rubinho Lyra © 2026 — @rubinholyra (YouTube, TikTok, Instagram)",
            bg=BG, fg="#5a5a5a", font=(FONT_FAMILY, 7), anchor="e")
        producer_label.pack(side=tk.RIGHT, fill=tk.X, expand=True)

    def _build_input_section(self, parent):
        card = tk.Frame(parent, bg=CARD, bd=0, highlightthickness=1, highlightcolor=BORDER, highlightbackground=BORDER)
        card.pack(fill=tk.X, pady=(0, 12))

        inner = tk.Frame(card, bg=CARD, padx=16, pady=14)
        inner.pack(fill=tk.X)

        tk.Label(inner, text="Texto / URL", bg=CARD, fg=PRIMARY,
            font=(FONT_FAMILY, 10, "bold")).pack(anchor="w")
        tk.Label(inner, text="O que voc\u00ea deseja codificar?", bg=CARD, fg=MUTED,
            font=(FONT_FAMILY, 9)).pack(anchor="w", pady=(2, 8))

        entry_frame = tk.Frame(inner, bg=CARD)
        entry_frame.pack(fill=tk.X)

        self.entry_text = tk.Text(entry_frame, height=2, wrap="word",
            bg=INPUT_BG, fg=FG, insertbackground=PRIMARY,
            font=(FONT_FAMILY, 11), bd=0, padx=14, pady=12,
            highlightthickness=1, highlightcolor=BORDER, highlightbackground=BORDER,
            relief="flat", selectbackground=PRIMARY, selectforeground="#000000")
        self.entry_text.pack(fill=tk.X)
        self.entry_text.bind("<Control-Return>", lambda e: self.generate())

        self.entry_text.insert("1.0", "")

        btn_row = tk.Frame(inner, bg=CARD)
        btn_row.pack(fill=tk.X, pady=(12, 0))

        self.btn_generate = GradientButton(btn_row, text="\u26a1 Gerar QR Code",
            command=self.generate, width=180, height=38)
        self.btn_generate.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_save = GradientButton(btn_row, text="\u2b07 Salvar PNG",
            command=self.save, width=140, height=38)
        self.btn_save.set_state("disabled")
        self.btn_save.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_clear = tk.Button(btn_row, text="\u2716 Limpar",
            command=self.clear, bg=CARD2, fg=MUTED,
            font=(FONT_FAMILY, 9), bd=0, padx=14, pady=0,
            activebackground=BORDER, activeforeground=FG, cursor="hand2",
            highlightthickness=0, relief="flat")
        self.btn_clear.pack(side=tk.LEFT)

    def _build_style_section(self, parent):
        card = tk.Frame(parent, bg=CARD, bd=0, highlightthickness=1, highlightcolor=BORDER, highlightbackground=BORDER)
        card.pack(fill=tk.X, pady=(0, 12))

        inner = tk.Frame(card, bg=CARD, padx=16, pady=14)
        inner.pack(fill=tk.X)

        tk.Label(inner, text="Estilo dos M\u00f3dulos", bg=CARD, fg=PRIMARY,
            font=(FONT_FAMILY, 10, "bold")).pack(anchor="w")
        tk.Label(inner, text="Forma dos pontos do QR Code", bg=CARD, fg=MUTED,
            font=(FONT_FAMILY, 9)).pack(anchor="w", pady=(2, 8))

        row = tk.Frame(inner, bg=CARD)
        row.pack(fill=tk.X)

        self.style_combo = ttk.Combobox(row, values=list(STYLES.keys()),
            state="readonly", width=26)
        self.style_combo.pack(side=tk.LEFT, padx=(0, 12))
        self.style_combo.current(0)

        size_frame = tk.Frame(row, bg=CARD)
        size_frame.pack(side=tk.LEFT, padx=(0, 12))
        tk.Label(size_frame, text="Tam:", bg=CARD, fg=MUTED,
            font=(FONT_FAMILY, 9)).pack(side=tk.LEFT, padx=(0, 4))
        self.size_var = tk.IntVar(value=10)
        size_spin = ttk.Spinbox(size_frame, from_=1, to=40,
            textvariable=self.size_var, width=5)
        size_spin.pack(side=tk.LEFT)

        border_frame = tk.Frame(row, bg=CARD)
        border_frame.pack(side=tk.LEFT)
        tk.Label(border_frame, text="Borda:", bg=CARD, fg=MUTED,
            font=(FONT_FAMILY, 9)).pack(side=tk.LEFT, padx=(0, 4))
        self.border_var = tk.IntVar(value=4)
        border_spin = ttk.Spinbox(border_frame, from_=0, to=10,
            textvariable=self.border_var, width=5)
        border_spin.pack(side=tk.LEFT)

    def _build_color_section(self, parent):
        card = tk.Frame(parent, bg=CARD, bd=0, highlightthickness=1, highlightcolor=BORDER, highlightbackground=BORDER)
        card.pack(fill=tk.X, pady=(0, 12))

        inner = tk.Frame(card, bg=CARD, padx=16, pady=14)
        inner.pack(fill=tk.X)

        tk.Label(inner, text="Cores", bg=CARD, fg=PRIMARY,
            font=(FONT_FAMILY, 10, "bold")).pack(anchor="w")
        tk.Label(inner, text="Personalize as cores do seu QR Code", bg=CARD, fg=MUTED,
            font=(FONT_FAMILY, 9)).pack(anchor="w", pady=(2, 8))

        row = tk.Frame(inner, bg=CARD)
        row.pack(fill=tk.X)

        self.fg_btn = ColorButton(row, label="QR Code", color=self.fg_color,
            command=self.choose_fg_color)
        self.fg_btn.pack(side=tk.LEFT, padx=(0, 24))

        self.bg_btn = ColorButton(row, label="Fundo", color=self.bg_color,
            command=self.choose_bg_color)
        self.bg_btn.pack(side=tk.LEFT)

    def _build_gradient_section(self, parent):
        card = tk.Frame(parent, bg=CARD, bd=0, highlightthickness=1, highlightcolor=BORDER, highlightbackground=BORDER)
        card.pack(fill=tk.X, pady=(0, 12))

        inner = tk.Frame(card, bg=CARD, padx=16, pady=14)
        inner.pack(fill=tk.X)

        tk.Label(inner, text="Gradiente (Experimental)", bg=CARD, fg=PRIMARY,
            font=(FONT_FAMILY, 10, "bold")).pack(anchor="w")
        tk.Label(inner, text="Preenchimento degrad\u00ea entre duas cores", bg=CARD, fg=MUTED,
            font=(FONT_FAMILY, 9)).pack(anchor="w", pady=(2, 8))

        row = tk.Frame(inner, bg=CARD)
        row.pack(fill=tk.X)

        self.grad_combo = ttk.Combobox(row, textvariable=self.gradient_mode,
            values=["none", "Radial", "Horizontal", "Vertical", "Quadrado"],
            state="readonly", width=16)
        self.grad_combo.pack(side=tk.LEFT, padx=(0, 12))
        self.grad_combo.bind("<<ComboboxSelected>>", self._on_grad_change)
        self.grad_combo.current(0)

        self.grad_from_btn = ColorButton(row, label="De", color=self.gradient_from,
            command=self.choose_grad_from)
        self.grad_from_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.grad_to_btn = ColorButton(row, label="At\u00e9", color=self.gradient_to,
            command=self.choose_grad_to)
        self.grad_to_btn.pack(side=tk.LEFT)

        self._set_grad_enabled(False)

    def _set_grad_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        self.grad_from_btn.label.config(fg=MUTED if not enabled else FG)
        self.grad_to_btn.label.config(fg=MUTED if not enabled else FG)

    def _on_grad_change(self, e=None):
        self._set_grad_enabled(self.gradient_mode.get() != "none")

    def choose_fg_color(self):
        color = colorchooser.askcolor(title="Cor do QR Code",
            initialcolor=self.fg_color)
        if color and color[1]:
            self.fg_color = color[1]
            self.fg_btn.set_color(self.fg_color)

    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Cor do Fundo",
            initialcolor=self.bg_color)
        if color and color[1]:
            self.bg_color = color[1]
            self.bg_btn.set_color(self.bg_color)

    def choose_grad_from(self):
        color = colorchooser.askcolor(title="Cor inicial do gradiente",
            initialcolor=self.gradient_from)
        if color and color[1]:
            self.gradient_from = color[1]
            self.grad_from_btn.set_color(self.gradient_from)

    def choose_grad_to(self):
        color = colorchooser.askcolor(title="Cor final do gradiente",
            initialcolor=self.gradient_to)
        if color and color[1]:
            self.gradient_to = color[1]
            self.grad_to_btn.set_color(self.gradient_to)

    def _draw_grid_bg(self):
        c = self.preview_canvas
        c.delete("grid")
        cw = int(c.cget("width"))
        ch = int(c.cget("height"))
        grid_color = "#1a1f28"
        step = 28
        for x in range(0, cw, step):
            c.create_line(x, 0, x, ch, fill=grid_color, width=1, tags="grid")
        for y in range(0, ch, step):
            c.create_line(0, y, cw, y, fill=grid_color, width=1, tags="grid")

    def _build_preview_section(self, parent):
        card = tk.Frame(parent, bg=CARD, bd=0, highlightthickness=1,
            highlightcolor=BORDER, highlightbackground=BORDER)
        card.pack(fill=tk.BOTH, expand=True)

        inner = tk.Frame(card, bg=CARD, padx=16, pady=14)
        inner.pack(fill=tk.BOTH, expand=True)

        tk.Label(inner, text="Preview", bg=CARD, fg=PRIMARY,
            font=(FONT_FAMILY, 10, "bold")).pack(anchor="w")
        tk.Label(inner, text="Visualiza\u00e7\u00e3o ao vivo", bg=CARD, fg=MUTED,
            font=(FONT_FAMILY, 9)).pack(anchor="w", pady=(2, 8))

        preview_bg = "#0a0c0f"
        pframe = tk.Frame(inner, bg=preview_bg, bd=0, highlightthickness=0)
        pframe.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        w, h = 280, 280
        self.preview_canvas = tk.Canvas(pframe, bg=preview_bg, bd=0,
            highlightthickness=0, width=w, height=h)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)

        self._draw_grid_bg()

        mid_x, mid_y = w//2, h//2
        self.preview_img_label = tk.Label(self.preview_canvas, bg=preview_bg, bd=0)
        self.preview_img_label.place(x=mid_x, y=mid_y, anchor="center")

        self.preview_info = tk.Label(inner, text="Clique em Gerar para criar seu QR Code",
            bg=CARD, fg=MUTED, font=(FONT_FAMILY, 9), wraplength=260)
        self.preview_info.pack(anchor="w")

    def _make_color_mask(self):
        grad = self.gradient_mode.get()
        bg_rgb = _hex_to_rgb(self.bg_color)
        if grad == "none":
            fg_rgb = _hex_to_rgb(self.fg_color)
            return SolidFillColorMask(back_color=bg_rgb, front_color=fg_rgb), False
        f1 = _hex_to_rgb(self.gradient_from)
        f2 = _hex_to_rgb(self.gradient_to)
        if grad == "Radial":
            return RadialGradiantColorMask(back_color=bg_rgb, center_color=f1, edge_color=f2), True
        elif grad == "Horizontal":
            return HorizontalGradiantColorMask(back_color=bg_rgb, left_color=f1, right_color=f2), True
        elif grad == "Vertical":
            return VerticalGradiantColorMask(back_color=bg_rgb, top_color=f1, bottom_color=f2), True
        elif grad == "Quadrado":
            return SquareGradiantColorMask(back_color=bg_rgb, center_color=f1, edge_color=f2), True
        return SolidFillColorMask(back_color=_hex_to_rgb(self.fg_color), front_color=bg_rgb), False

    def generate(self):
        text = self.entry_text.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Aviso", "Digite um texto ou URL primeiro.")
            self.entry_text.focus()
            return

        try:
            self.status_var.set("Gerando QR Code...")
            self.preview_info.config(text="Processando...")
            self.root.update_idletasks()

            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=self.size_var.get(),
                border=self.border_var.get(),
            )
            qr.add_data(text)
            qr.make(fit=True)

            style_name = self.style_combo.get()
            module_drawer_cls = STYLES[style_name]

            color_mask, _ = self._make_color_mask()

            self.last_qr_pil = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=module_drawer_cls(),
                color_mask=color_mask,
            )

            preview = self.last_qr_pil.copy()
            preview.thumbnail((260, 260), Image.LANCZOS)
            self.preview_photo = ImageTk.PhotoImage(preview)
            self.preview_img_label.config(image=self.preview_photo)

            self.preview_info.config(text=f"QR Code gerado! {len(text)} caracteres.")
            self.btn_save.set_state("normal")
            self.last_text = text
            self.status_var.set("QR Code gerado com sucesso.")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar QR Code:\n{e}")
            self.status_var.set("Erro na gera\u00e7\u00e3o.")

    def save(self):
        if self.last_qr_pil is None:
            messagebox.showwarning("Aviso", "Nenhum QR Code foi gerado ainda.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("BMP Image", "*.bmp"),
                ("All Files", "*.*"),
            ],
            title="Salvar QR Code",
        )
        if not file_path:
            return

        try:
            ext = os.path.splitext(file_path)[1].lower()
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=self.size_var.get(),
                border=self.border_var.get(),
            )
            qr.add_data(self.last_text)
            qr.make(fit=True)

            style_name = self.style_combo.get()
            module_drawer_cls = STYLES[style_name]
            color_mask, _ = self._make_color_mask()

            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=module_drawer_cls(),
                color_mask=color_mask,
            )

            save_format = "PNG"
            if ext in (".jpg", ".jpeg"):
                img = img.convert("RGB")
                save_format = "JPEG"
            elif ext == ".bmp":
                save_format = "BMP"

            img.save(file_path, save_format)
            self.status_var.set(f"Salvo: {os.path.basename(file_path)}")
            messagebox.showinfo("Sucesso", f"QR Code salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar:\n{e}")
            self.status_var.set("Erro ao salvar.")

    def clear(self):
        self.entry_text.delete("1.0", "end")
        self.preview_img_label.config(image="")
        self.preview_photo = None
        self.last_qr_pil = None
        self.last_text = ""
        self.btn_save.set_state("disabled")
        self.preview_info.config(text="\u00c1rea limpa. Insira um texto e gere novamente.")
        self.status_var.set("Limpo.")
        self.entry_text.focus()


def main():
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
