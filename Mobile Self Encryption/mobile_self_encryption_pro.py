import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# ------------------ KEY GENERATION ------------------

def generate_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# ------------------ PASSWORD STRENGTH ------------------

def check_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char in "!@#$%^&*()" for char in password):
        score += 1

    levels = ["Weak", "Medium", "Strong", "Very Strong"]
    if score == 0:
        strength_label.config(text="Strength: Weak", fg="red")
    else:
        strength_label.config(text=f"Strength: {levels[score-1]}", fg="lime")

# ------------------ FILE SELECT ------------------

def select_file():
    path = filedialog.askopenfilename()
    if path:
        file_path.set(path)
        size = os.path.getsize(path) / 1024
        size_label.config(text=f"File Size: {size:.2f} KB")

# ------------------ ENCRYPT ------------------

def encrypt_file():
    path = file_path.get()
    password = password_entry.get()

    if not path or not password:
        messagebox.showerror("Error", "Select file and enter password!")
        return

    progress.start()

    try:
        salt = os.urandom(16)
        key = generate_key(password, salt)
        fernet = Fernet(key)

        with open(path, 'rb') as file:
            data = file.read()

        encrypted = fernet.encrypt(data)

        with open(path + ".enc", 'wb') as encrypted_file:
            encrypted_file.write(salt + encrypted)

        progress.stop()
        messagebox.showinfo("Success", "File Encrypted Successfully!")

    except Exception as e:
        progress.stop()
        messagebox.showerror("Error", str(e))

# ------------------ DECRYPT ------------------

def decrypt_file():
    path = file_path.get()
    password = password_entry.get()

    if not path or not password:
        messagebox.showerror("Error", "Select file and enter password!")
        return

    progress.start()

    try:
        with open(path, 'rb') as file:
            file_data = file.read()

        salt = file_data[:16]
        encrypted_data = file_data[16:]

        key = generate_key(password, salt)
        fernet = Fernet(key)

        decrypted = fernet.decrypt(encrypted_data)

        output_path = path.replace(".enc", "_decrypted")

        with open(output_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)

        progress.stop()
        messagebox.showinfo("Success", "File Decrypted Successfully!")

    except:
        progress.stop()
        messagebox.showerror("Error", "Incorrect Password or Corrupted File!")

# ------------------ SHOW/HIDE PASSWORD ------------------

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
    else:
        password_entry.config(show='*')

# ------------------ GUI SETUP ------------------

root = tk.Tk()
root.title("Mobile Self Encryption Pro")
root.geometry("520x450")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

file_path = tk.StringVar()

title = tk.Label(root, text="🔐 Mobile Self Encryption Pro",
                 font=("Arial", 18, "bold"), bg="#1e1e1e", fg="cyan")
title.pack(pady=15)

file_frame = tk.Frame(root, bg="#1e1e1e")
file_frame.pack(pady=10)

tk.Entry(file_frame, textvariable=file_path, width=40).grid(row=0, column=0, padx=5)
tk.Button(file_frame, text="Browse", command=select_file).grid(row=0, column=1)

size_label = tk.Label(root, text="File Size: 0 KB", bg="#1e1e1e", fg="white")
size_label.pack()

tk.Label(root, text="Enter Password:", bg="#1e1e1e", fg="white").pack(pady=5)

password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack()

password_entry.bind("<KeyRelease>", lambda event: check_strength(password_entry.get()))

tk.Button(root, text="Show/Hide Password", command=toggle_password).pack(pady=5)

strength_label = tk.Label(root, text="Strength: ", bg="#1e1e1e")
strength_label.pack()

progress = ttk.Progressbar(root, mode="indeterminate", length=300)
progress.pack(pady=15)

button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Encrypt File", command=encrypt_file,
          bg="green", fg="white", width=15).grid(row=0, column=0, padx=10)

tk.Button(button_frame, text="Decrypt File", command=decrypt_file,
          bg="blue", fg="white", width=15).grid(row=0, column=1, padx=10)

footer = tk.Label(root, text="Secure AES Encryption | PBKDF2 | 100k Iterations",
                  bg="#1e1e1e", fg="gray")
footer.pack(pady=20)

root.mainloop()