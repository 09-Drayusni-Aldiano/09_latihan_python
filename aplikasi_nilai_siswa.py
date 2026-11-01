
import tkinter as tk
from tkinter import ttk, messagebox
import gspread

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1ORliwjOZalpMKjiOhqYfYBuHX2xLPPIAJfTfhRxJgDY/edit?gid=0#gid=0"

HEADERS = [
    "NIS", "Nama", "Kelas", "Tugas",
    "UTS", "UAS", "Nilai Akhir", "Status"
]

try:
    gc = gspread.service_account(
        filename="google_credentials.json"
    )

    spreadsheet = gc.open_by_url(SPREADSHEET_URL)
    sheet = spreadsheet.worksheet("DataSiswa")

    if not sheet.get_all_values():
        sheet.update(
            range_name="A1:H1",
            values=[HEADERS]
        )

except Exception as error:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Koneksi Gagal",
        f"Gagal menghubungkan Google Spreadsheet:\n{error}"
    )
    root.destroy()
    raise SystemExit

selected_nis = None

def hitung_nilai(tugas, uts, uas):
    nilai = tugas * 0.20 + uts * 0.30 + uas * 0.50
    status = "LULUS" if nilai >= 75 else "TIDAK LULUS"
    return round(nilai, 2), status


def tampil_data():
    for item in tabel.get_children():
        tabel.delete(item)

    try:
        data = sheet.get_all_values()

        for row in data[1:]:
            if len(row) >= 8:
                tabel.insert("", "end", values=row)

    except Exception as error:
        messagebox.showerror("Error", str(error))


def simpan_data():
    global selected_nis

    nis = entry_nis.get().strip()
    nama = entry_nama.get().strip()
    kelas = entry_kelas.get().strip()

    try:
        tugas = float(entry_tugas.get())
        uts = float(entry_uts.get())
        uas = float(entry_uas.get())

        if not all(0 <= n <= 100 for n in [tugas, uts, uas]):
            raise ValueError("Nilai harus antara 0 sampai 100.")

        if not nis or not nama or not kelas:
            messagebox.showwarning(
                "Peringatan", "Semua data harus diisi."
            )
            return

        nilai, status = hitung_nilai(tugas, uts, uas)

        data_lama = sheet.get_all_values()

        if selected_nis is None:
            for row in data_lama[1:]:
                if row and row[0] == nis:
                    messagebox.showwarning(
                        "Peringatan", "NIS sudah digunakan."
                    )
                    return

            sheet.append_row([
                nis, nama, kelas, tugas, uts,
                uas, nilai, status
            ])

            messagebox.showinfo(
                "Berhasil", "Data siswa berhasil disimpan."
            )

        else:
            nomor_baris = None

            for index, row in enumerate(data_lama[1:], start=2):
                if row and row[0] == selected_nis:
                    nomor_baris = index
                    break

            if nomor_baris is None:
                messagebox.showerror(
                    "Error", "Data siswa tidak ditemukan."
                )
                return

            for index, row in enumerate(data_lama[1:], start=2):
                if row and row[0] == nis and index != nomor_baris:
                    messagebox.showwarning(
                        "Peringatan", "NIS sudah digunakan."
                    )
                    return

            sheet.update(
                range_name=f"A{nomor_baris}:H{nomor_baris}",
                values=[[
                    nis, nama, kelas, tugas,
                    uts, uas, nilai, status
                ]]
            )

            messagebox.showinfo(
                "Berhasil", "Data siswa berhasil diperbarui."
            )

        bersihkan()
        tampil_data()

    except ValueError as error:
        messagebox.showwarning(
            "Input Tidak Valid",
            f"Masukkan nilai angka antara 0 sampai 100.\n{error}"
        )

    except Exception as error:
        messagebox.showerror("Error", str(error))


def pilih_data(event):
    global selected_nis

    pilihan = tabel.selection()

    if not pilihan:
        return

    data = tabel.item(pilihan[0], "values")

    selected_nis = data[0]

    entry_nis.delete(0, tk.END)
    entry_nis.insert(0, data[0])

    entry_nama.delete(0, tk.END)
    entry_nama.insert(0, data[1])

    entry_kelas.delete(0, tk.END)
    entry_kelas.insert(0, data[2])

    entry_tugas.delete(0, tk.END)
    entry_tugas.insert(0, data[3])

    entry_uts.delete(0, tk.END)
    entry_uts.insert(0, data[4])

    entry_uas.delete(0, tk.END)
    entry_uas.insert(0, data[5])


