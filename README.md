# 📜 Pencarian Naskah Jawa – Wedhus lan Asu Ajag

Aplikasi web interaktif untuk menelusuri kosakata Aksara Jawa beserta transliterasi Latin, terjemahan Bahasa Indonesia, dan contoh kalimat berdasarkan data RDF. Proyek ini menggabungkan teknologi Semantic Web menggunakan GraphDB, SPARQL, dan Streamlit, serta menampilkan data dengan visualisasi yang ramah pengguna.

---

## 🚀 Fitur Utama

* **🔍 Pencarian Kosakata Fleksibel**: Cari kata dalam bentuk Aksara Jawa, Latin, atau Bahasa Indonesia. Pencarian tidak peka huruf besar/kecil (case-insensitive).
* **📖 Tampilan Hasil Terstruktur**: Setiap hasil ditampilkan dalam format kartu yang jelas, memisahkan transliterasi Latin, Aksara Jawa, arti, dan contoh kalimat.
* **🧠 Integrasi Semantic Web**: Menggunakan GraphDB sebagai basis data RDF dan SPARQL untuk melakukan query data secara semantik.
* **🖼️ Desain Khas Jawa**: Antarmuka pengguna dirancang dengan tema warna dan gaya yang terinspirasi dari naskah Jawa kuno untuk pengalaman yang lebih mendalam.
* **🧪 Tes Koneksi Langsung**: Fitur di sidebar untuk menguji konektivitas ke endpoint SPARQL GraphDB secara langsung dari aplikasi, memudahkan proses setup dan debugging.

---

## 🧰 Tumpukan Teknologi (Tech Stack)

* **Frontend & Logika Aplikasi**: Streamlit (Python)
* **Basis Data**: GraphDB (RDF Triple Store)
* **Bahasa Query**: SPARQL
* **Pustaka Python**: `requests` (untuk HTTP request), `pandas`
* **Deployment & Exposing Lokal**: Ngrok (opsional, untuk mengekspos GraphDB lokal ke internet)
* **Desain UI**: CSS kustom yang di-embed dalam Streamlit

---

## 📦 Cara Menjalankan Aplikasi

1.  **Jalankan GraphDB**:
    * Pastikan GraphDB sudah terinstal dan berjalan di mesin Anda.
    * Buat sebuah repository (misalnya, `Semweb`) dan pastikan repository tersebut aktif.
    * Impor data RDF Anda ke dalam repository ini.

2.  **Ekspos GraphDB (Opsional)**:
    * Jika Anda ingin aplikasi diakses dari mana saja atau saat mendeploy, ekspos port GraphDB (biasanya `7200`) menggunakan ngrok.
    * ```bash
      ngrok http 7200
      ```
    * Salin URL `https://...` yang diberikan oleh ngrok.

3.  **Siapkan Proyek**:
    * Clone repositori ini ke komputer Anda.
    * Instal semua pustaka Python yang dibutuhkan:
    * ```bash
      pip install streamlit requests pandas
      ```

4.  **Jalankan Aplikasi Streamlit**:
    * Buka terminal di direktori proyek dan jalankan perintah:
    * ```bash
      streamlit run app.py
      ```

5.  **Konfigurasi Endpoint**:
    * Setelah aplikasi terbuka di browser, buka sidebar.
    * Masukkan URL endpoint SPARQL GraphDB Anda (misalnya, URL dari ngrok atau `http://localhost:7200/repositories/Semweb`) ke dalam kolom input.
    * Gunakan tombol "Tes Koneksi" untuk memastikan semuanya terhubung dengan benar.

---

## 🔗 Contoh Struktur Data RDF

Aplikasi ini mengharapkan data RDF dengan struktur seperti di bawah ini agar query SPARQL dapat berjalan dengan benar.

```turtle
@prefix jawa: [http://example.org/jawa#](http://example.org/jawa#) .
@prefix rdf: [http://www.w3.org/1999/02/22-rdf-syntax-ns#](http://www.w3.org/1999/02/22-rdf-syntax-ns#) .

:kata_wedhus a jawa:Kata ;
  jawa:memilikiAksara "ꦮꦼꦣꦸꦱ꧀" ;
  jawa:ditulisDenganLatin "wedhus" ;
  jawa:berartiDalamBahasaIndonesia "kambing" ;
  jawa:memilikiContohKalimatIndonesia "Ibu memiliki seekor kambing." ;
  jawa:memilikiContohKalimatLatin "Ibu duwe wedhus siji." ;
  jawa:memilikiContohKalimatAksara "ꦲꦶꦧꦸꦢꦸꦮꦺꦮꦺꦣꦸꦱ꧀ꦱꦶꦗꦶ" .

:kata_asu_ajag a jawa:Kata ;
  jawa:memilikiAksara "ꦲꦱꦸꦲꦗꦒ꧀" ;
  jawa:ditulisDenganLatin "asu ajag" ;
  jawa:berartiDalamBahasaIndonesia "serigala" ;
  jawa:memilikiContohKalimatIndonesia "Serigala itu sangat lapar." ;
  jawa:memilikiContohKalimatLatin "Asu ajag iku luwe banget." ;
  jawa:memilikiContohKalimatAksara "ꦲꦱꦸꦲꦗꦒ꧀ꦲꦶꦏꦸꦭꦸꦮꦺꦧꦔꦼꦠ꧀" .

📸 Tampilan Antarmuka
(Disarankan untuk menambahkan screenshot aplikasi di sini untuk menunjukkan tampilan UI)

📁 Struktur Folder Proyek
.
├── app.py                # File utama aplikasi Streamlit
├── data/                 # Folder untuk menyimpan file RDF (opsional)
│   └── naskah.ttl
└── README.md             # Dokumentasi proyek ini
