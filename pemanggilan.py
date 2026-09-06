import matematika

print("=== PROGRAM KALKULATOR MODULAR ===")

a = int(input("Masukkan angka pertama: "))
b = int(input("Masukkan angka kedua: "))

print("\nHasil Tambah :", matematika.tambah(a, b))
print("Hasil Kurang :", matematika.kurang(a, b))
print("Hasil Kali   :", matematika.kali(a, b))
print("Hasil Bagi   :", matematika.bagi(a, b))