# 📝 Aplikasi Pencarian Kosakata Aksara Jawa

Aplikasi ini memungkinkan pengguna untuk mencari kosakata dalam Aksara Jawa berdasarkan input dalam bentuk aksara, latin, atau bahasa Indonesia. Aplikasi ini terhubung dengan GraphDB untuk mendapatkan data kosakata yang telah ditetapkan dalam bentuk RDF.

## 🌐 Link Aplikasi

🔗 [Buka Aplikasi di Sini](https://shervina22001-semweb-aksara-jawa-slnggi.streamlit.app/)

## 🚀 Fitur Utama

- 🔍 Pencarian kosakata berdasarkan aksara, latin, atau bahasa Indonesia.
- 🧠 Menampilkan hasil dalam tiga bentuk: **Aksara Jawa**, **Latin**, dan **Indonesia**.
- ✍️ Menyediakan **contoh kalimat** dari kosakata yang dicari.
- 🔗 Terintegrasi dengan **GraphDB** untuk pengambilan data RDF.

## 🛠️ Cara Penggunaan

1. **Buka Aplikasi**  
   Klik link berikut untuk membuka aplikasi:  
   👉 [https://shervina22001-semweb-aksara-jawa-slnggi.streamlit.app/](https://shervina22001-semweb-aksara-jawa-slnggi.streamlit.app/)

2. **Tes Koneksi ke GraphDB**  
   Klik tombol **"Test Koneksi GraphDB"**.  
   Jika berhasil, akan muncul pesan:  
   ✅ _"Koneksi Berhasil!"_

3. **Lakukan Pencarian**  
   - Masukkan kata yang ingin dicari pada kolom pencarian (bisa dalam bentuk aksara Jawa, latin, atau bahasa Indonesia).
   - Klik tombol **"Cari"**.

4. **Lihat Hasil**  
   - Hasil pencarian akan ditampilkan dalam tiga bentuk:
     - ✨ Aksara Jawa
     - 🔤 Latin
     - 🇮🇩 Bahasa Indonesia
   - Ditampilkan juga **contoh kalimat** dari kosakata tersebut.

## 📦 Teknologi yang Digunakan

- [Streamlit](https://streamlit.io/) — Untuk antarmuka pengguna web
- [GraphDB](https://www.ontotext.com/products/graphdb/) — Sebagai RDF triple store untuk penyimpanan data kosakata
- SPARQL — Bahasa query untuk mengambil data RDF

## 💡 Catatan Tambahan

Pastikan koneksi internet stabil saat menggunakan aplikasi karena aplikasi memerlukan akses ke GraphDB yang di-host secara online.


