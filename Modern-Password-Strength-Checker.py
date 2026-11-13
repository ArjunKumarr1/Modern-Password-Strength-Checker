from logging import root
import re
import random
import string
import customtkinter as ctk
from tkinter import messagebox

# -------------------- APP CONFIG --------------------
ctk.set_appearance_mode("dark")      # "light", "dark", "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

APP_WIDTH = 900
APP_HEIGHT = 680

# -------------------- PASSWORD LOGIC --------------------
def analyze_password(password):
    score = 0
    checks = {
        "At least 8 characters": False,
        "At least 12 characters": False,
        "Contains lowercase letter": False,
        "Contains uppercase letter": False,
        "Contains number": False,
        "Contains special character": False
    }
    feedback = []

    # Rule checks
    if len(password) >= 8:
        checks["At least 8 characters"] = True
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if len(password) >= 12:
        checks["At least 12 characters"] = True
        score += 1
    else:
        feedback.append("Use 12+ characters for better security.")

    if re.search(r"[a-z]", password):
        checks["Contains lowercase letter"] = True
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if re.search(r"[A-Z]", password):
        checks["Contains uppercase letter"] = True
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if re.search(r"[0-9]", password):
        checks["Contains number"] = True
        score += 1
    else:
        feedback.append("Add at least one number.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\];'`~]", password):
        checks["Contains special character"] = True
        score += 1
    else:
        feedback.append("Add at least one special character.")

    # Strength levels
    if score <= 2:
        strength = "Weak"
        color = "#ff4d4d"
        progress = 0.20
    elif score <= 4:
        strength = "Medium"
        color = "#ffaa00"
        progress = 0.55
    elif score == 5:
        strength = "Strong"
        color = "#4da6ff"
        progress = 0.80
    else:
        strength = "Very Strong"
        color = "#00cc66"
        progress = 1.0

    return strength, color, progress, checks, feedback


# -------------------- APP FUNCTIONS --------------------
def evaluate_password(event=None):
    password = password_entry.get().strip()

    if not password:
        messagebox.showwarning("Warning", "Please enter a password first.")
        return

    strength, color, progress, checks, feedback = analyze_password(password)

    # Strength label
    strength_value_label.configure(text=strength, text_color=color)

    # Progress bar
    progress_bar.set(progress)
    score_percentage = int(progress * 100)
    percent_label.configure(text=f"{score_percentage}% Secure")

    # Rule checklist update
    for rule, label in rule_labels.items():
        if checks[rule]:
            label.configure(text=f"✔ {rule}", text_color="#00cc66")
        else:
            label.configure(text=f"✘ {rule}", text_color="#ff5c5c")

    # Feedback update
    feedback_box.configure(state="normal")
    feedback_box.delete("1.0", "end")
    if feedback:
        feedback_box.insert("end", "Suggestions to improve password:\n\n")
        for item in feedback:
            feedback_box.insert("end", f"• {item}\n")
    else:
        feedback_box.insert("end", "Excellent! Your password is secureand satisfies all major conditions.")
    feedback_box.configure(state="disabled")


def toggle_password():
    if show_password_var.get() == 1:
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")


def clear_all():
    password_entry.delete(0, "end")
    strength_value_label.configure(text="Not Checked", text_color="white")
    progress_bar.set(0)
    percent_label.configure(text="0% Secure")

    for rule, label in rule_labels.items():
        label.configure(text=f"• {rule}", text_color="gray70")

    feedback_box.configure(state="normal")
    feedback_box.delete("1.0", "end")
    feedback_box.configure(state="disabled")


def generate_password():
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{};:,.<>?/"

    # Ensure strong password
    password_chars = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]

    all_chars = lowercase + uppercase + digits + special
    for _ in range(10):  # total length = 14
        password_chars.append(random.choice(all_chars))

    random.shuffle(password_chars)
    generated_password = "".join(password_chars)

    password_entry.delete(0, "end")
    password_entry.insert(0, generated_password)
    evaluate_password()


def copy_password():
    password = password_entry.get().strip()
    if not password:
        messagebox.showwarning("Warning", "No password available to copy.")
        return
    app.clipboard_clear()
    app.clipboard_append(password)
    messagebox.showinfo("Copied", "Password copied to clipboard successfully.")


# -------------------- MAIN WINDOW --------------------
app = ctk.CTk() 
app.title("Modern Password Strength Checker")
app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
app.resizable(True, True)
app.state("zoomed")

# -------------------- TOP TITLE --------------------
title_label = ctk.CTkLabel(
    app,
    text="Modern Password Strength Checker",
    font=("Segoe UI", 27, "bold")
)
title_label.pack(pady=(20, 5))

title_label.pack(pady=(20, 5))

author_label = ctk.CTkLabel(
    app,
    text="BY",
    font=("Segoe UI", 13, "bold"),
    text_color="#15b3b9"
)
author_label.pack(pady=(0, 5))