def hapus_data():
    global selected_nis

    if selected_nis is None:
        messagebox.showwarning(
            "Peringatan", "Pilih data yang ingin dihapus."
        )
        return

    konfirmasi = messagebox.askyesno(
        "Konfirmasi", "Yakin ingin menghapus data siswa ini?"
    )

    if not konfirmasi:
        return

    try:
        data = sheet.get_all_values()

        for index, row in enumerate(data[1:], start=2):
            if row and row[0] == selected_nis:
                sheet.delete_rows(index)
                break

        messagebox.showinfo(
            "Berhasil", "Data siswa berhasil dihapus."
        )

        bersihkan()
        tampil_data()

    except Exception as error:
        messagebox.showerror("Error", str(error))


def cari_data():
    keyword = entry_cari.get().strip().lower()

    for item in tabel.get_children():
        tabel.delete(item)

    try:
        data = sheet.get_all_values()

        for row in data[1:]:
            if len(row) >= 8:
                if keyword in row[0].lower() or keyword in row[1].lower():
                    tabel.insert("", "end", values=row)

    except Exception as error:
        messagebox.showerror("Error", str(error))


def bersihkan():
    global selected_nis
    selected_nis = None

    for entry in [
        entry_nis, entry_nama, entry_kelas,
        entry_tugas, entry_uts, entry_uas
    ]:
        entry.delete(0, tk.END)


root = tk.Tk()
root.title("Aplikasi Nilai Siswa")
root.geometry("1050x650")
root.configure(bg="#EAF2F8")

judul = tk.Label(
    root,
    text="APLIKASI NILAI SISWA",
    font=("Arial", 22, "bold"),
    bg="#EAF2F8",
    fg="#1A5276"
)
judul.pack(pady=15)

frame_form = tk.LabelFrame(
    root,
    text="Form Data Siswa",
    font=("Arial", 12, "bold"),
    bg="#EAF2F8",
    padx=15,
    pady=15
)
frame_form.pack(fill="x", padx=20)

labels = [
    "NIS", "Nama", "Kelas",
    "Nilai Tugas", "Nilai UTS", "Nilai UAS"
]

entries = []

for i, label in enumerate(labels):
    row = i // 3
    col = (i % 3) * 2

    tk.Label(
        frame_form,
        text=label,
        bg="#EAF2F8",
        font=("Arial", 10)
    ).grid(row=row, column=col, padx=8, pady=8, sticky="w")

    entry = tk.Entry(frame_form, width=22)
    entry.grid(row=row, column=col + 1, padx=8, pady=8)

    entries.append(entry)

entry_nis = entries[0]
entry_nama = entries[1]
entry_kelas = entries[2]
entry_tugas = entries[3]
entry_uts = entries[4]
entry_uas = entries[5]

frame_tombol = tk.Frame(root, bg="#EAF2F8")
frame_tombol.pack(pady=12)

tk.Button(
    frame_tombol, text="Simpan Data",
    width=15, command=simpan_data,
    bg="#2471A3", fg="white"
).grid(row=0, column=0, padx=5)

tk.Button(
    frame_tombol, text="Hapus Data",
    width=15, command=hapus_data,
    bg="#C0392B", fg="white"
).grid(row=0, column=1, padx=5)

tk.Button(
    frame_tombol, text="Bersihkan",
    width=15, command=bersihkan,
    bg="#7F8C8D", fg="white"
).grid(row=0, column=2, padx=5)

tk.Button(
    frame_tombol, text="Tampilkan Semua",
    width=17, command=tampil_data,
    bg="#239B56", fg="white"
).grid(row=0, column=3, padx=5)

frame_cari = tk.Frame(root, bg="#EAF2F8")
frame_cari.pack(pady=8)

tk.Label(
    frame_cari,
    text="Cari NIS atau Nama:",
    bg="#EAF2F8"
).pack(side="left", padx=5)

entry_cari = tk.Entry(frame_cari, width=30)
entry_cari.pack(side="left", padx=5)

tk.Button(
    frame_cari,
    text="Cari",
    command=cari_data
).pack(side="left", padx=5)

frame_tabel = tk.Frame(root)
frame_tabel.pack(fill="both", expand=True, padx=20, pady=10)

kolom = (
    "NIS", "Nama", "Kelas", "Tugas",
    "UTS", "UAS", "Nilai Akhir", "Status"
)

tabel = ttk.Treeview(
    frame_tabel,
    columns=kolom,
    show="headings"
)

for kolom_nama in kolom:
    tabel.heading(kolom_nama, text=kolom_nama)
    tabel.column(kolom_nama, width=115, anchor="center")

scrollbar = ttk.Scrollbar(
    frame_tabel,
    orient="vertical",
    command=tabel.yview
)

tabel.configure(yscrollcommand=scrollbar.set)

tabel.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tabel.bind("<<TreeviewSelect>>", pilih_data)

tampil_data()

root.mainloop()