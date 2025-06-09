import streamlit as st
import requests
import pandas as pd
import json
from urllib.parse import quote

# Konfigurasi halaman
st.set_page_config(
    page_title="Pencarian Naskah Jawa - Wedhus lan Asu Ajag",
    page_icon="📜",
    layout="wide"
)

# Custom CSS dari skrip pertama
st.markdown("""
<style>
    /* Color Palette Variables */
    :root {
        --primary-dark: #5D8736;
        --primary: #809D3C;
        --primary-light: #A9C46C;
        --accent-light: #F4FFC3;
        --secondary: #B0DB9C;
        --background-light: #DDF6D2;
        --background-medium: #CAE8BD;
        --background-secondary: #B0DB9C;
    }
   
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #DDF6D2 0%, #F4FFC3 100%);
    }
   
    /* Header styling (digunakan oleh main() dari skrip kedua) */
    .main-header {
        background: linear-gradient(135deg, #5D8736 0%, #809D3C 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(93, 135, 54, 0.3);
    }
   
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
   
    .main-header p {
        color: #F4FFC3;
        margin: 10px 0 0 0;
        font-size: 1.2rem;
        font-style: italic;
    }
   
    /* Search container */
    .search-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(93, 135, 54, 0.1);
        border: 2px solid #CAE8BD;
    }
   
    /* Result cards */
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 6px 25px rgba(93, 135, 54, 0.15);
        border-left: 5px solid #809D3C;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
   
    .result-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 35px rgba(93, 135, 54, 0.25);
    }
   
    .result-header {
        background: linear-gradient(135deg, #A9C46C 0%, #809D3C 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
   
    .result-header h3 {
        color: white;
        margin: 0;
        font-size: 1.3rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
   
    /* Content boxes */
    .aksara-box {
        background: linear-gradient(135deg, #F4FFC3 0%, #DDF6D2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #CAE8BD;
        margin-bottom: 1rem;
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
   
    .aksara-text {
        font-size: 2rem;
        font-weight: bold;
        color: #5D8736;
        font-family: "Noto Sans Javanese", serif;
    }
   
    .latin-box {
        background: linear-gradient(135deg, #CAE8BD 0%, #B0DB9C 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #809D3C;
        margin-bottom: 1rem;
        min-height: 80px;
        display: flex;
        align-items: center;
    }
   
    .latin-text {
        font-size: 1.1rem;
        font-style: italic;
        color: #5D8736;
        font-weight: 500;
    }
   
    .indonesia-box {
        background: linear-gradient(135deg, #DDF6D2 0%, #F4FFC3 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #A9C46C;
        margin-bottom: 1rem;
        min-height: 80px;
        display: flex;
        align-items: center;
    }
   
    .indonesia-text {
        font-size: 1rem;
        color: #5D8736;
        line-height: 1.5;
    }
   
    /* Section headers */
    .section-header {
        color: #5D8736;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
   
    /* Summary box */
    .summary-box {
        background: linear-gradient(135deg, #809D3C 0%, #5D8736 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 6px 25px rgba(93, 135, 54, 0.3);
    }
   
    .summary-text {
        color: white;
        margin: 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
   
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #5D8736 0%, #3a5a22 100%);
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
   
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #F4FFC3 !important;
    }
   
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] li {
        color: #DDF6D2 !important;
    }
   
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #809D3C 0%, #A9C46C 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        height: 48px;
        font-size: 16px;
    }
   
    .stButton > button:hover {
        background: linear-gradient(135deg, #5D8736 0%, #809D3C 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(93, 135, 54, 0.3);
    }
   
    /* Input styling */
    .stTextInput > div > div > input {
        border: 2px solid #CAE8BD;
        border-radius: 8px;
        background: white;
        height: 48px;
        font-size: 16px;
        color: #5D8736;
    }
   
    .stTextInput > div > div > input:focus {
        border-color: #809D3C;
        box-shadow: 0 0 0 2px rgba(128, 157, 60, 0.2);
    }
   
    /* Info boxes styling */
    .stInfo {
        background: linear-gradient(135deg, #F4FFC3 0%, #DDF6D2 100%);
        border-left: 4px solid #A9C46C;
    }
   
    .stSuccess {
        background: linear-gradient(135deg, #DDF6D2 0%, #CAE8BD 100%);
        border-left: 4px solid #809D3C;
    }
   
    .stWarning {
        background: linear-gradient(135deg, #F4FFC3 0%, #DDF6D2 100%);
        border-left: 4px solid #A9C46C;
    }
   
    /* Footer styling */
    .footer {
        text-align: center;
        color: #5D8736;
        padding: 2rem;
        background: rgba(221, 246, 210, 0.5);
        border-radius: 10px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# URL GraphDB endpoint
# Pastikan ini URL ngrok yang aktif dan benar
GRAPHDB_ENDPOINT = "https://69d4-36-69-143-181.ngrok-free.app/repositories/Semweb"

def execute_sparql_query(query):
    """
    Menjalankan query SPARQL ke GraphDB endpoint
    """
    try:
        headers = {
            'Accept': 'application/sparql-results+json',
            'Content-Type': 'application/sparql-query'
        }
       
        response = requests.post(
            GRAPHDB_ENDPOINT,
            data=query,
            headers=headers,
            timeout=30
        )
       
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
           
    except requests.exceptions.RequestException as e:
        st.error(f"Koneksi error: {str(e)}")
        return None

def search_by_keyword(keyword):
    """
    Mencari berdasarkan kata kunci dan mengelompokkan contoh kalimat untuk menghindari duplikasi.
    """
    # Query utama menggunakan prefix jawa seperti di RDF
    query = f"""
    PREFIX jawa: <http://example.org/jawa#>
   
    SELECT ?aksara ?latin ?indonesia
           (GROUP_CONCAT(DISTINCT ?contohIndo; separator="||") AS ?contohIndoGroup)
           (GROUP_CONCAT(DISTINCT ?contohLatin; separator="||") AS ?contohLatinGroup)
           (GROUP_CONCAT(DISTINCT ?contohAksara; separator="||") AS ?contohAksaraGroup)
    WHERE {{
        ?s a jawa:Kata ;
           jawa:memilikiAksara ?aksara ;
           jawa:ditulisDenganLatin ?latin ;
           jawa:berartiDalamBahasaIndonesia ?indonesia .
       
        # Mengambil contoh kalimat secara opsional
        OPTIONAL {{ ?s jawa:memilikiContohKalimatIndonesia ?contohIndo . }}
        OPTIONAL {{ ?s jawa:memilikiContohKalimatLatin ?contohLatin . }}
        OPTIONAL {{ ?s jawa:memilikiContohKalimatAksara ?contohAksara . }}
       
        # Filter pencarian hanya pada kata, bukan contoh kalimat
        FILTER(
            CONTAINS(LCASE(?aksara), LCASE("{keyword}")) ||
            CONTAINS(LCASE(?latin), LCASE("{keyword}")) ||
            CONTAINS(LCASE(?indonesia), LCASE("{keyword}"))
        )
    }}
    GROUP BY ?aksara ?latin ?indonesia
    ORDER BY ?latin
    LIMIT 50
    """
   
    # Jalankan query spesifik
    result = execute_sparql_query(query)
   
    # Fallback tidak diperlukan lagi karena query utama sudah cukup solid
    if result and 'results' in result and result['results']['bindings']:
        return result
   
    st.error("❌ Tidak ada data yang ditemukan. Periksa kata kunci atau koneksi ke GraphDB.")
    return None

def display_results(results):
    """
    Menampilkan hasil pencarian dalam format yang rapi
    Fokus pada aksara Jawa, transliterasi Latin, terjemahan Indonesia, dan contoh kalimat.
    """
    if not results or 'results' not in results or not results['results']['bindings']:
        st.warning("Tidak ada hasil yang ditemukan.")
        return
   
    data = results['results']['bindings']
    st.success(f"🎉 Ditemukan {len(data)} hasil pencarian yang unik")
   
    # Tampilkan semua hasil dalam format card yang menarik
    for i, item in enumerate(data, 1):
        # Container untuk setiap hasil
        st.markdown(f"""
        <div class="result-card">
            <div class="result-header">
                <h3>📜 Hasil Pencarian {i}</h3>
            </div>
        """, unsafe_allow_html=True)
       
        # Buat kolom untuk menampilkan data utama
        col1, col2, col3 = st.columns([1, 1, 1])
       
        # Ekstraksi data dari GraphDB endpoint
        aksara_jawa = item.get('aksara', {}).get('value', '')
        transliterasi = item.get('latin', {}).get('value', '')
        terjemahan = item.get('indonesia', {}).get('value', '')
       
        # Ekstraksi dan proses contoh kalimat yang sudah digabung
        contoh_indo_group = item.get('contohIndoGroup', {}).get('value', '')
        contoh_latin_group = item.get('contohLatinGroup', {}).get('value', '')
        contoh_aksara_group = item.get('contohAksaraGroup', {}).get('value', '')
       
        with col1:
            st.markdown('<div class="section-header">🔤 Aksara Jawa</div>', unsafe_allow_html=True)
            if aksara_jawa:
                st.markdown(f'<div class="aksara-box"><div class="aksara-text">{aksara_jawa}</div></div>', unsafe_allow_html=True)
            else:
                st.info("Aksara Jawa tidak tersedia")
       
        with col2:
            st.markdown('<div class="section-header">🔤 Transliterasi Latin</div>', unsafe_allow_html=True)
            if transliterasi:
                st.markdown(f'<div class="latin-box"><div class="latin-text">"{transliterasi}"</div></div>', unsafe_allow_html=True)
            else:
                st.info("Transliterasi tidak tersedia")
       
        with col3:
            st.markdown('<div class="section-header">🇮🇩 Terjemahan Indonesia</div>', unsafe_allow_html=True)
            if terjemahan:
                st.markdown(f'<div class="indonesia-box"><div class="indonesia-text">{terjemahan}</div></div>', unsafe_allow_html=True)
            else:
                st.info("Terjemahan tidak tersedia")
       
        # Bagian baru untuk menampilkan contoh kalimat dengan urutan Indonesia, Latin, Aksara
        if contoh_indo_group or contoh_latin_group or contoh_aksara_group:
            st.markdown("<hr style='border-top: 1px solid var(--background-medium); margin: 1.5rem 0;'>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">📝 Contoh Kalimat</div>', unsafe_allow_html=True)
           
            # Styling untuk kotak contoh kalimat
            contoh_style = "background-color: #f8f9fa; padding: 10px; border-radius: 8px; border-left: 4px solid var(--primary-light); margin-bottom: 8px;"
           
            # Membuat list dari setiap jenis kalimat
            indo_sentences = contoh_indo_group.split('||') if contoh_indo_group else []
            latin_sentences = contoh_latin_group.split('||') if contoh_latin_group else []
            aksara_sentences = contoh_aksara_group.split('||') if contoh_aksara_group else []
            
            # Menentukan jumlah kalimat maksimal
            max_sentences = max(len(indo_sentences), len(latin_sentences), len(aksara_sentences))
            
            # Menampilkan setiap set kalimat secara berurutan: Indonesia, Latin, Aksara
            for i in range(max_sentences):
                # Tampilkan kalimat Indonesia jika ada
                if i < len(indo_sentences) and indo_sentences[i].strip():
                    st.markdown(f"""
                    <div style='{contoh_style}'>
                        <p style='color: #4a623a; margin: 0;'><strong>🇮🇩 Indonesia:</strong> <em>{indo_sentences[i].strip()}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Tampilkan kalimat Latin jika ada
                if i < len(latin_sentences) and latin_sentences[i].strip():
                    st.markdown(f"""
                    <div style='{contoh_style}'>
                        <p style='color: #4a623a; margin: 0;'><strong>🔤 Latin:</strong> <em>{latin_sentences[i].strip()}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Tampilkan kalimat Aksara Jawa jika ada
                if i < len(aksara_sentences) and aksara_sentences[i].strip():
                    st.markdown(f"""
                    <div style='{contoh_style}'>
                        <p style='color: #4a623a; margin: 0;'><strong>📜 Aksara Jawa:</strong> <span class='aksara-text' style='font-size: 1.5rem;'>{aksara_sentences[i].strip()}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Tambahkan pemisah antar set kalimat jika ada lebih dari satu set
                if i < max_sentences - 1:
                    st.markdown("<div style='margin: 15px 0; border-bottom: 1px dashed #ccc;'></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Summary di bagian bawah
    st.markdown(f"""
    <div class="summary-box">
        <h4 class="summary-text">✨ Total {len(data)} hasil ditemukan untuk pencarian Anda</h4>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header aplikasi
    st.markdown("""
    <div style='position: relative; text-align: center; height: 250px; border-radius: 10px; overflow: hidden; margin-bottom: 30px;'>
        <img src='https://startfmmadina.com/wp-content/uploads/2022/09/Serigala-dan-Anak-Kambing-yang-Berhati-hati-620x330.jpg'
             style='width: 100%; height: 100%; object-fit: cover; filter: brightness(60%);' />
        <div style='position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                    display: flex; flex-direction: column; justify-content: center; align-items: center;
                    color: white; text-shadow: 1px 1px 3px rgba(0,0,0,0.8); padding: 20px;'>
            <h1 style='margin: 0;'>📜 Pencarian Naskah Jawa</h1>
            <p style='margin: 10px 0 0 0; font-size: 18px;'>Wedhus lan Asu Ajag (Kambing dan Serigala)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
   
    # Sidebar untuk pengaturan pencarian
    with st.sidebar:
        st.header("🔍 Pengaturan Pencarian")
       
        if st.button("Test Koneksi GraphDB"):
            with st.spinner("Mengetes koneksi..."):
                test_query = "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o . }"
                result = execute_sparql_query(test_query)
                if result:
                    st.success("✅ Koneksi berhasil!")
                else:
                    st.error("❌ Koneksi gagal!")
       
        st.markdown("---")
       
        st.markdown("### ℹ Informasi")
        st.markdown("""
        - Gunakan kata kunci untuk mencari dalam teks Aksara Jawa, Latin, atau terjemahan Indonesia.
        - Pencarian tidak case-sensitive.
        - Data diambil langsung dari GraphDB melalui ngrok.
        - Contoh kalimat ditampilkan berurutan: Indonesia → Latin → Aksara Jawa
        """)

        st.markdown("---")
        st.markdown("### 📖 Cerita Lengkap")
        with st.expander("Baca Cerita: Wedhus lan Asu Ajag", expanded=False):
            st.markdown("""
            *Wedhus Lan Asu Ajag*
           
            ꦮꦼꦣꦸꦱ꧀ꦭꦤ꧀ꦲꦱꦸꦲꦗꦒ꧀

            Ing sawijining dina, ana wedhus lan anaké. Dicritakaké yèn wedhus arep menyang alas golèk pangan. Niaté ora ngajak anaké, wedhus ngajari anaké supaya ora mbukak lawang marang sapa waé. Supaya anaké tetep aman ing omah, wedhus mulangaké tembang marang anaké minangka tandha yèn iku ibuné.

            *Kambing dan Serigala*

            Pada suatu hari, terdapat ibu kambing beserta anaknya. Dikisahkan bahwa sang ibu kambing ingin pergi ke hutan untuk mencari makanan. Berniat untuk tidak mengajak anaknya, ibu kambing mengajarkan kepada sang anak untuk tidak membukakan pintu kepada siapa pun. Agar anak kambing tetap aman di dalam rumah, ibu kambing mengajarkan sebuah lagu kepada anaknya sebagai petanda bahwa itu adalah ibunya.
            """)
   
    # Area pencarian utama
    col1, col2 = st.columns([4, 1])
   
    with col1:
        keyword = st.text_input(
            "🔍 Masukkan kata kunci pencarian:",
            placeholder="Contoh: wedhus, kambing, ꦮꦼꦣꦸꦱ꧀, serigala, dll...",
            help="Ketik kata yang ingin dicari dalam Aksara Jawa, Latin, atau terjemahan Indonesia",
            label_visibility="collapsed"
        )
   
    with col2:
        search_button = st.button("Cari", type="primary", use_container_width=True)
   
    # Proses pencarian
    if search_button or keyword:
        if keyword:
            with st.spinner("Mencari data dari GraphDB..."):
                results = search_by_keyword(keyword)
                display_results(results)
        else:
            st.warning("Silakan masukkan kata kunci pencarian.")
   
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>Aplikasi Pencarian Naskah Jawa - Semantic Web Technology</strong></p>
        <p>Menggunakan GraphDB dan SPARQL Query melalui ngrok endpoint</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()