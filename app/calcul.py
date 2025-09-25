# calcul.py
import tkinter as tk
from tkinter import ttk
import random

OPS = {
    "add": ("+", lambda a, b: a + b),
    "sub": ("-", lambda a, b: a - b),
    "mul": ("×", lambda a, b: a * b),
    "div": ("÷", lambda a, b: a // b if b != 0 else None),
}

DIFFS = {
    "Facile (1–10)": (1, 10),
    "Classique (1–20)": (1, 20),
    "Avancé (10–99)": (10, 99),
}


def build(parent: tk.Misc) -> ttk.Frame:
    body = ttk.Frame(parent)

    # Centrage
    for c in (0, 2):
        body.grid_columnconfigure(c, weight=1)
    body.grid_rowconfigure(0, weight=1)
    body.grid_rowconfigure(2, weight=1)

    # Carte principale
    card = ttk.Frame(body, style="Card.TFrame", padding=22)
    card.grid(row=1, column=1, sticky="n", padx=40, pady=18)

    ttk.Label(card, text="Un jeu de calcul mental",
              style="Heading.TLabel", font=("Segoe UI", 14, "bold"))\
        .grid(row=0, column=0, columnspan=7, sticky="w", pady=(0, 12))

    # Score
    score_ok = tk.IntVar(value=0)
    score_tot = tk.IntVar(value=0)
    score_lbl = ttk.Label(card, text="Score : 0 / 0", style="Muted.TLabel")
    score_lbl.grid(row=0, column=7, sticky="e", padx=(12, 0))

    def _update_score():
        score_lbl.config(text=f"Score : {score_ok.get()} / {score_tot.get()}")

    # Choix de l’opération
    ttk.Label(card, text="Opération :", style="Muted.TLabel",
              font=("Segoe UI", 11, "bold"))\
        .grid(row=1, column=0, sticky="w", pady=(0, 6), padx=(0, 6))

    op_var = tk.StringVar(value="add")
    for i, (key, (sym, _)) in enumerate(OPS.items()):
        ttk.Radiobutton(card,
                        text={"add": "Addition", "sub": "Soustraction",
                              "mul": "Multiplication", "div": "Division"}[key],
                        value=key, variable=op_var,
                        style="Radio.TRadiobutton")\
            .grid(row=1, column=i+1, sticky="w", padx=(8, 12))

    # Choix difficulté (aligné avec "Opération")
    ttk.Label(card, text="Difficulté :", style="Muted.TLabel",
              font=("Segoe UI", 11, "bold"))\
        .grid(row=1, column=5, sticky="w", padx=(24, 6))

    diff_var = tk.StringVar(value=list(DIFFS.keys())[0])
    diff_menu = ttk.Combobox(card, textvariable=diff_var, values=list(DIFFS.keys()),
                             state="readonly", width=16)
    diff_menu.grid(row=1, column=6, sticky="w")

    # Question
    question_var = tk.StringVar(value="Choisis l’opération et la difficulté, puis clique « Générer la question ».")
    question_lbl = ttk.Label(card, textvariable=question_var, font=("Segoe UI", 12))
    question_lbl.grid(row=2, column=0, columnspan=7, sticky="w", pady=(10, 6))

    # Réponse
    ttk.Label(card, text="Réponse :", style="Muted.TLabel",
              font=("Segoe UI", 11, "bold"))\
        .grid(row=3, column=0, sticky="w")

    answer_var = tk.StringVar()
    answer_entry = ttk.Entry(card, textvariable=answer_var, style="Input.TEntry", width=12)
    answer_entry.grid(row=3, column=1, sticky="w")

    # Feedback
    feedback_var = tk.StringVar(value="")
    feedback = ttk.Label(card, textvariable=feedback_var, style="Muted.TLabel")
    feedback.grid(row=3, column=2, columnspan=4, sticky="w", padx=(12, 0))
    feedback.grid_remove()

    def show_feedback(msg: str | None):
        if msg:
            feedback_var.set(msg)
            feedback.grid()
        else:
            feedback_var.set("")
            feedback.grid_remove()

    # Boutons
    def _reset_ui_to_ready():
        state.update(a=None, b=None, op=None, ans=None)
        question_var.set("Choisis l’opération et la difficulté, puis clique « Générer la question ».")
        answer_var.set("")
        answer_entry.config(state="disabled")
        validate_btn.config(state="disabled")
        show_feedback(None)

    def generate_question(*_):
        rng = DIFFS[diff_var.get()]
        a = random.randint(*rng)
        b = random.randint(*rng)
        op = op_var.get()
        sym, fn = OPS[op]
        ans = fn(a, b)
        if ans is None:  # éviter division par 0
            return generate_question()
        state.update(a=a, b=b, op=op, ans=ans)
        question_var.set(f"Combien fait {a} {sym} {b} ?")
        answer_var.set("")
        answer_entry.config(state="normal")
        validate_btn.config(state="normal")
        show_feedback(None)

    def validate(*_):
        if state["ans"] is None:
            return
        raw = answer_var.get().strip().replace(",", ".")
        try:
            user_ans = int(raw)
        except Exception:
            show_feedback("❌ Nombre invalide.")
            return

        score_tot.set(score_tot.get() + 1)
        if user_ans == state["ans"]:
            score_ok.set(score_ok.get() + 1)
            show_feedback("✅ Correct !")
            answer_entry.config(state="disabled")
            validate_btn.config(state="disabled")
        else:
            sym, _ = OPS[state["op"]]
            show_feedback(f"❌ Faux. Réponse : {state['a']} {sym} {state['b']} = {state['ans']}")
        _update_score()

    gen_btn = ttk.Button(card, text="Générer la question", style="Primary.TButton",
                         command=generate_question)
    gen_btn.grid(row=4, column=0, columnspan=2, pady=(14, 0), sticky="w")

    validate_btn = ttk.Button(card, text="Valider", style="Primary.TButton", command=validate)
    validate_btn.grid(row=4, column=2, columnspan=2, pady=(14, 0), padx=(12, 0), sticky="w")

    # État
    state = {"a": None, "b": None, "op": None, "ans": None}
    _reset_ui_to_ready()

    return body
