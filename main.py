"""Sistem pakar sederhana dengan forward chaining (FC).
 
Membaca aturan IF-THEN dari kb_weatherwise.json, menanyakan fakta ke pengguna,
menjalankan aturan sampai tidak ada hasil baru, lalu menampilkan kesimpulan
beserta alasannya (aturan mana yang dipakai).
"""
import json
import sys
 
FILE_KB = "kb_weatherwise.json"
 
 
def muat_kb(nama_file):
    with open(nama_file, encoding="utf-8") as f:
        return json.load(f)
 
 
def syarat_terpenuhi(aturan, memori):
    """mode 'dan': semua syarat ada di memori; mode 'atau': salah satu cukup."""
    ada = [syarat in memori for syarat in aturan["jika"]]
    return all(ada) if aturan["mode"] == "dan" else any(ada)
 
 
def fakta_dasar(kb):
    """Fakta yang tidak pernah menjadi hasil aturan, jadi harus ditanyakan."""
    hasil = {a["maka"] for a in kb["aturan"]}
    dasar = []
    for a in kb["aturan"]:
        for syarat in a["jika"]:
            if syarat not in hasil and syarat not in dasar:
                dasar.append(syarat)
    return dasar
 
 
def tanya_fakta(dasar):
    """Tanya y/t untuk tiap fakta dasar; kembalikan fakta yang dijawab ya."""
    print("Jawab y/t.")
    ya = []
    for no, fakta in enumerate(dasar, start=1):
        while True:
            try:
                jawab = input(f"{no}. Apakah {fakta}? (y/t) > ").strip().lower()
            except EOFError:
                jawab = "t"
            if jawab in ("y", "t"):
                break
            print("   Ketik y atau t saja.")
        if jawab == "y":
            ya.append(fakta)
    return ya
 
 
def forward_chaining(daftar_aturan, fakta_awal):
    """Mesin FC: ulangi sampai tidak ada aturan cocok yang hasilnya belum ada."""
    memori = set(fakta_awal)
    asal = {}      # hasil -> (aturan, syarat yang terpakai saat aturan dijalankan)
    riwayat = []   # urutan aturan yang dijalankan
    while True:
        cocok = [a for a in daftar_aturan
                 if a["maka"] not in memori and syarat_terpenuhi(a, memori)]
        if not cocok:
            break
        r = cocok[0]                                   # ambil aturan pertama
        terpakai = [s for s in r["jika"] if s in memori]
        memori.add(r["maka"])
        asal[r["maka"]] = (r, terpakai)                # bahan "alasan"
        riwayat.append(r)
    return asal, riwayat
 
 
def kesimpulan_akhir(kb, asal):
    """Hasil aturan yang tidak dipakai sebagai syarat aturan lain."""
    dipakai = {s for a in kb["aturan"] for s in a["jika"]}
    return [hasil for hasil in asal if hasil not in dipakai]
 
 
def cetak_alasan(fakta, asal, tingkat=1):
    aturan, terpakai = asal[fakta]
    print("  " * tingkat + f"{fakta}  <- {aturan['id']} ({', '.join(terpakai)})")
    for syarat in terpakai:
        if syarat in asal:
            cetak_alasan(syarat, asal, tingkat + 1)
 
 
def main():
    kb = muat_kb(FILE_KB)
    print(kb["judul"])
    fakta_awal = tanya_fakta(fakta_dasar(kb))
 
    print()
    print("Fakta awal:", ", ".join(fakta_awal) if fakta_awal else "(tidak ada)")
    print()
 
    asal, riwayat = forward_chaining(kb["aturan"], fakta_awal)
    for no, r in enumerate(riwayat, start=1):
        print(f"Siklus {no}: {r['id']} -> {r['maka']}")
    print(f"Siklus {len(riwayat) + 1}: tidak ada aturan baru, berhenti")
    print()
 
    akhir = kesimpulan_akhir(kb, asal)
    if not akhir:
        print("Kesimpulan: tidak ada kesimpulan dari fakta yang diberikan")
    else:
        if len(akhir) == 1:
            print("Kesimpulan:", akhir[0])
        else:
            print("Kesimpulan:")
            for k in akhir:
                print("  -", k)
        print("Alasan:")
        for k in akhir:
            cetak_alasan(k, asal)
    print()
    print("Catatan:", kb["batas"])
 
 
if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print(f"File {FILE_KB} tidak ditemukan. Jalankan dari folder yang sama.")
        sys.exit(1)
