import tkinter as tk
from tkinter import ttk
from app import home, temp, somme, accueil, calcul, annee

# const
APP_TITLE = "Python TP1"
WIN_W, WIN_H = 1100, 700
HEADER_H = 68
STATUS_H = 24

PALETTE = {
    "bg": "#0F1115",
    "panel": "#1A1F29",
    "panel2": "#151923",
    "border": "#252B36",
    "fg": "#E5E7EB",
    "fg_muted": "#9CA3AF",
    "accent": "#6EAAFF",
    "hover": "#202635",
    "active": "#283046",
    "focus": "#3B82F6",
}

# tools
def center_window(win, w, h):
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = (sw - w) // 2, (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

def apply_scaling(root):
    try:
        scaling = root.winfo_fpixels('1i') / 96.0
        root.tk.call('tk', 'scaling', scaling)
    except Exception:
        root.tk.call('tk', 'scaling', 1.0)

def setup_style(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    root.configure(bg=PALETTE["bg"])
    style.configure(".", foreground=PALETTE["fg"], background=PALETTE["bg"])
    style.configure("TFrame", background=PALETTE["bg"])
    style.configure("Panel.TFrame", background=PALETTE["panel"])
    style.configure("Panel2.TFrame", background=PALETTE["panel2"])
    style.configure("TLabel", background=PALETTE["bg"], foreground=PALETTE["fg"])
    style.configure("Muted.TLabel", foreground=PALETTE["fg_muted"])
    style.configure("Heading.TLabel", font=("Segoe UI", 12, "bold"))

    # Boutons
    style.configure("TButton",
                    background=PALETTE["panel"],
                    foreground=PALETTE["fg"],
                    bordercolor=PALETTE["border"],
                    focusthickness=0, focuscolor=PALETTE["panel"],
                    padding=(12, 8))
    style.map("TButton",
              background=[("active", PALETTE["active"]), ("hover", PALETTE["hover"])],
              relief=[("pressed", "sunken"), ("!pressed", "flat")])

    # Bouton t
    style.configure("Primary.TButton",
                    background=PALETTE["accent"],
                    foreground="white",
                    padding=(16, 10),
                    font=("Segoe UI", 12, "bold"))
    style.map("Primary.TButton",
              background=[("active", "#528FFF"), ("hover", "#5B9BFF")],
              foreground=[("disabled", "white")])

    # entry
    style.configure("Input.TEntry",
                    fieldbackground="#E5E7EB",
                    foreground="#000000",
                    insertcolor="#000000",
                    padding=8,
                    font=("Segoe UI", 13, "bold"))

    # Radios
    style.configure("Radio.TRadiobutton",
                    background=PALETTE["bg"], foreground=PALETTE["fg"])
    style.map("Radio.TRadiobutton",
              background=[("active", PALETTE["bg"]), ("selected", PALETTE["bg"])],
              foreground=[("active", PALETTE["fg"]), ("selected", PALETTE["fg"])])

    # Style
    style.configure("Nav.TButton",
                    background=PALETTE["panel2"],
                    foreground=PALETTE["fg"],
                    padding=(18, 10),
                    font=("Segoe UI", 12, "bold"))
    style.map("Nav.TButton",
              background=[("active", PALETTE["hover"]), ("hover", PALETTE["hover"])],
              foreground=[("disabled", PALETTE["fg_muted"])])

    style.configure("NavIcon.TButton",
                    background=PALETTE["panel2"],
                    foreground=PALETTE["fg"],
                    padding=(14, 10),
                    font=("Segoe UI Emoji", 14))  # icône 🏠 plus grande
    style.map("NavIcon.TButton",
              background=[("active", PALETTE["hover"]), ("hover", PALETTE["hover"])])

# ui
current_body = None
content_frame = None

def build_ui(root):
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Header
    header = ttk.Frame(root, style="Panel2.TFrame", height=HEADER_H)
    header.grid(row=0, column=0, sticky="new")
    header.grid_propagate(False)

    # body
    home_btn = ttk.Button(header, text="🏠", style="NavIcon.TButton",
                          command=lambda: show_body("home"))
    home_btn.pack(side="left", padx=(12, 22))

    # Barre nav
    nav_frame = ttk.Frame(header, style="Panel2.TFrame")
    nav_frame.pack(side="top", pady=8)

    titles = [
        ("Celsius × Fahrenheit", "temp"),
        ("+ & * des nombres pairs", "somme"),
        ("Une accueil pas comme les autres", "accueil"),
        ("Un calcul mental ?", "calcul"),
        ("Cette année est bissextile ?", "annee"),
    ]

    nav_buttons = []
    for txt, key in titles:
        b = ttk.Button(nav_frame, text=txt, style="Nav.TButton",
                       command=lambda k=key: show_body(k))
        b.pack(side="left", padx=10)
        nav_buttons.append(b)

    # Cont
    global content_frame
    content_frame = ttk.Frame(root, style="Panel.TFrame")
    content_frame.grid(row=1, column=0, sticky="nsew")

    show_body("home")

    # Status bar
    status = ttk.Frame(root, style="Panel2.TFrame", height=STATUS_H)
    status.grid(row=2, column=0, sticky="sew")
    status.grid_propagate(False)

    # Largeur minimale
    def set_min_width():
        root.update_idletasks()
        required = home_btn.winfo_reqwidth() + 24
        for btn in nav_buttons:
            required += btn.winfo_reqwidth() + 20
        required += 40  # sécurité
        root.wm_minsize(max(WIN_W, required), 560)

    root.after(0, set_min_width)

def show_body(name: str):
    global current_body
    if current_body is not None:
        current_body.destroy()
        current_body = None

    if name == "home":
        current_body = home.build(content_frame)
    elif name == "temp":
        current_body = temp.build(content_frame)
    elif name == "somme":
        current_body = somme.build(content_frame)
    elif name == "accueil":
        current_body = accueil.build(content_frame)
    elif name == "calcul":
        current_body = calcul.build(content_frame)
    elif name == "annee":
        current_body = annee.build(content_frame)
    else:
        current_body = ttk.Frame(content_frame)

    current_body.pack(fill="both", expand=True)

# main
def main():
    root = tk.Tk()
    root.title(APP_TITLE)
    center_window(root, WIN_W, WIN_H)
    root.wm_minsize(WIN_W, 560)  # baseline
    apply_scaling(root)
    setup_style(root)
    build_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
