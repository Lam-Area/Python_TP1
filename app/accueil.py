# accueil.py
import tkinter as tk
from tkinter import ttk
import random

GREETINGS = [
    "Bonjour", "Salut", "Bienvenue", "Coucou", "Hey",
    "Ravi de te voir", "Content de te retrouver", "Enchanté",
]

def _split_names(raw: str) -> list[str]:
    """
    Coupe sur virgules et retours ligne, nettoie les espaces.
    Supprime les doublons vides.
    """
    parts = []
    for chunk in raw.replace(";", ",").split(","):
        for sub in chunk.splitlines():
            name = sub.strip()
            if name:
                parts.append(name)
    return parts

def build(parent: tk.Misc) -> ttk.Frame:
    body = ttk.Frame(parent)

    # centrer la carte
    for c in (0, 2):
        body.grid_columnconfigure(c, weight=1)
    body.grid_rowconfigure(0, weight=1)
    body.grid_rowconfigure(2, weight=1)   # rangée du footer (astuce)

    # ---- Carte ----
    card = ttk.Frame(body, style="Card.TFrame", padding=26)
    card.grid(row=1, column=1, sticky="n", padx=40, pady=18)
    card.configure(width=720)

    ttk.Label(card, text="Messages d'accueil personnalisés",
              style="Heading.TLabel", font=("Segoe UI", 15, "bold"))\
        .grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 14))

    # Champ des noms
    ttk.Label(card, text="Entrez une liste de prénoms (séparés par virgules ou retours à la ligne) :",
              style="Muted.TLabel", font=("Segoe UI", 11))\
        .grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 6))

    names_var = tk.StringVar()
    names_entry = ttk.Entry(card, textvariable=names_var, style="Input.TEntry", width=48)
    names_entry.grid(row=2, column=0, columnspan=2, sticky="w")

    # ---- Zone résultats (readonly + fond discret + scrollbar auto) ----
    result_wrap = ttk.Frame(card, style="Result.TFrame")
    result_wrap.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=(14, 0))
    card.grid_rowconfigure(4, weight=1)
    card.grid_columnconfigure(3, weight=1)

    txt = tk.Text(
        result_wrap,
        height=10,
        wrap="word",
        relief="flat",
        background="#202635",
        foreground="#E5E7EB",
        insertbackground="#E5E7EB",
        font=("Consolas", 12),
        cursor="arrow",
        takefocus=0
    )
    vscroll = ttk.Scrollbar(result_wrap, orient="vertical", style="Result.Vertical.TScrollbar")
    txt.grid(row=0, column=0, sticky="nsew")
    result_wrap.grid_rowconfigure(0, weight=1)
    result_wrap.grid_columnconfigure(0, weight=1)

    # scrollbar seulement si nécessaire
    def _update_scroll_visibility():
        first, last = txt.yview()
        if (last - first) >= 1.0:
            vscroll.grid_remove()
        else:
            vscroll.grid(row=0, column=1, sticky="ns", padx=(6, 0))

    def _yscroll(first, last):
        vscroll.set(first, last)
        _update_scroll_visibility()

    txt.configure(yscrollcommand=_yscroll, state="disabled")

    # bloquer l’édition par l’utilisateur
    txt.bind("<Key>", lambda e: "break")
    txt.bind("<Button-1>", lambda e: "break")

    def show(lines: list[str]):
        txt.configure(state="normal")
        txt.delete("1.0", "end")
        if lines:
            txt.insert("1.0", "\n".join(lines))
        txt.configure(state="disabled")
        txt.update_idletasks()
        _update_scroll_visibility()

    # Génération
    def generer(*_):
        raw = names_var.get()
        names = _split_names(raw)
        if not names:
            tip_var.set("❌ Ajoute au moins un prénom.")
            show([])
            return

        tip_var.set("")  # efface l’astuce si OK
        lines = []
        for name in names:
            greet = random.choice(GREETINGS)
            lines.append(f"{greet}, {name} !")
        show(lines)

    def reset():
        names_var.set("")
        tip_var.set("Astuce : ex. Alice, Bob, Charlie")
        show([])

    # Boutons
    ttk.Button(card, text="Effacer", style="TButton", command=reset)\
        .grid(row=2, column=3, padx=(12, 8), sticky="e")
    ttk.Button(card, text="Générer", style="Primary.TButton", command=generer)\
        .grid(row=2, column=4, padx=(0, 0), sticky="e")

    # ---- Astuce en bas à gauche du BODY (comme temp) ----
    tip_var = tk.StringVar(value="Astuce : ex. Alice, Bob, Charlie")
    footer = ttk.Frame(body, style="Panel.TFrame")
    footer.grid(row=2, column=0, columnspan=3, sticky="sw", padx=24, pady=(0, 24))
    ttk.Label(footer, textvariable=tip_var, style="Muted.TLabel").pack(anchor="w")

    # Bind + focus
    names_entry.bind("<Return>", generer)
    names_entry.focus_set()

    # init affichage (cache la scrollbar au départ)
    show([])

    return body
