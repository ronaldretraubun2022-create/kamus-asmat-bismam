import streamlit as st
from supabase import create_client, Client

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kamus Asmat Rumpun Bismam", 
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
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA KATEGORI ---
DAFTAR_KATA = {
    "🦴 Anatomi Tubuh": ["Kepala", "Rambut", "Mata", "Telinga", "Hidung", "Mulut", "Tangan", "Kaki", "Jantung", "Darah"],
    "👨‍👩‍👧‍👦 Keluarga": ["Bapak/Ayah", "Ibu/Mama", "Kakak Laki-laki", "Kakak Perempuan", "Adik", "Kakek", "Nenek", "Paman", "Bibi"],
    "🍳 Dapur & Rumah": ["Parang", "Kapak", "Periuk", "Piring", "Sendok", "Kayu Bakar", "Api", "Air", "Tungku"],
    "🍲 Makanan & Alam": ["Sagu", "Ikan", "Ulat Sagu", "Babi Hutan", "Burung", "Hutan", "Sungai", "Dusun", "Perahu", "Dayung"],
    "🐾 Hewan Papua": ["Cendrawasih", "Kasuari", "Kakatua", "Mambruk", "Walabi", "Kuskus", "Buaya", "Ular", "Rusa"]
}

# --- 5. HEADER (LOGO MUSEUM KEMBALI) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try: 
        # Memanggil kembali file logo Anda
        st.image("MUSEUM ASMAT.png", width=150)
    except: 
        # Jika file tidak ditemukan, tampilkan simbol pengganti agar tidak error
        st.markdown("<h1 style='text-align: center; color: #8B4513;'>🏹</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #8B4513; margin-top: -20px;'>KAMUS ASMAT BISMAM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #6F4E37;'>Melestarikan Budaya Lewat Bahasa - Papua Selatan</p>", unsafe_allow_html=True)
st.divider()

# --- 6. NAVIGASI TABS ---
tab_cari, tab_kontribusi, tab_admin = st.tabs(["🔍 CARI KATA", "📝 KONTRIBUSI", "🛡️ PANEL ADMIN"])

# --- TAB 1: CARI KATA ---
with tab_cari:
    st.subheader("🔍 Cari Kosakata")
    search = st.text_input("Ketik kata dalam Bahasa Indonesia atau Asmat...")
    if search:
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Verified").or_(f"kata_asmat.ilike.%{search}%,arti_indonesia.ilike.%{search}%").execute()
        if res.data:
            for item in res.data:
                st.markdown(f"""
                <div style="background-color: #F5F5DC; border-left: 10px solid #8B4513; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <h3 style="margin:0; color: #8B4513;">{item['kata_asmat']}</h3>
                    <p style="margin:0; color: #5D4037;">Artinya: <b>{item['arti_indonesia']}</b></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Kata belum ditemukan atau belum diverifikasi.")

# --- TAB 2: KONTRIBUSI ---
with tab_kontribusi:
    st.subheader("📝 Sumbangkan Kata Baru")
    metode = st.radio("Pilih Metode:", ["⌨️ Teks", "🎙️ Audio"])
    
    if metode == "⌨️ Teks":
        with st.form("form_kontribusi"):
            kat = st.selectbox("Kategori:", list(DAFTAR_KATA.keys()) + ["✨ Lainnya"])
            kata_indo = st.text_input("Kata Indonesia")
            kata_asmat = st.text_input("Bahasa Asmat")
            if st.form_submit_button("KIRIM TERJEMAHAN"):
                if kata_indo and kata_asmat:
                    supabase.table("kamus_bismam").insert({"kata_asmat": kata_asmat, "arti_indonesia": kata_indo, "kategori": kat, "status_verifikasi": "Pending"}).execute()
                    st.success("Terima kasih! Kontribusi Anda akan diperiksa.")
    else:
        audio = st.audio_input("Rekam Suara")
        if audio: st.success("Rekaman diterima!")

# --- TAB 3: ADMIN ---
with tab_admin:
    st.subheader("🛡️ Verifikasi Admin")
    admin_pass = st.text_input("Kode Akses", type="password")
    if admin_pass == st.secrets.get("ADMIN_PASSWORD", "Bismam2026"):
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
        if res.data:
            for item in res.data:
                with st.expander(f"📌 {item['kata_asmat']}"):
                    if st.button("SETUJUI ✅", key=f"s_{item['id']}"):
                        supabase.table("kamus_bismam").update({"status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                        st.rerun()
                    if st.button("HAPUS ❌", key=f"h_{item['id']}"):
                        supabase.table("kamus_bismam").delete().eq("id", item['id']).execute()
                        st.rerun()
        else:
            st.info("Tidak ada data pending.")
