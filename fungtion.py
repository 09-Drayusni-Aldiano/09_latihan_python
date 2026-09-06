def cek_ganjil_genap(angka):
    if angka % 2 == 0:
        return "GENAP"
    else:
        return "GANJIL"


for angka in range(1, 11):
    hasil = cek_ganjil_genap(angka)
    print(angka, "adalah bilangan", hasil)