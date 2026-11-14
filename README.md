# ⛅ Tugas 5 AI: WeatherWise
### Sistem Pakar Identifikasi Kondisi Cuaca

👤 **Nama:** Zhylalan Wahyu Ramadhani
🎓 **NIM:** F1D02510137

## 🎯 Topik dan cara menjalankan

Topik: mengenali kondisi cuaca (cerah, cerah berawan, berawan, berawan tebal, hujan lebat, dan potensi hujan lebat disertai petir) dari pengamatan langit, kelembapan udara, dan curah hujan. Program (nama aplikasi: WeatherWise) bertanya kondisi yang teramati (y/t), lalu menyimpulkan kondisi cuaca beserta alasannya.

- 🐍 Bahasa: Python 3 (diuji dengan Python 3.15.2). Hanya memakai modul bawaan (`json`, `sys`), tanpa instalasi.
- ▶️ Menjalankan (di folder yang berisi `main.py` dan `kb_weatherwise.json`):

```
python main.py
```

📁 Struktur repository:

```
ai-tugas5-weatherwise/
├── kb_weatherwise.json   (aturan IF-THEN + sumber)
├── main.py               (mesin forward chaining)
├── README.md
└── screenshot/           (bukti 3 kasus uji)

## 📚 Sumber

| ID | Judul | Penerbit | URL | Diakses |
|---|---|---|---|---|
| S1 | Penggunaan Jenis dan Simbol Parameter Prakiraan Cuaca, Simbol Parameter Arah Angin, dan Simbol Parameter Indeks Ultraviolet (SE.3/DM/XII/2024), 2024 | Deputi Bidang Meteorologi, BMKG | https://jdih.bmkg.go.id/common/dokumen/2024sedmbmkg003.pdf | 14 Nov 2026 |
| S2 | Kajian Dinamika Atmosfer saat Kejadian Hujan Lebat di Wilayah Pesisir Timur Sumatera Utara Menggunakan Model WRF-ARW dan Citra Satelit Himawari-8 (Saragih dkk.), Unnes Physics Journal Vol. 6 No. 1, 2018 | Universitas Negeri Semarang | https://journal.unnes.ac.id/sju/upj/article/view/21895/10397 | 14 Nov 2026 |
| S3 | Indeks Labilitas Udara untuk Memprediksi Kejadian Badai Guntur pada Puncak Musim Hujan Tahun 2016 (Zahroh dkk.), Jurnal Sains & Teknologi Modifikasi Cuaca Vol. 18 No. 1, 2017 | Badan Riset dan Inovasi Nasional (BRIN) | https://ejournal.brin.go.id/JSTMC/article/download/1307/727/4661 | 14 Nov 2026 |

## 📋 Tabel aturan

| Aturan | IF | THEN | Sumber |
|---|---|---|---|
| R1 | kelembapan udara 70% atau lebih AND udara permukaan terasa hangat dan lembap | atmosfer lembap dan mendukung awan hujan | S2, S3 |
| R2 | atmosfer lembap dan mendukung awan hujan AND terlihat awan gelap pekat bertekstur seperti bunga kol (Cumulonimbus) | berpotensi hujan lebat disertai petir | S2, S3 |
| R3 | curah hujan 50 sampai 100 mm per hari OR curah hujan 10 sampai 20 mm per jam | hujan lebat | S1 |
| R4 | langit tidak tertutup awan atau tutupan awan kurang dari 10% | cuaca cerah | S1 |
| R5 | tutupan awan sekitar 10 sampai 60% | cuaca cerah berawan | S1 |
| R6 | tutupan awan sekitar 60 sampai 90% | cuaca berawan | S1 |
| R7 | tutupan awan sekitar 90% | cuaca berawan tebal | S1 |
| R8 | tutupan awan sekitar 90% AND kelembapan udara 70% atau lebih | ada kemungkinan hujan, siapkan payung | S1, S2 |

🔗 Rantai aturan: R1 menghasilkan "atmosfer lembap dan mendukung awan hujan" yang dipakai R2. Ada 7 kesimpulan akhir (R2, R3, R4, R5, R6, R7, R8).

Catatan: R1 dan R8 adalah penafsiran penulis atas isi sumber (S2 mencatat kelembapan relatif 70% atau lebih pada fase tumbuh awan Cumulonimbus; S3 menyebut badai guntur terbentuk dari udara hangat dan lembap yang naik). Hal ini juga tertulis di kolom `catatan` file JSON. Angka tutupan awan dan kategori curah hujan (R3 sampai R7) diambil langsung dari S1.

## ⚙️ Metode: Forward Chaining (FC)

💡 Alasan memilih FC: kondisi cuaca diamati langsung (langit, kelembapan, hujan), jadi fakta sudah ada lebih dulu, lalu dicari kesimpulan apa saja yang berlaku. Satu keadaan bisa menghasilkan lebih dari satu kesimpulan, misalnya berawan tebal sekaligus kemungkinan hujan.

🔧 Langkah mesin (ditulis sendiri di `main.py`):

1. Program menanyakan fakta dasar (fakta yang tidak pernah menjadi hasil aturan); jawaban "ya" masuk ke memori.
2. Cari aturan yang syaratnya terpenuhi oleh memori dan hasilnya belum ada di memori. Mode "dan": semua syarat ada; mode "atau": salah satu cukup.
3. Jika tidak ada, berhenti. Jika ada, ambil aturan pertama, tambahkan hasilnya ke memori, dan catat aturan asalnya.
4. Ulangi dari langkah 2.
5. Kesimpulan akhir adalah hasil aturan yang tidak dipakai sebagai syarat aturan lain. Alasan ditampilkan dengan menelusuri aturan asal ke belakang.

## 🧪 Tiga kasus uji

Urutan pertanyaan: 1 kelembapan udara 70% atau lebih, 2 udara permukaan terasa hangat dan lembap, 3 terlihat awan gelap pekat bertekstur seperti bunga kol (Cumulonimbus), 4 curah hujan 50 sampai 100 mm per hari, 5 curah hujan 10 sampai 20 mm per jam, 6 langit tidak tertutup awan atau tutupan awan kurang dari 10%, 7 tutupan awan sekitar 10 sampai 60%, 8 tutupan awan sekitar 60 sampai 90%, 9 tutupan awan sekitar 90%.

| # | Jawaban "ya" (nomor pertanyaan) | Kesimpulan |
|---|---|---|
| 1 | 1, 2, dan 3 | berpotensi hujan lebat disertai petir (R2, lewat R1) |
| 2 | 1, 2, dan 9 | cuaca berawan tebal (R7); ada kemungkinan hujan, siapkan payung (R8) |
| 3 | 2 saja (kasus negatif) | tidak ada kesimpulan |

Kasus 3 tidak menghasilkan kesimpulan karena udara hangat dan lembap saja belum cukup; harus ada kelembapan 70% atau lebih (R1) dan pengamatan awan. Ini bukan berarti cuaca pasti baik.

✅ Kasus 1:

![Kasus 1](screenshoot/kasus1.png
)

✅ Kasus 2:

![Kasus 2](screenshoot/kasus2.png
)

🚫 Kasus 3 (tidak ada kesimpulan):

![Kasus 3](screenshoot/kasus3
)

## ⚠️ Batas keberlakuan

Pengetahuan dalam program ini berasal dari tiga dokumen: surat edaran BMKG tentang parameter prakiraan cuaca (SE.3/DM/XII/2024) untuk kategori tutupan awan dan curah hujan, jurnal Unnes Physics Journal (Saragih dkk., 2018) tentang hujan lebat dan awan Cumulonimbus, serta jurnal Sains & Teknologi Modifikasi Cuaca (Zahroh dkk., 2017) tentang badai guntur, yang dirangkum penulis menjadi aturan sederhana. Aturan berlaku untuk pengamatan cuaca di wilayah tropis Indonesia; ambang kelembapan berasal dari kajian di pesisir timur Sumatera Utara dan hanya perkiraan untuk tempat lain. Program tidak mengukur data atmosfer atas (radiosonde, satelit) dan tidak memberi peringatan dini; kategori tutupan awan hanya dari pengamatan langit, jadi bisa meleset. Jawaban "tidak ada kesimpulan" tidak berarti cuaca aman. Hasilnya adalah saran awal, bukan keputusan akhir: ikuti prakiraan dan peringatan resmi BMKG. Catatan yang sama ditampilkan di akhir keluaran program.

## 🤖 Penggunaan Alat Bantu AI

Dalam pengerjaan tugas ini, saya menggunakan **Claude (Anthropic)** dan **Gemini (Google)** sebagai alat bantu dalam proses pembelajaran dan pengembangan program. Claude digunakan untuk membantu memahami struktur dan kerangka penyusunan file JSON serta memberikan penjelasan mengenai penerapan aturan IF-THEN. Sementara itu, Gemini digunakan untuk membantu mencari ide dan memberikan referensi awal terkait pemilihan topik sistem pakar. 

Seluruh proses penyusunan aturan, penyesuaian program, serta pengujian hasil dilakukan dengan pemahaman dan pemeriksaan kembali secara mandiri.
