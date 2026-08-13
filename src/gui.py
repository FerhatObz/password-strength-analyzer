import tkinter as tk
from tkinter import messagebox

from src.analyzer import analyze_password


BG_COLOR = "#111111"
PANEL_COLOR = "#1A1A1A"
TEXT_COLOR = "#F2F2F2"
SECONDARY_TEXT = "#9A9A9A"
ACCENT_COLOR = "#7CFFB2"
BORDER_COLOR = "#2A2A2A"


def analyze():
    # Kullanıcının yazdığı parolayı alıyoruz.
    password = password_entry.get()

    if not password:
        messagebox.showwarning("Password Analyzer", "Please enter a password.")
        return

    # Mevcut analiz motorumuzu GUI'ye bağlıyoruz.
    result = analyze_password(password)

    score = result["score"]["score"]
    strength = result["score"]["strength"]

    score_label.config(text=f"{score}/100")
    strength_label.config(text=strength)

    entropy_label.config(
        text=f"{result['entropy']:.2f} bits"
    )

    common_label.config(
        text="Yes" if result["is_common"] else "No"
    )

    pattern_label.config(
        text="Detected" if result["patterns"]["has_pattern"] else "None detected"
    )

    policy_label.config(
        text="Passed" if result["policy"]["passed"] else "Failed"
    )

    length_label.config(
        text=str(result["length"])
    )


def toggle_password():
    # Parolayı görmek istersek gizlemeyi kaldırıyoruz.
    if password_entry.cget("show") == "":
        password_entry.config(show="•")
        show_button.config(text="SHOW")
    else:
        password_entry.config(show="")
        show_button.config(text="HIDE")


root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("620x720")
root.resizable(False, False)
root.configure(bg=BG_COLOR)


# ---------------- HEADER ----------------

title_label = tk.Label(
    root,
    text="PASSWORD STRENGTH ANALYZER",
    font=("Segoe UI", 20, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

title_label.pack(pady=(35, 5))


subtitle_label = tk.Label(
    root,
    text="Local password security assessment",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

subtitle_label.pack(pady=(0, 30))


# ---------------- PASSWORD INPUT ----------------

input_panel = tk.Frame(
    root,
    bg=PANEL_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

input_panel.pack(
    padx=40,
    fill="x"
)


input_title = tk.Label(
    input_panel,
    text="PASSWORD",
    font=("Segoe UI", 9, "bold"),
    bg=PANEL_COLOR,
    fg=SECONDARY_TEXT
)

input_title.pack(
    anchor="w",
    padx=20,
    pady=(18, 5)
)


password_frame = tk.Frame(
    input_panel,
    bg=PANEL_COLOR
)

password_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 18)
)


password_entry = tk.Entry(
    password_frame,
    font=("Segoe UI", 13),
    bg="#222222",
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    show="•"
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10
)


show_button = tk.Button(
    password_frame,
    text="SHOW",
    font=("Segoe UI", 8, "bold"),
    bg="#222222",
    fg=SECONDARY_TEXT,
    activebackground="#222222",
    activeforeground=TEXT_COLOR,
    relief="flat",
    bd=0,
    command=toggle_password
)

show_button.pack(
    side="right",
    padx=(8, 0)
)


# ---------------- ANALYZE BUTTON ----------------

analyze_button = tk.Button(
    root,
    text="ANALYZE PASSWORD",
    font=("Segoe UI", 10, "bold"),
    bg=ACCENT_COLOR,
    fg="#111111",
    activebackground=ACCENT_COLOR,
    activeforeground="#111111",
    relief="flat",
    bd=0,
    cursor="hand2",
    command=analyze
)

analyze_button.pack(
    padx=40,
    pady=25,
    fill="x",
    ipady=12
)


# ---------------- RESULT PANEL ----------------

result_panel = tk.Frame(
    root,
    bg=PANEL_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

result_panel.pack(
    padx=40,
    fill="both"
)


result_title = tk.Label(
    result_panel,
    text="SECURITY SCORE",
    font=("Segoe UI", 9, "bold"),
    bg=PANEL_COLOR,
    fg=SECONDARY_TEXT
)

result_title.pack(pady=(20, 5))


score_label = tk.Label(
    result_panel,
    text="--/100",
    font=("Segoe UI", 34, "bold"),
    bg=PANEL_COLOR,
    fg=ACCENT_COLOR
)

score_label.pack()


strength_label = tk.Label(
    result_panel,
    text="WAITING FOR ANALYSIS",
    font=("Segoe UI", 11, "bold"),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR
)

strength_label.pack(
    pady=(0, 20)
)


def create_result_row(parent, title):
    frame = tk.Frame(
        parent,
        bg=PANEL_COLOR
    )

    frame.pack(
        fill="x",
        padx=20,
        pady=5
    )

    left = tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 10),
        bg=PANEL_COLOR,
        fg=SECONDARY_TEXT
    )

    left.pack(side="left")

    right = tk.Label(
        frame,
        text="--",
        font=("Segoe UI", 10, "bold"),
        bg=PANEL_COLOR,
        fg=TEXT_COLOR
    )

    right.pack(side="right")

    return right


length_label = create_result_row(
    result_panel,
    "Length"
)

entropy_label = create_result_row(
    result_panel,
    "Entropy"
)

common_label = create_result_row(
    result_panel,
    "Common Password"
)

pattern_label = create_result_row(
    result_panel,
    "Pattern"
)

policy_label = create_result_row(
    result_panel,
    "Policy"
)


# ---------------- FOOTER ----------------

footer_label = tk.Label(
    root,
    text="Local analysis • Password is not stored",
    font=("Segoe UI", 8),
    bg=BG_COLOR,
    fg="#666666"
)

footer_label.pack(
    pady=25
)


password_entry.focus()

root.mainloop()