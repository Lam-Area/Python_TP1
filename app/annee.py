# annee.py
import tkinter as tk
from tkinter import ttk
from datetime import date

def _is_leap(year: int) -> bool:
    # Année bissextile : divisible par 4, sauf séculaires non divisibles par 400.
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def build(parent: tk.Misc) -> ttk.Frame:
    body = ttk.Frame(parent)

    # Centrer la carte
    for c in (0, 2):
        body.grid_columnconfigure(c, weight=1)
    body.grid_rowconfigure(0, weight=1)
    body.grid_rowconfigure(2, weight=1)

    # ---- Carte ----
    card = ttk.Frame(body, style="Card.TFrame", padding=24)
    card.grid(row=1, column=1, sticky="n", padx=40, pady=18)

    ttk.Label(card, text="Cette année est bissextile ?",
              style="Heading.TLabel", font=("Segoe UI", 15, "bold"))\
        .grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

    # Saisie
    ttk.Label(card, text="Entrez une année :", style="Muted.TLabel",
              font=("Segoe UI", 11, "bold"))\
        .grid(row=1, column=0, sticky="w", pady=(0, 6))

    year_var = tk.StringVar()
    entry = ttk.Entry(card, textvariable=year_var, style="Input.TEntry", width=12)
    entry.grid(row=1, column=1, sticky="w", pady=(0, 6), padx=(8, 0))

    # Résultat (caché au départ)
    result_var = tk.StringVar(value="")
    result_label = ttk.Label(card, textvariable=result_var, font=("Segoe UI", 12))
    result_label.grid(row=2, column=0, columnspan=4, sticky="w", pady=(12, 0))
    result_label.grid_remove()

    def check_leap_year():
        raw = year_var.get().strip()
        if not raw:
            result_var.set("❌ Entre une année valide.")
            result_label.grid()
            return
        try:
            year = int(raw)
        except ValueError:
            result_var.set("❌ Entre un nombre valide.")
            result_label.grid()
            return

        if _is_leap(year):
            result_var.set(f"✅ {year} est bissextile.")
        else:
            result_var.set(f"❌ {year} n'est pas bissextile.")
        result_label.grid()

    def on_verify(*_):
        check_leap_year()  # ← utiliser la bonne fonction

    def use_current_year():
        y = date.today().year
        year_var.set(str(y))
        check_leap_year()   # ← utiliser la bonne fonction

    # Boutons
    ttk.Button(card, text="Année courante", style="TButton",
               command=use_current_year)\
        .grid(row=1, column=2, padx=(12, 6), sticky="w")

    ttk.Button(card, text="Vérifier", style="Primary.TButton",
               command=on_verify)\
        .grid(row=1, column=3, padx=(6, 0), sticky="w")

    # Raccourci Entrée
    entry.bind("<Return>", on_verify)
    entry.focus_set()

    # Tip en bas à gauche du body (garde/retire selon ton choix)
    tip = ttk.Label(
        body,
        text="Règle : divisible par 4, sauf les années séculaires (×100) non divisibles par 400.",
        style="Muted.TLabel"
    )
    tip.grid(row=2, column=0, columnspan=3, sticky="sw", padx=12, pady=8)

    return body
