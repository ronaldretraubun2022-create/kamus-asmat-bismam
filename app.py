import streamlit as st
from supabase import create_client, Client

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kamus Digital Asmat Rumpun Bismam", 
    page_icon="🏹", 
    layout="centered"
)

# --- 2. KONEKSI DATABASE (SUPABASE) ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    st.error("Konfigurasi Secrets (SUPABASE_URL/KEY) belum lengkap di Streamlit Cloud.")
    st.stop()

# --- 3. CUSTOM CSS (TEMA ETNIK PAPUA SELATAN) ---
st.markdown("""
    <style>
    /* Hilangkan elemen bawaan Streamlit */
    header, footer, .stDeployButton, #MainMenu { display: none !important; }
    
    /* Latar Belakang Krem */
    .stApp { background-color: #FFFDF9 !important; }
    
    /* Warna Teks Utama */
    p, span, label, h1, h2, h3 { color: #5D4037 !important; }
    
    /* Styling Sidebar */
    [data-testid="stSidebar"] { background-color: #2E1A08 !important; }
    [data-testid="stSidebar"] * { color: #EADDCA !important; }

    /* Tombol-tombol Warna Kayu */
    .stButton>button {
        background-color: #8B4513 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 100%;
    }
    
    /* Styling Box Input */
    .stTextInput input {
        border: 2px solid #8B4513 !important;
        border-radius: 10px !important;
    }

    /* Footer Style */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #2E1A08;
        color: #EADDCA;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }

    /* Styling khusus Google Translate */
    .goog-te-gadget {
        font-family: sans-serif !important;
        color: #EADDCA !important;
    }
    .goog-te-gadget-simple {
        background-color: #3E2723 !important;
        border: 1px solid #8B4513 !important;
        padding: 5px !important;
        border-radius: 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA KATEGORI & KOSA KATA ---
DAFTAR_KATA = {
    "🦴 Anatomi Tubuh": ["Kepala", "Rambut", "Mata", "Telinga", "Hidung", "Mulut", "Tangan", "Kaki", "Jantung", "Darah"],
    "👨‍👩‍👧‍👦 Keluarga": ["Bapak/Ayah", "Ibu/Mama", "Kakak Laki-laki", "Kakak Perempuan", "Adik", "Kakek", "Nenek", "Paman", "Bibi"],
    "🍳 Dapur & Rumah": ["Parang", "Kapak", "Periuk", "Piring", "Sendok", "Kayu Bakar", "Api", "Air", "Tungku"],
    "🍲 Makanan & Alam": ["Sagu", "Ikan", "Ulat Sagu", "Babi Hutan", "Burung", "Hutan", "Sungai", "Dusun", "Perahu", "Dayung"],
    "🐾 Hewan Papua": ["Cendrawasih", "Kasuari", "Kakatua", "Mambruk", "Walabi", "Kuskus", "Buaya", "Ular", "Rusa"]
}

# --- 5. SIDEBAR: GOOGLE TRANSLATE ---
with st.sidebar:
    st.markdown("### 🌐 Terjemahan / Translation")
    st.components.v1.html("""
    <div id="google_translate_element"></div>
    <script type="text/javascript">
    function googleTranslateElementInit() {
      new google.translate.TranslateElement({
        pageLanguage: 'id', 
        includedLanguages: 'en,id', 
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE
      }, 'google_translate_element');
    }
    </script>
    <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
    """, height=100)
    st.divider()
    st.info("Aplikasi ini berfokus pada pelestarian Bahasa Asmat Rumpun Bismam.")

# --- 6. HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try: 
        st.image("MUSEUM ASMAT.png", width=150)
    except: 
        st.markdown("<h1 style='text-align: center; color: #8B4513;'>🏹</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #8B4513; margin-top: -20px; font-weight: bold;'>KAMUS DIGITAL BAHASA ASMAT<br>RUMPUN BISMAM</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #6F4E37;'>Melestarikan Budaya Lewat Bahasa - Papua Selatan</p>", unsafe_allow_html=True)
st.divider()

# --- 7. NAVIGASI TABS ---
tab_cari, tab_kontribusi, tab_admin = st.tabs(["🔍 CARI KATA", "📝 KONTRIBUSI", "🛡️ PANEL ADMIN"])

# --- TAB 1: CARI KATA ---
with tab_cari:
    st.subheader("🔍 Cari Kosakata")
    search = st.text_input("Ketik kata dalam Bahasa Indonesia atau Asmat...", placeholder="Cari kata...")
    if search:
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Verified").or_(f"kata_asmat.ilike.%{search}%,arti_indonesia.ilike.%{search}%").execute()
        if res.data:
            for item in res.data:
                st.markdown(f"""
                <div style="background-color: #F5F5DC; border-left: 10px solid #8B4513; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <h3 style="margin:0; color: #8B4513;">{item['kata_asmat']}</h3>
                    <p style="margin:0; color: #5D4037;">Artinya: <b>{item['arti_indonesia']}</b></p>
                    <p style="margin:0; font-size: 12px; color: #8B4513;"><i>Kategori: {item.get('kategori', 'Umum')}</i></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Kata belum ditemukan atau belum diverifikasi.")
    
    total_res = supabase.table("kamus_bismam").select("id", count="exact").eq("status_verifikasi", "Verified").execute()
    if total_res.count:
        st.markdown(f"<p style='text-align: center; font-size: 12px; opacity: 0.7;'>Total: {total_res.count} kosakata terverifikasi</p>", unsafe_allow_html=True)

# --- TAB 2: KONTRIBUSI (BAGIAN YANG DIPERBARUI) ---
with tab_kontribusi:
    st.subheader("📝 Sumbangkan Kata Baru")
    st.write("Pilih kata Bahasa Indonesia di bawah ini, lalu isi terjemahan Bahasa Asmat-nya.")
    
    with st.form("form_kontribusi", clear_on_submit=True):
        # 1. Pilih Kategori
        kat_pilihan = st.selectbox("Pilih Kategori Kosakata:", list(DAFTAR_KATA.keys()) + ["✨ Lainnya"])
        
        # 2. Pilih Kata Indonesia berdasarkan kategori yang dipilih
        if kat_pilihan in DAFTAR_KATA:
            kata_indo_pilihan = st.selectbox("Pilih Kata Bahasa Indonesia:", DAFTAR_KATA[kat_pilihan])
        else:
            kata_indo_pilihan = st.text_input("Ketik Kata Bahasa Indonesia (Jika tidak ada di daftar):")
        
        # 3. Kontributor TINGGAL MENGISI BAHASA ASMAT
        kata_asmat = st.text_input("Tuliskan Bahasa Asmat Rumpun Bismam-nya:", placeholder="Contoh: Terjemahan kata tersebut...")
        
        nama_p = st.text_input("Nama Penyumbang (Opsional)")
        
        if st.form_submit_button("KIRIM TERJEMAHAN"):
            if kata_indo_pilihan and kata_asmat:
                supabase.table("kamus_bismam").insert({
                    "kata_asmat": kata_asmat, 
                    "arti_indonesia": kata_indo_pilihan, 
                    "kategori": kat_pilihan, 
                    "nama_penyumbang": nama_p if nama_p else "Anonim",
                    "status_verifikasi": "Pending"
                }).execute()
                st.success(f"Terima kasih! Terjemahan untuk '{kata_indo_pilihan}' telah dikirim ke Admin.")
            else:
                st.error("Mohon isi terjemahan Bahasa Asmat terlebih dahulu.")

# --- TAB 3: ADMIN ---
with tab_admin:
    st.subheader("🛡️ Verifikasi Admin")
    admin_pass = st.text_input("Kode Akses", type="password")
    if admin_pass == st.secrets.get("ADMIN_PASSWORD", "Bismam2026"):
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
        if res.data:
            st.write(f"Menunggu Verifikasi: **{len(res.data)} item**")
            for item in res.data:
                with st.expander(f"📌 {item['kata_asmat']} - {item['arti_indonesia']}"):
                    st.write(f"Penyumbang: {item.get('nama_penyumbang', 'Anonim')}")
                    c1, c2 = st.columns(2)
                    if c1.button("SETUJUI ✅", key=f"s_{item['id']}"):
                        supabase.table("kamus_bismam").update({"status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                        st.rerun()
                    if c2.button("HAPUS ❌", key=f"h_{item['id']}"):
                        supabase.table("kamus_bismam").delete().eq("id", item['id']).execute()
                        st.rerun()
        else:
            st.info("Tidak ada kontribusi baru.")

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        © 2026 Kamus Digital Asmat Rumpun Bismam - Kabupaten Asmat, Papua Selatan
    </div>
    """, unsafe_allow_html=True)
