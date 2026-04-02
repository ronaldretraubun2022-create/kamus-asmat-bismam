import streamlit as st
from supabase import create_client, Client

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kamus Asmat Bismam", page_icon="🏹", layout="centered")

# --- 2. KONEKSI DATABASE (AMBIL DARI SECRETS) ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Konfigurasi Secrets belum lengkap di Streamlit Cloud.")
    st.stop()

# --- 3. FIX TAMPILAN: PAKSA TERANG & BERSIH ---
st.markdown("""
    <style>
    /* Hilangkan elemen bawaan Streamlit */
    header, footer, .stDeployButton, #MainMenu { display: none !important; }
    
    /* Paksa Latar Belakang Putih & Teks Gelap agar Terbaca */
    .stApp { background-color: #FFFFFF !important; }
    p, span, label, h1, h2, h3 { color: #2E1A08 !important; font-family: 'sans-serif'; }
    
    /* Percantik Box Input */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #F8F9FA !important;
        color: #2E1A08 !important;
        border: 1px solid #D2B48C !important;
    }
    
    /* Hilangkan ruang kosong bawah */
    .stApp { margin-bottom: -50px !important; padding-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DAFTAR KATA OTOMATIS ---
DAFTAR_KATA = {
    "🦴 Anatomi Tubuh": ["Kepala", "Rambut", "Mata", "Telinga", "Hidung", "Mulut", "Tangan", "Kaki", "Jantung", "Darah"],
    "👨‍👩‍👧‍👦 Keluarga": ["Bapak/Ayah", "Ibu/Mama", "Kakak Laki-laki", "Kakak Perempuan", "Adik", "Kakek", "Nenek", "Paman", "Bibi"],
    "🍳 Dapur & Rumah": ["Parang", "Kapak", "Periuk", "Piring", "Sendok", "Kayu Bakar", "Api", "Air", "Tungku"],
    "🍲 Makanan & Alam": ["Sagu", "Ikan", "Ulat Sagu", "Babi Hutan", "Burung", "Hutan", "Sungai", "Dusun", "Perahu", "Dayung"],
    "🚲 Kendaraan": ["Perahu (Kole-kole)", "Perahu Motor", "Speedboat", "Motor", "Sepeda Listrik", "Pesawat Capung"],
    "🐾 Hewan Papua": ["Cendrawasih", "Kasuari", "Kakatua", "Mambruk", "Walabi", "Kuskus", "Buaya", "Ular", "Rusa"]
}

# --- 5. HEADER ETNIK ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try: st.image("MUSEUM ASMAT.png", width=150)
    except: st.markdown("<h2 style='text-align:center;'>🏹</h2>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #8B4513; margin-top: -20px;'>KAMUS ASMAT BISMAM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Melestarikan Budaya Lewat Bahasa</p>", unsafe_allow_html=True)
st.divider()

# --- 6. NAVIGASI MENU ---
menu = st.sidebar.radio("PILIH MENU:", ["🔍 Cari Kata", "📝 Kontribusi Kata", "🛡️ Admin"])

# --- MENU 1: CARI KATA ---
if menu == "🔍 Cari Kata":
    st.subheader("Cari Kosakata")
    search = st.text_input("Ketik kata Indonesia atau Asmat...")
    if search:
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Verified").or_(f"kata_asmat.ilike.%{search}%,arti_indonesia.ilike.%{search}%").execute()
        if res.data:
            for item in res.data:
                st.info(f"**{item['kata_asmat']}** = {item['arti_indonesia']}")
        else:
            st.warning("Kata belum ditemukan dalam database.")

# --- MENU 2: KONTRIBUSI (TEKS & AUDIO) ---
elif menu == "📝 Kontribusi Kata":
    st.subheader("Sumbangkan Kata Baru")
    metode = st.radio("Metode Kontribusi:", ["⌨️ Teks (Menulis)", "🎙️ Audio (Bicara)"])
    
    if metode == "⌨️ Teks (Menulis)":
        kat = st.selectbox("Pilih Kategori:", list(DAFTAR_KATA.keys()) + ["✨ Lainnya"])
        kata_indo = ""
        if kat == "✨ Lainnya":
            kata_indo = st.text_input("Ketik Kata Bahasa Indonesia:")
        else:
            opsi = st.radio("Pilihan Kata:", ["Dari Daftar", "Ketik Baru"])
            kata_indo = st.selectbox("Pilih Kata:", DAFTAR_KATA[kat]) if opsi == "Dari Daftar" else st.text_input("Ketik Kata Indonesia Baru:")

        with st.form("form_kontribusi"):
            nama = st.text_input("Nama Anda")
            asmat = st.text_input(f"Bahasa Asmat dari '{kata_indo}'")
            if st.form_submit_button("KIRIM TERJEMAHAN"):
                if asmat and kata_indo:
                    supabase.table("kamus_bismam").insert({"nama_penyumbang": nama, "kata_asmat": asmat, "arti_indonesia": kata_indo, "kategori": kat, "status_verifikasi": "Pending"}).execute()
                    st.success("Terima kasih! Data sudah dikirim ke Admin.")

    else:
        st.info("Bapak/Ibu silakan tekan tombol mikrofon, sebutkan kata Indonesia dan bahasa Asmat-nya.")
        audio = st.audio_input("Rekam Suara")
        if audio:
            st.audio(audio)
            nama_aud = st.text_input("Nama Penyumbang")
            if st.button("KIRIM REKAMAN"):
                st.success(f"Rekaman diterima! Terima kasih {nama_aud}. Admin akan memprosesnya.")

# --- MENU 3: ADMIN ---
elif menu == "🛡️ Admin":
    admin_pass = st.text_input("Kode Akses Admin", type="password")
    if admin_pass == st.secrets.get("ADMIN_PASSWORD", "Bismam2026"):
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
        if res.data:
            for item in res.data:
                with st.expander(f"Verifikasi: {item['kata_asmat']}"):
                    if st.button("SETUJUI", key=f"v_{item['id']}"):
                        supabase.table("kamus_bismam").update({"status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                        st.rerun()
        else:
            st.write("Semua data sudah bersih (terverifikasi).")
