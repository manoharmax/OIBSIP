
# password_manager.py - Version 4
# Features:
# Master Password Login, Encryption, Categories, Treeview,
# Add/Update/Delete, Import/Export, Password Generator

import os, json, random, string, re, hashlib, pyperclip
from tkinter import messagebox, filedialog, ttk
import customtkinter as ctk
from cryptography.fernet import Fernet

VAULT_DIR = "vault"
KEY_FILE = os.path.join(VAULT_DIR, "key.key")
DATA_FILE = os.path.join(VAULT_DIR, "passwords.enc")
MASTER_FILE = os.path.join(VAULT_DIR, "master.hash")

# ---------- Security ----------

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def master_exists():
    return os.path.exists(MASTER_FILE)

def save_master_password(p):
    with open(MASTER_FILE, "w") as f:
        f.write(hash_password(p))

def verify_master_password(p):
    with open(MASTER_FILE, "r") as f:
        return f.read() == hash_password(p)

def initialize_vault():
    os.makedirs(VAULT_DIR, exist_ok=True)
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "wb") as f:
            f.write(Fernet.generate_key())
    if not os.path.exists(DATA_FILE):
        save_data([])

def get_cipher():
    with open(KEY_FILE, "rb") as f:
        return Fernet(f.read())

def load_data():
    try:
        cipher = get_cipher()
        with open(DATA_FILE, "rb") as f:
            data = f.read()
        if not data:
            return []
        return json.loads(cipher.decrypt(data).decode())
    except Exception:
        return []

def save_data(data):
    cipher = get_cipher()
    enc = cipher.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, "wb") as f:
        f.write(enc)

# ---------- Password ----------

def password_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[^A-Za-z0-9]", password): score += 1
    return "Weak" if score <= 3 else "Medium" if score <= 5 else "Strong"

# ---------- Login ----------

def login():
    pwd = master_entry.get()
    if not pwd:
        return
    if not master_exists():
        save_master_password(pwd)
        login_window.destroy()
        launch_main_app()
        return
    if verify_master_password(pwd):
        login_window.destroy()
        launch_main_app()
    else:
        messagebox.showerror("Error", "Invalid master password")

# ---------- Main App ----------

def refresh_table(records=None):
    for row in tree.get_children():
        tree.delete(row)

    records = load_data() if records is None else records

    for i, item in enumerate(records):
        tree.insert("", "end", iid=str(i),
                    values=(item["website"], item["category"], item["username"]))

def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    pwd = ''.join(random.choice(chars) for _ in range(16))
    password_entry.delete(0, "end")
    password_entry.insert(0, pwd)
    strength_label.configure(text=f"Password Strength: {password_strength(pwd)}")

def add_credential():
    data = load_data()
    data.append({
        "website": website_entry.get(),
        "category": category_var.get(),
        "username": username_entry.get(),
        "password": password_entry.get()
    })
    save_data(data)
    refresh_table()

def selected_index():
    sel = tree.selection()
    if not sel:
        return None
    return int(sel[0])

def load_selected(event=None):
    idx = selected_index()
    if idx is None:
        return
    item = load_data()[idx]

    website_entry.delete(0, "end")
    website_entry.insert(0, item["website"])

    username_entry.delete(0, "end")
    username_entry.insert(0, item["username"])

    password_entry.delete(0, "end")
    password_entry.insert(0, item["password"])

    category_var.set(item["category"])

def update_credential():
    idx = selected_index()
    if idx is None:
        return

    data = load_data()
    data[idx] = {
        "website": website_entry.get(),
        "category": category_var.get(),
        "username": username_entry.get(),
        "password": password_entry.get()
    }

    save_data(data)
    refresh_table()

def delete_credential():
    idx = selected_index()
    if idx is None:
        return

    if not messagebox.askyesno("Confirm", "Delete selected credential?"):
        return

    data = load_data()
    data.pop(idx)
    save_data(data)
    refresh_table()