author_label = ctk.CTkLabel(
    app,
    text="ARJUN",
    font=("Segoe UI", 16, "bold"),
    text_color="#e65255"
)
author_label.pack(pady=(0, 5))


# -------------------- MAIN FRAME --------------------
main_frame = ctk.CTkFrame(app, corner_radius=20)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# -------------------- LEFT SECTION --------------------
left_frame = ctk.CTkFrame(main_frame, corner_radius=16)
left_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)

input_label = ctk.CTkLabel(left_frame, text="Enter Password", font=("Segoe UI", 22, "bold"))
input_label.pack(pady=(20, 10))

password_entry = ctk.CTkEntry(
    left_frame,
    width=420,
    height=45,
    font=("Segoe UI", 16),
    show="*",
    placeholder_text="Type password here..."
)
password_entry.pack(pady=(10, 8))
password_entry.bind("<Return>", evaluate_password)

show_password_var = ctk.IntVar(value=0)
show_checkbox = ctk.CTkCheckBox(
    left_frame,
    text="Show Password",
    variable=show_password_var,
    command=toggle_password,
    font=("Segoe UI", 13)
)
show_checkbox.pack(pady=(0, 15))

# -------------------- BUTTONS --------------------
button_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
button_frame.pack(pady=10)

check_btn = ctk.CTkButton(
    button_frame,
    text="Check Strength",
    width=160,
    height=42,
    font=("Segoe UI", 14, "bold"),
    command=evaluate_password
)
check_btn.grid(row=0, column=0, padx=8, pady=8)

generate_btn = ctk.CTkButton(
    button_frame,
    text="Generate Password",
    width=160,
    height=42,
    font=("Segoe UI", 14, "bold"),
    command=generate_password
)
generate_btn.grid(row=0, column=1, padx=8, pady=8)

copy_btn = ctk.CTkButton(
    button_frame,
    text="Copy Password",
    width=160,
    height=42,
    font=("Segoe UI", 14, "bold"),
    command=copy_password
)
copy_btn.grid(row=1, column=0, padx=8, pady=8)

clear_btn = ctk.CTkButton(
    button_frame,
    text="Clear",
    width=160,
    height=42,
    font=("Segoe UI", 14, "bold"),
    fg_color="#d9534f",
    hover_color="#c9302c",
    command=clear_all
)
clear_btn.grid(row=1, column=1, padx=8, pady=8)

# -------------------- STRENGTH AREA --------------------
strength_title = ctk.CTkLabel(left_frame, text="Password Strength", font=("Segoe UI", 20, "bold"))
strength_title.pack(pady=(25, 8))

strength_value_label = ctk.CTkLabel(
    left_frame,
    text="Not Checked",
    font=("Segoe UI", 26, "bold"),
    text_color="white"
)
strength_value_label.pack(pady=(0, 10))

progress_bar = ctk.CTkProgressBar(left_frame, width=420, height=20)
progress_bar.set(0)
progress_bar.pack(pady=(5, 8))

percent_label = ctk.CTkLabel(left_frame, text="0% Secure", font=("Segoe UI", 14))
percent_label.pack(pady=(0, 20))

# -------------------- RIGHT SECTION --------------------
right_frame = ctk.CTkFrame(main_frame, corner_radius=16)
right_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

rules_title = ctk.CTkLabel(right_frame, text="Security Rules Checklist", font=("Segoe UI", 22, "bold"))
rules_title.pack(pady=(20, 15))

rules_container = ctk.CTkFrame(right_frame, fg_color="transparent")
rules_container.pack(pady=(0, 15))

rule_labels = {}
rules = [
    "At least 8 characters",
    "At least 12 characters",
    "Contains lowercase letter",
    "Contains uppercase letter",
    "Contains number",
    "Contains special character"
]

for rule in rules:
    lbl = ctk.CTkLabel(
        rules_container,
        text=f"• {rule}",
        font=("Segoe UI", 14),
        text_color="gray70",
        anchor="w"
    )
    lbl.pack(fill="x", padx=10, pady=5)
    rule_labels[rule] = lbl

feedback_title = ctk.CTkLabel(right_frame, text="Feedback / Suggestions", font=("Segoe UI", 22, "bold"))
feedback_title.pack(pady=(20, 10))

feedback_box = ctk.CTkTextbox(
    right_frame,
    width=360,
    height=250,
    font=("Segoe UI", 14),
    wrap="word"
)
feedback_box.pack(pady=(5, 20), padx=10)
feedback_box.configure(state="disabled")

# -------------------- FOOTER --------------------
footer = ctk.CTkLabel(
    app,
    text="Project: Password Strength Checker App using Python",
    font=("Segoe UI", 12),
    text_color="gray70"
)
footer.pack(pady=(0, 10))

# -------------------- RUN APP --------------------
app.mainloop()