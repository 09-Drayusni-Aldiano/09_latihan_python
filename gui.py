import tkinter as tk
from tkinter import messagebox
import os

def buka_create():
    frame_login.pack_forget()
    frame_create.pack(pady=30)

def buka_login():
    frame_create.pack_forget()
    frame_login.pack(pady=30)

def create_account():
    username = entry_create_user.get()
    password = entry_create_pass.get()

    if username == "" or password == "":
        messagebox.showwarning(
            "Peringatan",
            "Username dan Password harus diisi!"
        )
        return

    if os.path.exists("akun.txt"):
        with open("akun.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")

                if len(data) == 2:
                    user, pw = data

                    if user == username:
                        messagebox.showerror(
                            "Gagal",
                            "Username sudah digunakan!"
                        )
                        return

    with open("akun.txt", "a") as file:
        file.write(f"{username},{password}\n")

    messagebox.showinfo(
        "Berhasil",
        "Akun berhasil dibuat!"
    )

    entry_create_user.delete(0, tk.END)
    entry_create_pass.delete(0, tk.END)

    buka_login()

def login():
    username = entry_login_user.get()
    password = entry_login_pass.get()

    if not os.path.exists("akun.txt"):
        messagebox.showerror(
            "Error",
            "Belum ada akun yang terdaftar!"
        )
        return

    with open("akun.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")

            if len(data) == 2:
                user, pw = data

                if username == user and password == pw:
                    frame_login.pack_forget()

                    lbl_user.config(
                        text=f"Selamat Datang, {username}"
                    )

                    frame_menu.pack(pady=30)
                    return

    messagebox.showerror(
        "Login Gagal",
        "Username atau Password salah!"
    )

def cek_bilangan():
    try:
        angka = int(entry_angka.get())

        if angka % 2 == 0:
            hasil.config(
                text=f"Hasil: {angka} merupakan bilangan GENAP"
            )
        else:
            hasil.config(
                text=f"Hasil: {angka} merupakan bilangan GANJIL"
            )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Masukkan angka yang valid!"
        )

def logout():
    frame_menu.pack_forget()

    entry_login_user.delete(0, tk.END)
    entry_login_pass.delete(0, tk.END)
    entry_angka.delete(0, tk.END)

    hasil.config(text="")

    frame_login.pack(pady=30)

window = tk.Tk()
window.title("Aplikasi Cek Ganjil Genap")
window.geometry("600x500")
window.resizable(False, False)

BG_COLOR = "#EAF4FF"
FRAME_COLOR = "#FFFFFF"
TITLE_COLOR = "#2C3E50"

window.configure(bg=BG_COLOR)

frame_login = tk.Frame(
    window,
    bg=FRAME_COLOR,
    padx=30,
    pady=30
)

tk.Label(
    frame_login,
    text="🔐 HALAMAN LOGIN",
    font=("Segoe UI", 18, "bold"),
    bg=FRAME_COLOR,
    fg=TITLE_COLOR
).pack(pady=15)

tk.Label(
    frame_login,
    text="Username",
    font=("Segoe UI", 11),
    bg=FRAME_COLOR
).pack()

entry_login_user = tk.Entry(
    frame_login,
    font=("Segoe UI", 11),
    width=30,
    bd=2,
    relief="solid"
)
entry_login_user.pack(pady=5)

tk.Label(
    frame_login,
    text="Password",
    font=("Segoe UI", 11),
    bg=FRAME_COLOR
).pack()

entry_login_pass = tk.Entry(
    frame_login,
    show="*",
    font=("Segoe UI", 11),
    width=30,
    bd=2,
    relief="solid"
)
entry_login_pass.pack(pady=5)

tk.Button(
    frame_login,
    text="Login",
    width=20,
    bg="#3498DB",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=login
).pack(pady=10)

tk.Button(
    frame_login,
    text="Create Account",
    width=20,
    bg="#27AE60",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=buka_create
).pack()

frame_create = tk.Frame(
    window,
    bg=FRAME_COLOR,
    padx=30,
    pady=30
)

tk.Label(
    frame_create,
    text="📝 CREATE ACCOUNT",
    font=("Segoe UI", 18, "bold"),
    bg=FRAME_COLOR,
    fg=TITLE_COLOR
).pack(pady=15)

tk.Label(
    frame_create,
    text="Username Baru",
    font=("Segoe UI", 11),
    bg=FRAME_COLOR
).pack()

entry_create_user = tk.Entry(
    frame_create,
    font=("Segoe UI", 11),
    width=30,
    bd=2,
    relief="solid"
)
entry_create_user.pack(pady=5)

tk.Label(
    frame_create,
    text="Password Baru",
    font=("Segoe UI", 11),
    bg=FRAME_COLOR
).pack()

entry_create_pass = tk.Entry(
    frame_create,
    show="*",
    font=("Segoe UI", 11),
    width=30,
    bd=2,
    relief="solid"
)
entry_create_pass.pack(pady=5)

tk.Button(
    frame_create,
    text="Simpan Akun",
    width=20,
    bg="#27AE60",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=create_account
).pack(pady=10)

tk.Button(
    frame_create,
    text="Kembali ke Login",
    width=20,
    bg="#E67E22",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=buka_login
).pack()

frame_menu = tk.Frame(
    window,
    bg=FRAME_COLOR,
    padx=30,
    pady=30
)

tk.Label(
    frame_menu,
    text="🔢 APLIKASI CEK GANJIL / GENAP",
    font=("Segoe UI", 16, "bold"),
    bg=FRAME_COLOR,
    fg=TITLE_COLOR
).pack(pady=10)

lbl_user = tk.Label(
    frame_menu,
    text="",
    font=("Segoe UI", 12, "bold"),
    bg=FRAME_COLOR,
    fg="#2980B9"
)
lbl_user.pack(pady=10)

tk.Label(
    frame_menu,
    text="Masukkan Bilangan",
    font=("Segoe UI", 11),
    bg=FRAME_COLOR
).pack()

entry_angka = tk.Entry(
    frame_menu,
    font=("Segoe UI", 12),
    width=25,
    bd=2,
    relief="solid"
)
entry_angka.pack(pady=10)

tk.Button(
    frame_menu,
    text="Cek Bilangan",
    width=20,
    bg="#9B59B6",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=cek_bilangan
).pack()

hasil = tk.Label(
    frame_menu,
    text="",
    font=("Segoe UI", 12, "bold"),
    bg=FRAME_COLOR,
    fg="#16A085"
)
hasil.pack(pady=20)

tk.Button(
    frame_menu,
    text="Logout",
    width=20,
    bg="#E74C3C",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=logout
).pack()

frame_login.pack(pady=30)

window.mainloop()