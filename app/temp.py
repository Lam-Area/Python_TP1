# temp.py
import tkinter as tk
from tkinter import ttk

def c_to_f(c: float) -> float:
    return c * 9.0 / 5.0 + 32.0

def f_to_c(f: float) -> float:
    return (f - 32.0) * 5.0 / 9.0

def _parse_float(s: str) -> float:
    return float(s.strip().replace(",", "."))

def build(parent: tk.Misc) -> ttk.Frame:
    """
    Body centré : carte plus grande, textes agrandis.
    Formules/astuce ancrées en bas à GAUCHE du body (hauteur inchangée).
    """
    body = ttk.Frame(parent)

    # grille pour centrer la carte et réserver une rangée "footer"
    for c in (0, 2):
        body.grid_columnconfigure(c, weight=1)
    body.grid_rowconfigure(0, weight=1)   # espace haut
    body.grid_rowconfigure(1, weight=0)   # carte
    body.grid_rowconfigure(2, weight=1)   # pousse le footer en bas (hauteur inchangée)

    # ---------- Carte agrandie ----------
    card = ttk.Frame(body, style="Card.TFrame", padding=26)
    card.grid(row=1, column=1, sticky="n", padx=40, pady=18)
    card.configure(width=720)  # + large

    # Titre plus grand
    ttk.Label(card, text="Convertir une température",
              style="Heading.TLabel", font=("Segoe UI", 15, "bold"))\
       .grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 14))

    # Radios (typo + état stable)
    choice = tk.StringVar(value="C2F")
    rb_style = "Radio.TRadiobutton"
    ttk.Radiobutton(card, text="Celsius → Fahrenheit", value="C2F",
                    variable=choice, style=rb_style, cursor="hand2",
                    ).grid(row=1, column=0, sticky="w", pady=(0, 10))
    ttk.Radiobutton(card, text="Fahrenheit → Celsius", value="F2C",
                    variable=choice, style=rb_style, cursor="hand2",
                    ).grid(row=1, column=1, sticky="w", pady=(0, 10))

    # Labels un peu plus grands
    ttk.Label(card, text="Valeur :", style="Muted.TLabel", font=("Segoe UI", 11))\
       .grid(row=2, column=0, sticky="w", pady=(2, 6))

    # Champ clair (texte noir) + un peu plus large
    entry = ttk.Entry(card, width=24, style="Input.TEntry")
    entry.grid(row=3, column=0, sticky="w")

    # Séparateur visuel + résultat plus grand
    ttk.Label(card, text="→", style="Muted.TLabel", font=("Segoe UI", 12))\
       .grid(row=3, column=1, padx=16)

    result = tk.StringVar(value="—")
    ttk.Label(card, textvariable=result, font=("Segoe UI", 13, "bold"))\
       .grid(row=3, column=2, sticky="w")

    # Bouton plus grand
    def convert(*_):
        try:
            v = _parse_float(entry.get())
            val = c_to_f(v) if choice.get() == "C2F" else f_to_c(v)
            unit = "°F" if choice.get() == "C2F" else "°C"
            result.set(f"{val:.2f} {unit}")
        except ValueError:
            result.set("Entrée invalide")

    ttk.Button(card, text="Convertir", command=convert, style="Primary.TButton")\
       .grid(row=3, column=5, padx=(24, 0))

    entry.bind("<Return>", convert)
    entry.focus_set()

    # grille interne
    for i in range(6):
        card.grid_columnconfigure(i, weight=0)
    card.grid_columnconfigure(2, weight=1)  # laisse respirer le résultat

    # ---------- Footer (formules) : collé à GAUCHE du body ----------
    footer = ttk.Frame(body)
    footer.grid(row=2, column=0, columnspan=3, sticky="sw", padx=24, pady=(0, 24))
    ttk.Label(
        footer,
        text="Formules  •  °F = (°C × 9/5) + 32     •     °C = (°F − 32) × 5/9",
        style="Muted.TLabel"
    ).pack(anchor="w")
    ttk.Label(
        footer,
        text="Astuce : la virgule est acceptée (ex. 36,6).",
        style="Muted.TLabel"
    ).pack(anchor="w")

    return body
