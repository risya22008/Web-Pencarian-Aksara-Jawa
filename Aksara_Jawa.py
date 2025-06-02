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

# Custom CSS dengan color palette yang diminta
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
    
    /* Header styling */
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
    .css-1d391kg {
        background: linear-gradient(135deg, #5D8736 0%, #809D3C 100%);
    }
    
    /* Sidebar content styling */
    .css-1d391kg .css-1544g2n {
        color: white;
    }
    
    .css-1d391kg h2, .css-1d391kg h3 {
        color: #F4FFC3 !important;
    }
    
    .css-1d391kg .stMarkdown p, .css-1d391kg .stMarkdown li {
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
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #809D3C;
        box-shadow: 0 0 0 2px rgba(128, 157, 60, 0.2);
    }
    
    /* Button height adjustment to match input */
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
    
    /* Info boxes */
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
GRAPHDB_ENDPOINT = "https://4e73-2404-c0-2b10-00-2aff-bb8c.ngrok-free.app/repositories/Semweb"

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
    Mencari berdasarkan kata kunci dalam transliterasi atau terjemahan
    dari data yang ada di GraphDB endpoint
    """
    # Query utama menggunakan prefix jawa seperti di RDF
    query = f"""
    PREFIX jawa: <http://example.org/jawa#>
    
    SELECT ?aksara ?latin ?indonesia
    WHERE {{
        ?s a jawa:Kata ;
           jawa:aksara ?aksara ;
           jawa:latin ?latin ;
           jawa:indonesia ?indonesia .
        
        FILTER(
            CONTAINS(LCASE(?latin), LCASE("{keyword}")) || 
            CONTAINS(LCASE(?indonesia), LCASE("{keyword}"))
        )
    }}
    ORDER BY ?latin
    LIMIT 50
    """
    
    # Jalankan query spesifik
    result = execute_sparql_query(query)
    
    if result and 'results' in result and result['results']['bindings']:
        return result
    else:
        # Fallback query jika struktur spesifik tidak ada
        general_query = f"""
        SELECT DISTINCT ?subject ?predicate ?object
        WHERE {{
            ?subject ?predicate ?object .
            FILTER(
                isLiteral(?object) && 
                CONTAINS(LCASE(STR(?object)), LCASE("{keyword}"))
            )
        }}
        LIMIT 20
        """
        result_general = execute_sparql_query(general_query)
        if result_general and 'results' in result_general and result_general['results']['bindings']:
            return result_general
    
    st.error("❌ Tidak ada data yang ditemukan. Periksa kata kunci atau koneksi ke GraphDB.")
    return None

def display_results(results):
    """
    Menampilkan hasil pencarian dalam format yang rapi
    Fokus pada aksara Jawa, transliterasi Latin, dan terjemahan Indonesia
    """
    if not results or 'results' not in results or not results['results']['bindings']:
        st.warning("Tidak ada hasil yang ditemukan.")
        return
    
    data = results['results']['bindings']
    st.success(f"🎉 Ditemukan {len(data)} hasil pencarian")
    
    # Tampilkan semua hasil dalam format card yang menarik
    for i, item in enumerate(data, 1):
        # Container untuk setiap hasil
        st.markdown(f"""
        <div class="result-card">
            <div class="result-header">
                <h3>📜 Hasil Pencarian {i}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Buat 3 kolom untuk menampilkan data
        col1, col2, col3 = st.columns([1, 1, 1])
        
        # Ekstraksi data dari GraphDB endpoint
        aksara_jawa = item.get('aksara', {}).get('value', '')
        transliterasi = item.get('latin', {}).get('value', '')
        terjemahan = item.get('indonesia', {}).get('value', '')

        # Fallback untuk query umum jika struktur spesifik tidak ada
        if not aksara_jawa and 'predicate' in item and 'object' in item:
            pred_lower = item['predicate']['value'].lower()
            obj_value = item['object']['value']
            
            if 'aksara' in pred_lower or 'jawa' in pred_lower:
                aksara_jawa = obj_value
            elif 'latin' in pred_lower or 'transliter' in pred_lower:
                transliterasi = obj_value
            elif 'indonesia' in pred_lower or 'terjemah' in pred_lower:
                terjemahan = obj_value
        
        with col1:
            # Aksara Jawa
            st.markdown('<div class="section-header">🔤 Aksara Jawa</div>', unsafe_allow_html=True)
            if aksara_jawa:
                st.markdown(f"""
                <div class="aksara-box">
                    <div class="aksara-text">{aksara_jawa}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Aksara Jawa tidak tersedia")
        
        with col2:
            # Transliterasi Latin
            st.markdown('<div class="section-header">🔤 Transliterasi Latin</div>', unsafe_allow_html=True)
            if transliterasi:
                st.markdown(f"""
                <div class="latin-box">
                    <div class="latin-text">"{transliterasi}"</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Transliterasi tidak tersedia")
        
        with col3:
            # Terjemahan Indonesia
            st.markdown('<div class="section-header">🇮🇩 Terjemahan Indonesia</div>', unsafe_allow_html=True)
            if terjemahan:
                st.markdown(f"""
                <div class="indonesia-box">
                    <div class="indonesia-text">{terjemahan}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Terjemahan tidak tersedia")
        
        # Tampilkan raw data jika tidak ada data terstruktur
        if not (aksara_jawa or transliterasi or terjemahan) and (item.get('subject') or item.get('predicate') or item.get('object')):
            st.markdown("### 🔍 Data Mentah")
            with st.expander("Lihat data mentah", expanded=False):
                st.json(item)
        
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
    <div class="main-header">
        <h1>📜 Pencarian Naskah Jawa</h1>
        <p>Wedhus lan Asu Ajag (Kambing dan Serigala)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar untuk pengaturan pencarian
    with st.sidebar:
        st.header("🔍 Pengaturan Pencarian")
        
        # Test koneksi
        if st.button("Test Koneksi GraphDB", type="secondary"):
            with st.spinner("Mengetes koneksi..."):
                test_query = """
                SELECT (COUNT(*) as ?count) WHERE {
                    ?s ?p ?o .
                }
                """
                result = execute_sparql_query(test_query)
                if result:
                    st.success("✅ Koneksi berhasil!")
                else:
                    st.error("❌ Koneksi gagal!")
        
        st.markdown("---")
        
        # Informasi tambahan
        st.markdown("### ℹ️ Informasi")
        st.markdown("""
        - Gunakan kata kunci untuk mencari dalam teks
        - Pencarian tidak case-sensitive
        - Data diambil langsung dari GraphDB melalui ngrok
        """)
    
    # Area pencarian utama
    col1, col2 = st.columns([4, 1])
    
    with col1:
        keyword = st.text_input(
            "🔍 Masukkan kata kunci pencarian:",
            placeholder="Contoh: wedhus, kambing, serigala, dll...",
            help="Ketik kata yang ingin dicari dalam transliterasi atau terjemahan",
            label_visibility="collapsed"
        )
    
    with col2:
        # Add some spacing to align with text input
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
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