import tkinter as tk
from tkinter import ttk

def even_list_upto(n: int) -> list[int]:
    """Retourne [2,4,...,n] si n est pair, sinon s'arrête à n-1."""
    if n < 2:
        return []
    end = n if n % 2 == 0 else n - 1
    return list(range(2, end + 1, 2))

def build(parent: tk.Misc) -> ttk.Frame:
    body = ttk.Frame(parent)

    # centrer la carte
    for c in (0, 2):
        body.grid_columnconfigure(c, weight=1)
    body.grid_rowconfigure(0, weight=1)
    body.grid_rowconfigure(2, weight=1)

    # ---- Carte ----
    card = ttk.Frame(body, style="Card.TFrame", padding=26)
    card.grid(row=1, column=1, sticky="n", padx=40, pady=18)
    card.configure(width=720)

    ttk.Label(card, text="La somme et le produit des nombres pairs",
              style="Heading.TLabel", font=("Segoe UI", 15, "bold"))\
        .grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 14))

    ttk.Label(card, text="Entrez un entier positif N :", style="Muted.TLabel", font=("Segoe UI", 11))\
        .grid(row=1, column=0, sticky="w", pady=(0, 6))

    n_var = tk.StringVar()
    entry = ttk.Entry(card, textvariable=n_var, width=16, style="Input.TEntry")
    entry.grid(row=2, column=0, sticky="w")

    # Message d'aide/erreur (caché par défaut)
    msg_var = tk.StringVar(value="")
    msg = ttk.Label(card, textvariable=msg_var, style="Muted.TLabel")
    msg.grid(row=2, column=1, sticky="w", padx=12)
    msg.grid_remove()

    # ---- Zone résultats (readonly + fond discret + scrollbar auto) ----
    result_wrap = ttk.Frame(card, style="Result.TFrame")
    result_wrap.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=(14, 0))
    card.grid_rowconfigure(3, weight=1)
    card.grid_columnconfigure(3, weight=1)

    txt = tk.Text(
        result_wrap,
        height=7,
        wrap="word",
        relief="flat",
        background="#202635",     # très léger contraste
        foreground="#E5E7EB",
        insertbackground="#E5E7EB",
        font=("Consolas", 12),
        cursor="arrow",
        takefocus=0
    )

    # >>> Retrait de width= (non supporté par ttk.Scrollbar)
    vscroll = ttk.Scrollbar(
        result_wrap,
        orient="vertical",
        style="Result.Vertical.TScrollbar",   # style défini dans main.py
    )

    # n'afficher la barre que si besoin
    def _update_scroll_visibility():
        first, last = txt.yview()
        if (last - first) >= 1.0:
            vscroll.grid_remove()
        else:
            vscroll.grid(row=0, column=1, sticky="ns", padx=(6, 0))

    def _yscroll(first, last):
        vscroll.set(first, last)
        _update_scroll_visibility()

    txt.configure(yscrollcommand=_yscroll)
    txt.grid(row=0, column=0, sticky="nsew")
    result_wrap.grid_rowconfigure(0, weight=1)
    result_wrap.grid_columnconfigure(0, weight=1)

    # Empêche toute saisie utilisateur dans la zone
    txt.bind("<Key>", lambda e: "break")
    txt.bind("<Button-1>", lambda e: "break")

    def write_output(lines: list[str]):
        txt.configure(state="normal")
        txt.delete("1.0", "end")
        if lines:
            txt.insert("1.0", "\n".join(lines))
        txt.configure(state="disabled")
        txt.update_idletasks()
        _update_scroll_visibility()

    def thousands(x: int) -> str:
        return f"{x:,}".replace(",", " ")

    def compute(*_):
        raw = n_var.get().strip()
        # N doit être un entier positif pair
        if not raw.isdigit():
            msg_var.set("Veuillez saisir un entier positif (ex. 6).")
            msg.grid()
            write_output([])
            return
        n = int(raw)
        if n <= 0:
            msg_var.set("N doit être > 0.")
            msg.grid()
            write_output([])
            return
        if n % 2 != 0:
            msg_var.set("N doit être un nombre PAIR.")
            msg.grid()
            write_output([])
            return

        evens = even_list_upto(n)
        if not evens:
            msg_var.set("Aucun pair ≤ N.")
            msg.grid()
            write_output([])
            return

        S = sum(evens)
        P = 1
        for e in evens:
            P *= e

        plus_expr = " + ".join(map(str, evens))
        star_expr = " * ".join(map(str, evens))

        lines = [
            f"{plus_expr} = {thousands(S)}",
            f"{thousands(S)} = {plus_expr}",
            f"{star_expr} = {thousands(P)}",
            f"{thousands(P)} = {star_expr}",
        ]
        msg_var.set("")
        msg.grid_remove()
        write_output(lines)

    # Actions
    ttk.Button(card, text="Calculer", style="Primary.TButton", command=compute)\
        .grid(row=2, column=3, padx=(18, 0))
    ttk.Button(card, text="Réinitialiser",
               command=lambda: (n_var.set(""), msg_var.set(""), msg.grid_remove(), write_output([])))\
        .grid(row=2, column=2, padx=(12, 0))

    entry.bind("<Return>", compute)
    entry.focus_set()

    # Grille interne
    for i in range(4):
        card.grid_columnconfigure(i, weight=0)
    card.grid_columnconfigure(1, weight=1)

    # Initial : zone vide -> scrollbar cachée
    write_output([])

    return body