def search_credentials():
    q = search_entry.get().lower().strip()
    data = load_data()

    filtered = [
        x for x in data
        if q in x["website"].lower()
        or q in x["username"].lower()
        or q in x["category"].lower()
    ]
    refresh_table(filtered)

def export_vault():
    path = filedialog.asksaveasfilename(defaultextension=".json")
    if not path:
        return
    with open(path, "w") as f:
        json.dump(load_data(), f, indent=4)
    messagebox.showinfo("Success", "Vault exported")

def import_vault():
    path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if not path:
        return
    with open(path, "r") as f:
        data = json.load(f)
    save_data(data)
    refresh_table()
    messagebox.showinfo("Success", "Vault imported")

def copy_password():
    pyperclip.copy(password_entry.get())
    messagebox.showinfo("Copied", "Password copied")

def toggle_password():
    password_entry.configure(show="" if show_var.get() else "*")

def launch_main_app():
    global website_entry, username_entry, password_entry, search_entry
    global category_var, strength_label, tree, show_var

    app = ctk.CTk()
    app.geometry("1000x700")
    app.title("Secure Password Manager V4")

    ctk.CTkLabel(app, text="Secure Password Manager", font=("Arial", 28, "bold")).pack(pady=10)

    form = ctk.CTkFrame(app)
    form.pack(fill="x", padx=10, pady=10)

    website_entry = ctk.CTkEntry(form, placeholder_text="Website")
    website_entry.pack(pady=5)

    username_entry = ctk.CTkEntry(form, placeholder_text="Username")
    username_entry.pack(pady=5)

    password_entry = ctk.CTkEntry(form, placeholder_text="Password", show="*")
    password_entry.pack(pady=5)

    show_var = ctk.BooleanVar()
    ctk.CTkCheckBox(form, text="Show Password", variable=show_var,
                    command=toggle_password).pack()

    strength_label = ctk.CTkLabel(form, text="Password Strength: N/A")
    strength_label.pack()

    category_var = ctk.StringVar(value="Email")
    ctk.CTkOptionMenu(form, variable=category_var,
        values=["Email","Banking","Social Media","Shopping","Work","Other"]).pack(pady=5)

    ctk.CTkButton(form, text="Generate Password", command=generate_password).pack(pady=2)
    ctk.CTkButton(form, text="Copy Password", command=copy_password).pack(pady=2)
    ctk.CTkButton(form, text="Add Credential", command=add_credential).pack(pady=2)
    ctk.CTkButton(form, text="Update Credential", command=update_credential).pack(pady=2)
    ctk.CTkButton(form, text="Delete Credential", command=delete_credential).pack(pady=2)

    search_entry = ctk.CTkEntry(app, placeholder_text="Search")
    search_entry.pack(pady=5)

    ctk.CTkButton(app, text="Search", command=search_credentials).pack()
    ctk.CTkButton(app, text="Export Vault", command=export_vault).pack(pady=2)
    ctk.CTkButton(app, text="Import Vault", command=import_vault).pack(pady=2)

    tree = ttk.Treeview(app, columns=("Website","Category","Username"), show="headings", height=15)
    tree.heading("Website", text="Website")
    tree.heading("Category", text="Category")
    tree.heading("Username", text="Username")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    tree.bind("<<TreeviewSelect>>", load_selected)

    refresh_table()
    app.mainloop()

initialize_vault()

ctk.set_appearance_mode("dark")

login_window = ctk.CTk()
login_window.geometry("400x250")
login_window.title("Master Password Login")

ctk.CTkLabel(login_window, text="Master Password Login",
             font=("Arial", 20, "bold")).pack(pady=20)

master_entry = ctk.CTkEntry(login_window, show="*", width=250)
master_entry.pack(pady=10)

ctk.CTkButton(login_window, text="Login", command=login).pack(pady=10)

login_window.mainloop()
