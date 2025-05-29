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

# URL GraphDB endpoint
GRAPHDB_ENDPOINT = "https://1093-114-10-145-170.ngrok-free.app/repositories/Semweb"

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
        with st.container():
            # Header untuk setiap hasil
            st.markdown(f"""
            <div style='background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 10px; border-radius: 10px; margin: 10px 0;'>
                <h3 style='color: white; margin: 0; text-align: center;'>
                    📜 Hasil Pencarian {i}
                </h3>
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
                st.markdown("### 🔤 Aksara Jawa")
                if aksara_jawa:
                    st.markdown(f"""
                    <div style='font-size: 24px; font-weight: bold; color: #2E4057; 
                                 background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                                 padding: 20px; border-radius: 15px; text-align: center; 
                                 border: 2px solid #ddd; margin-bottom: 15px;
                                 font-family: "Noto Sans Javanese", serif;'>
                        {aksara_jawa}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Aksara Jawa tidak tersedia")
            
            with col2:
                # Transliterasi Latin
                st.markdown("### 🔤 Transliterasi Latin")
                if transliterasi:
                    st.markdown(f"""
                    <div style='font-size: 18px; font-style: italic; color: #1565C0; 
                                 background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                                 padding: 15px; border-radius: 10px; 
                                 border-left: 4px solid #2196F3; margin-bottom: 15px;'>
                        "{transliterasi}"
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Transliterasi tidak tersedia")
            
            with col3:
                # Terjemahan Indonesia
                st.markdown("### 🇮🇩 Terjemahan Indonesia")
                if terjemahan:
                    st.markdown(f"""
                    <div style='font-size: 16px; color: #2E7D32; 
                                 background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                                 padding: 15px; border-radius: 10px; 
                                 border-left: 4px solid #4CAF50; margin-bottom: 15px;'>
                        {terjemahan}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Terjemahan tidak tersedia")
            
            # Tampilkan raw data jika tidak ada data terstruktur
            if not (aksara_jawa or transliterasi or terjemahan) and (item.get('subject') or item.get('predicate') or item.get('object')):
                st.markdown("### 🔍 Data Mentah")
                with st.expander("Lihat data mentah", expanded=False):
                    st.json(item)
            
            st.markdown("---")
    
    # Summary di bagian bawah
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px;'>
        <h4 style='color: white; margin: 0;'>
            ✨ Total {len(data)} hasil ditemukan untuk pencarian Anda
        </h4>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header aplikasi
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>📜 Pencarian Naskah Jawa</h1>
        <p style='color: white; margin: 10px 0 0 0; font-size: 18px;'>Wedhus lan Asu Ajag (Kambing dan Serigala)</p>
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
    col1, col2 = st.columns([3, 1])
    
    with col1:
        keyword = st.text_input(
            "🔍 Masukkan kata kunci pencarian:",
            placeholder="Contoh: wedhus, kambing, serigala, dll...",
            help="Ketik kata yang ingin dicari dalam transliterasi atau terjemahan"
        )
    
    with col2:
        st.write("")  # spacing
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
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Aplikasi Pencarian Naskah Jawa - Semantic Web Technology</p>
        <p>Menggunakan GraphDB dan SPARQL Query melalui ngrok endpoint</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()