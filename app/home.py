import tkinter as tk
from tkinter import ttk
from pathlib import Path


# pdf to img
try:
    import fitz  # PyMuPDF
    from PIL import Image, ImageTk
    HAS_PYMUPDF = True
except Exception:
    HAS_PYMUPDF = False


PALETTE = {
    "bg": "#0F1115",
    "panel": "#1A1F29",
    "panel2": "#151923",
    "fg": "#E5E7EB",
    "fg_muted": "#9CA3AF",
    "accent": "#6EAAFF",
    "hover": "#202635",
    "active": "#283046",
}


# viewer pdf
class PdfViewer(ttk.Frame):
    """
    Affiche un PDF
    """
    def __init__(self, parent: tk.Misc, pdf_path: Path):
        super().__init__(parent, style="Panel.TFrame")
        if not HAS_PYMUPDF:
            ttk.Label(
                self,
                text="Affichage PDF indisponible (PyMuPDF non installé).\nInstalle :  pip install pymupdf pillow",
                style="Muted.TLabel",
            ).pack(padx=24, pady=24)
            return

        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path.as_posix())
        self.page_index = 0

        # zoom
        self.zoom = 1.0
        self.auto_fit = True        # ← tant qu'aucun zoom manuel
        self._photo = None
        self._img_id = None

        # Toolbar
        bar = ttk.Frame(self, style="Panel2.TFrame", padding=(8, 6))
        bar.pack(side="top", fill="x")

        self.page_lab = ttk.Label(bar, text=self._page_label_text(), style="Muted.TLabel")
        self.page_lab.pack(side="left", padx=(0, 8))

        ttk.Button(bar, text="←", command=self.prev_page).pack(side="left", padx=4)
        ttk.Button(bar, text="→", command=self.next_page).pack(side="left", padx=2)

        ttk.Button(bar, text="Zoom –", command=self.zoom_out).pack(side="left", padx=12)
        ttk.Button(bar, text="Zoom +", command=self.zoom_in).pack(side="left", padx=4)
        ttk.Button(bar, text="Adapter", command=self.fit_to_area).pack(side="left", padx=12)  # reset auto-fit

        ttk.Button(bar, text="Fermer", style="TButton", command=self.close_viewer).pack(side="right")

        # Zone centrale scrollable
        wrap = ttk.Frame(self)
        wrap.pack(fill="both", expand=True)

        # Scrollbars ttk
        style = ttk.Style(self)
        style.layout("PDF.Vertical.TScrollbar", [
            ("Vertical.Scrollbar.trough", {
                "children": [("Vertical.Scrollbar.thumb", {"expand": 1, "sticky": "nswe"})],
                "sticky": "ns",
            })
        ])
        style.configure("PDF.Vertical.TScrollbar",
                        troughcolor="#181E2A", background="#3B4763",
                        darkcolor="#3B4763", lightcolor="#3B4763",
                        bordercolor="#3B4763", arrowsize=0)
        style.map("PDF.Vertical.TScrollbar",
                  background=[("active", "#4C5A7D"), ("pressed", "#586895")])

        style.layout("PDF.Horizontal.TScrollbar", [
            ("Horizontal.Scrollbar.trough", {
                "children": [("Horizontal.Scrollbar.thumb", {"expand": 1, "sticky": "nswe"})],
                "sticky": "ew",
            })
        ])
        style.configure("PDF.Horizontal.TScrollbar",
                        troughcolor="#181E2A", background="#3B4763",
                        darkcolor="#3B4763", lightcolor="#3B4763",
                        bordercolor="#3B4763", arrowsize=0)
        style.map("PDF.Horizontal.TScrollbar",
                  background=[("active", "#4C5A7D"), ("pressed", "#586895")])

        self.canvas = tk.Canvas(wrap, bg=PALETTE["panel"], highlightthickness=0, bd=0)
        self.vbar = ttk.Scrollbar(wrap, orient="vertical", command=self.canvas.yview, style="PDF.Vertical.TScrollbar")
        self.hbar = ttk.Scrollbar(wrap, orient="horizontal", command=self.canvas.xview, style="PDF.Horizontal.TScrollbar")
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        # grille
        wrap.grid_rowconfigure(0, weight=1)
        wrap.grid_columnconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.hbar.grid(row=1, column=0, sticky="ew")

        # Taille initiale
        toplevel = self.winfo_toplevel()
        toplevel.update_idletasks()
        w = max(720, int(toplevel.winfo_width() * 0.72))
        h = max(420, int(toplevel.winfo_height() * 0.56))
        self.canvas.config(width=w, height=h)

        # taille auto
        self.after_idle(self._initial_fit_and_render)

        # redim auto
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # zoom molette
        self._bind_mousewheel()

    # ajustement et zoom
    def _page_label_text(self) -> str:
        return f"Page {self.page_index + 1} / {len(self.doc)} — {self.pdf_path.name}"

    def _compute_fit_zoom(self) -> float:
        page = self.doc.load_page(self.page_index)
        pw, ph = page.rect.width, page.rect.height
        cw = max(1, self.canvas.winfo_width() - 12)
        ch = max(1, self.canvas.winfo_height() - 12)
        return max(0.2, min(4.0, min(cw / pw, ch / ph)))

    def _initial_fit_and_render(self):
        self.update_idletasks()
        self.zoom = self._compute_fit_zoom()
        self.auto_fit = True
        self.render_page()

    def fit_to_area(self):
        self.zoom = self._compute_fit_zoom()
        self.auto_fit = True
        self.render_page()

    def _on_canvas_resize(self, *_):
        if self.auto_fit:
            z = self._compute_fit_zoom()
            if abs(z - self.zoom) > 1e-3:
                self.zoom = z
                self.render_page()

    # rendu
    def render_page(self):
        page = self.doc.load_page(self.page_index)
        mat = fitz.Matrix(self.zoom, self.zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self._photo = ImageTk.PhotoImage(img)

        if self._img_id is None:
            self._img_id = self.canvas.create_image(0, 0, image=self._photo, anchor="nw")
        else:
            self.canvas.itemconfig(self._img_id, image=self._photo)

        self.canvas.configure(scrollregion=(0, 0, self._photo.width(), self._photo.height()))
        self.page_lab.configure(text=self._page_label_text())

    # navigation zoom
    def prev_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            if self.auto_fit:
                self.zoom = self._compute_fit_zoom()
            self.render_page()

    def next_page(self):
        if self.page_index < len(self.doc) - 1:
            self.page_index += 1
            if self.auto_fit:
                self.zoom = self._compute_fit_zoom()
            self.render_page()

    def zoom_in(self):
        self.auto_fit = False
        self.zoom = min(self.zoom * 1.2, 6.0)
        self.render_page()

    def zoom_out(self):
        self.auto_fit = False
        self.zoom = max(self.zoom / 1.2, 0.2)
        self.render_page()

    def close_viewer(self):
        self.event_generate("<<PdfViewerClosed>>")

    # --------- souris ----------
    def _bind_mousewheel(self):
        # Windows/Mac
        self.canvas.bind_all("<MouseWheel>", self._on_wheel)
        # Linux
        self.canvas.bind_all("<Button-4>", self._on_wheel)
        self.canvas.bind_all("<Button-5>", self._on_wheel)

        # Ctrl + molette = zoom
        self.canvas.bind_all("<Control-MouseWheel>", self._on_ctrl_wheel)
        self.canvas.bind_all("<Control-Button-4>", self._on_ctrl_wheel)
        self.canvas.bind_all("<Control-Button-5>", self._on_ctrl_wheel)

    def _on_wheel(self, e):
        delta = 0
        if hasattr(e, "delta") and e.delta:
            delta = e.delta
        elif hasattr(e, "num"):
            delta = 120 if e.num == 4 else -120
        self.canvas.yview_scroll(-1 if delta > 0 else 1, "units")

    def _on_ctrl_wheel(self, e):
        self.auto_fit = False
        delta = 0
        if hasattr(e, "delta") and e.delta:
            delta = e.delta
        elif hasattr(e, "num"):
            delta = 120 if e.num == 4 else -120
        if delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
        return "break"


# vitrine
def _make_thumb(pdf: Path, width: int = 260, height: int = 340):
    """Retourne (PhotoImage, size) de la 1ère page. Nécessite PyMuPDF + PIL."""
    doc = fitz.open(pdf.as_posix())
    page = doc.load_page(0)
    zoom = 260 / max(page.rect.width, 1)
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.thumbnail((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(img), img.size


def build(parent: tk.Misc) -> ttk.Frame:
    body = ttk.Frame(parent)

    # centrage vertical
    for c in (0, 2):
        body.grid_columnconfigure(c, weight=1)
    body.grid_rowconfigure(0, weight=1)
    body.grid_rowconfigure(2, weight=1)

    # conteneur central
    container = ttk.Frame(body, style="Card.TFrame", padding=20)
    container.grid(row=1, column=1, sticky="n", padx=40, pady=24)

    ttk.Label(container, text="Ressources PDF",
              style="Heading.TLabel", font=("Segoe UI", 15, "bold"))\
        .grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

    container.grid_columnconfigure(0, weight=1)

    project_root = Path(__file__).resolve().parents[1]
    pdf_dir = project_root / "pdf"
    pdf_files = sorted(pdf_dir.glob("*.pdf"))

    images_refs = []

    def open_viewer(p: Path):
        # remplace galerie par viewer
        for w in container.grid_slaves(row=1, column=0):
            w.destroy()

        viewer = PdfViewer(container, p)
        viewer.grid(row=1, column=0, sticky="nsew")

        # assure bonne calibration pour viewer
        container.update_idletasks()
        container.grid_rowconfigure(1, weight=1)  # la ligne du viewer s’étire
        container.grid_columnconfigure(0, weight=1)

        # option pour close
        viewer.bind("<<PdfViewerClosed>>", lambda _:
        _back_to_gallery())

    def _back_to_gallery():
        for w in container.grid_slaves(row=1, column=0):
            w.destroy()
        _build_gallery()

    def _build_gallery():
        gal = ttk.Frame(container, style="Panel.TFrame")
        gal.grid(row=1, column=0, sticky="nsew")
        for i in range(3):
            gal.grid_columnconfigure(i, weight=1)

        if not pdf_files:
            ttk.Label(gal, text="Aucun PDF trouvé dans ./pdf",
                      style="Muted.TLabel").grid(row=0, column=1, pady=40)
            return

        for idx, p in enumerate(pdf_files[:2]):  # deux vitrines
            col = 0 if idx == 0 else 2
            card = ttk.Frame(gal, style="Card.TFrame", padding=12)
            card.grid(row=0, column=col, padx=36, pady=18, sticky="n")
            title = ttk.Label(card, text=p.name, style="Heading.TLabel")
            title.pack(pady=(0, 8))

            if HAS_PYMUPDF:
                try:
                    ph, _ = _make_thumb(p)
                    images_refs.append(ph)
                    canv = tk.Label(card, image=ph, bg=PALETTE["panel"])
                    canv.pack()
                except Exception:
                    ttk.Label(card, text="Aperçu indisponible",
                              style="Muted.TLabel").pack()

            ttk.Button(card, text="Ouvrir",
                       style="Primary.TButton",
                       command=lambda f=p: open_viewer(f)).pack(pady=10)

    _build_gallery()
    return body
