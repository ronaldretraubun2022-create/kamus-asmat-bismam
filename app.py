import streamlit as st
from supabase import create_client, Client

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kamus Digital Asmat Rumpun Bismam", 
    page_icon="🏹", 
    layout="centered"
)

# --- 2. KONEKSI DATABASE (SUPABASE) ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_connection()
except Exception as e:
    st.error(f"Gagal koneksi ke database: {e}")
    st.stop()

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu { display: none !important; }
    .stApp { background-color: #FFFDF9 !important; }
    p, span, label, h1, h2, h3 { color: #5D4037 !important; }
    [data-testid="stSidebar"] { background-color: #2E1A08 !important; }
    [data-testid="stSidebar"] * { color: #EADDCA !important; }
    .stButton>button {
        background-color: #8B4513 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 100%;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        border: 2px solid #8B4513 !important;
        border-radius: 10px !important;
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #2E1A08; color: #EADDCA;
        text-align: center; padding: 10px; font-size: 12px; z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA KOSA KATA ---
DAFTAR_KATA = {
    "🦴 Anatomi: Bagian Luar": ["Kepala", "Rambut", "Dahi", "Mata", "Hidung"],
    "🫀 Anatomi: Dalam & Sistem": ["Otak", "Jantung", "Paru-paru", "Hati"],
    "🍳 Alat Masak": ["Kompor", "Wajan", "Panci", "Dandang"],
    "🍽️ Alat Makan & Wadah": ["Piring", "Mangkok", "Sendok", "Gelas"],
    "🧂 Bumbu & Protein Sagu": ["Garam", "Gula", "Minyak goreng", "Sagu", "Papeda"],
    "🏹 Budaya & Ritual Asmat": ["Upacara adat", "Ritual leluhur", "Pesta adat", "Ukiran kayu", "Tifa", "Noken"],
    "🐾 Hewan (Darat & Papua)": ["Anjing", "Babi", "Kasuari", "Rusa", "Burung nuri", "Burung cenderawasih"],
    "✨ Kategori Lainnya": []
}

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🌐 Translation")
    st.components.v1.html("""
    <div id="google_translate_element"></div>
    <script type="text/javascript">
    function googleTranslateElementInit() {
      new google.translate.TranslateElement({pageLanguage: 'id', includedLanguages: 'en,id', layout: google.translate.TranslateElement.InlineLayout.SIMPLE}, 'google_translate_element');
    }
    </script>
    <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
    """, height=80)
    st.divider()
    st.info("Fokus: Pelestarian Bahasa Asmat Rumpun Bismam.")

# --- 6. HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try: 
        st.image("MUSEUM ASMAT.png", width=150)
    except: 
        st.markdown("<h1 style='text-align: center;'>🏹</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #8B4513; margin-top: -20px; font-weight: bold;'>KAMUS DIGITAL BAHASA ASMAT<br>RUMPUN BISMAM</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #6F4E37;'>Melestarikan Budaya Lewat Bahasa - Papua Selatan</p>", unsafe_allow_html=True)
st.divider()

# --- 7. TABS ---
tab_cari, tab_kontribusi, tab_admin = st.tabs(["🔍 CARI KATA", "📝 KONTRIBUSI", "🛡️ PANEL ADMIN"])

# --- TAB 1: CARI KATA ---
with tab_cari:
    search = st.text_input("Ketik kata dalam Bahasa Indonesia atau Asmat...", placeholder="Contoh: Tifa atau Kepala")
    if search:
        res = supabase.table("kamus_bismam").select("*")\
            .eq("status_verifikasi", "Verified")\
            .or_(f"kata_asmat.ilike.%{search}%,arti_indonesia.ilike.%{search}%")\
            .execute()
        
        if res.data:
            for item in res.data:
                st.markdown(f"""
                <div style="background-color: #F5F5DC; border-left: 10px solid #8B4513; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <h3 style="margin:0; color: #8B4513;">{item['kata_asmat']}</h3>
                    <p style="margin:0; color: #5D4037;">Indonesia: <b>{item['arti_indonesia']}</b></p>
                    <small style="color: #8B4513;">Kategori: {item['kategori']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Kata belum ditemukan dalam database terverifikasi.")

# --- TAB 2: KONTRIBUSI ---
with tab_kontribusi:
    st.subheader("📝 Tambah Kosa Kata")
    kat_pilihan = st.selectbox("Pilih Kategori:", list(DAFTAR_KATA.keys()))
    
    with st.form("form_kontribusi", clear_on_submit=True):
        if kat_pilihan == "✨ Kategori Lainnya":
            kata_indo_input = st.text_input("Ketik Kata Indonesia Baru:")
        else:
            kata_indo_input = st.selectbox("Pilih Kata Bahasa Indonesia:", DAFTAR_KATA[kat_pilihan])
        
        kata_asmat_input = st.text_input("Tuliskan Bahasa Asmat-nya:")
        nama_p = st.text_input("Nama Anda (Opsional):")
        
        submit = st.form_submit_button("KIRIM KE DATABASE")
        
        if submit:
            if kata_indo_input and kata_asmat_input:
                try:
                    supabase.table("kamus_bismam").insert({
                        "kata_asmat": kata_asmat_input, 
                        "arti_indonesia": kata_indo_input, 
                        "kategori": kat_pilihan, 
                        "kontributor_name": nama_p if nama_p else "Anonim",
                        "status_verifikasi": "Pending"
                    }).execute()
                    st.success("✅ Terkirim! Data akan muncul setelah diverifikasi admin.")
                except Exception as e:
                    st.error(f"Gagal mengirim. Error: {e}")
            else:
                st.error("Silakan isi semua kolom wajib.")

# --- TAB 3: ADMIN ---
with tab_admin:
    admin_pass = st.text_input("Kode Akses Admin", type="password")
    if admin_pass == st.secrets.get("ADMIN_PASSWORD", "Bismam2026"):
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
        
        if res.data:
            st.write(f"Terdapat {len(res.data)} data baru:")
            for item in res.data:
                with st.expander(f"📌 {item['kata_asmat']} - {item['arti_indonesia']}"):
                    st.write(f"Kontributor: {item['kontributor_name']}")
                    c1, c2 = st.columns(2)
                    if c1.button("Terima ✅", key=f"v_{item['id']}"):
                        supabase.table("kamus_bismam").update({"status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                        st.rerun()
                    if c2.button("Hapus ❌", key=f"d_{item['id']}"):
                        supabase.table("kamus_bismam").delete().eq("id", item['id']).execute()
                        st.rerun()
        else:
            st.success("Semua data sudah bersih.")

# --- FOOTER ---
st.markdown('<div class="footer">© 2026 Kamus Digital Asmat Rumpun Bismam - Papua Selatan</div>', unsafe_allow_html=True)
