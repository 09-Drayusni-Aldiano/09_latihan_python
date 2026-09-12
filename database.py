import gspread
from google.oauth2.service_account import Credentials

# =========================
# KONEKSI GOOGLE SHEETS
# =========================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open("database").sheet1


# =========================
# MEMBUAT HEADER
# =========================

if sheet.cell(1, 1).value == "":
    sheet.update("A1:B1", [["username", "password"]])


# =========================
# FUNGSI LOGIN
# =========================

def login():
    username = input("Username : ")
    password = input("Password : ")

    data = sheet.get_all_values()

    for baris in data[1:]:
        if len(baris) >= 2:
            if baris[0] == username and baris[1] == password:
                print("\nLogin berhasil!")
                print("Selamat datang,", username)
                return True

    print("\nUsername atau password salah!")
    return False


# =========================
# FUNGSI BUAT AKUN
# =========================

def buat_akun():
    username = input("Username baru : ")
    password = input("Password baru : ")

    data = sheet.get_all_values()

    # Mengecek username
    for baris in data[1:]:
        if len(baris) >= 1:
            if baris[0] == username:
                print("Username sudah digunakan!")
                return

    # Menyimpan akun ke Google Sheets
    sheet.append_row([username, password])

    print("\nAkun berhasil dibuat!")


# =========================
# MENU LOGIN
# =========================

while True:
    print("\n===== MENU LOGIN =====")
    print("1. Login")
    print("2. Buat Akun")
    print("3. Keluar")
    print("======================")

    pilihan = input("Pilih menu : ")

    if pilihan == "1":
        if login():
            break

    elif pilihan == "2":
        buat_akun()

    elif pilihan == "3":
        print("Program selesai.")
        break

    else:
        print("Pilihan tidak tersedia!")