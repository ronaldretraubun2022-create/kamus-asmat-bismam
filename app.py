import streamlit as st
from supabase import create_client, Client

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Bahasa Asmat Rumpun Bismam", 
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
    
    /* Latar Belakang Krem (Warna Kulit Kayu) */
    .stApp { background-color: #FFFDF9 !important; }
    
    /* Warna Teks Utama (Cokelat Tua) */
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
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #5D2E0A !important;
        border: none !important;
    }
    
    /* Styling Box Input */
    .stTextInput input {
        border: 2px solid #8B4513 !important;
        border-radius: 10px !important;
    }
    
    /* Garis Pembatas */
    hr { border: 1px solid #D2B48C !important; }
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

# --- 5. HEADER UTAMA ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Ganti "logo.png" dengan file logo Anda jika ada
    st.markdown("<h1 style='text-align: center; color: #8B4513; margin-bottom: 0;'>🏹</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #8B4513; margin-top: -10px;'>KAMUS ASMAT BISMAM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #6F4E37;'>Melestarikan Budaya Lewat Bahasa - Papua Selatan</p>", unsafe_allow_html=True)
st.divider()

# --- 6. NAVIGASI TABS ---
# Memindahkan navigasi dari Sidebar ke Tabs tengah agar lebih fokus
tab_cari, tab_kontribusi, tab_admin = st.tabs(["🔍 CARI KATA", "📝 KONTRIBUSI", "🛡️ PANEL ADMIN"])

# --- TAB 1: CARI KATA ---
with tab_cari:
    st.subheader("🔍 Cari Kosakata")
    search = st.text_input("Ketik kata dalam Bahasa Indonesia atau Asmat...", placeholder="Contoh: Sagu atau Tifa")
    
    if search:
        # Mencari di tabel Supabase (Hanya yang statusnya Verified)
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Verified").or_(f"kata_asmat.ilike.%{search}%,arti_indonesia.ilike.%{search}%").execute()
        
        if res.data:
            for item in res.data:
                st.markdown(f"""
                <div style="background-color: #F5F5DC; border-left: 10px solid #8B4513; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <h3 style="margin:0; color: #8B4513;">{item['kata_asmat']}</h3>
                    <p style="margin:0; color: #5D4037;">Artinya: <b>{item['arti_indonesia']}</b></p>
                    <small style="color: #8B4513;">Kategori: {item.get('kategori', 'Umum')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"Kata '{search}' belum ditemukan atau belum diverifikasi oleh Admin.")

# --- TAB 2: KONTRIBUSI ---
with tab_kontribusi:
    st.subheader("📝 Sumbangkan Kata Baru")
    st.write("Bantu kami melengkapi database bahasa Asmat Bismam.")
    
    metode = st.segmented_control("Metode Input:", ["⌨️ Teks", "🎙️ Audio"], default="⌨️ Teks")
    
    if metode == "⌨️ Teks":
        with st.form("form_kontribusi", clear_on_submit=True):
            kat = st.selectbox("Pilih Kategori:", list(DAFTAR_KATA.keys()) + ["✨ Lainnya"])
            nama = st.text_input("Nama Anda (Opsional)")
            kata_indo = st.text_input("Kata dalam Bahasa Indonesia")
            kata_asmat = st.text_input("Bahasa Asmat-nya")
            
            if st.form_submit_button("KIRIM TERJEMAHAN"):
                if kata_indo and kata_asmat:
                    data = {
                        "nama_penyumbang": nama if nama else "Anonim",
                        "kata_asmat": kata_asmat,
                        "arti_indonesia": kata_indo,
                        "kategori": kat,
                        "status_verifikasi": "Pending"
                    }
                    supabase.table("kamus_bismam").insert(data).execute()
                    st.success("Terima kasih! Kontribusi Anda akan diperiksa oleh Admin.")
                else:
                    st.error("Mohon isi kata Indonesia dan Asmat terlebih dahulu.")
    
    else:
        st.info("Gunakan mikrofon untuk merekam cara pengucapan kata.")
        audio = st.audio_input("Rekam Suara Anda")
        if audio:
            st.success("Rekaman berhasil diunggah! Admin akan mendengarkan dan mencatatnya.")

# --- TAB 3: ADMIN ---
with tab_admin:
    st.subheader("🛡️ Verifikasi Admin")
    admin_pass = st.text_input("Masukkan Kode Akses Admin", type="password")
    
    # Password default 'Bismam2026', bisa diubah di Secrets
    if admin_pass == st.secrets.get("ADMIN_PASSWORD", "Bismam2026"):
        st.success("Akses Diterima.")
        
        # Ambil data yang statusnya masih 'Pending'
        res_pending = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
        
        if res_pending.data:
            st.write(f"Terdapat **{len(res_pending.data)}** kata menunggu verifikasi:")
            for item in res_pending.data:
                with st.expander(f"📌 {item['kata_asmat']} - {item['arti_indonesia']}"):
                    st.write(f"Penyumbang: {item['nama_penyumbang']}")
                    st.write(f"Kategori: {item['kategori']}")
                    
                    col_setuju, col_hapus = st.columns(2)
                    if col_setuju.button("SETUJUI ✅", key=f"setuju_{item['id']}"):
                        supabase.table("kamus_bismam").update({"status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                        st.rerun()
                    
                    if col_hapus.button("HAPUS ❌", key=f"hapus_{item['id']}"):
                        supabase.table("kamus_bismam").delete().eq("id", item['id']).execute()
                        st.rerun()
        else:
            st.info("Tidak ada data baru yang perlu diverifikasi.")
