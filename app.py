import streamlit as st
from supabase import create_client, Client

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kamus Asmat Bismam", page_icon="🏹")

# --- KONEKSI KE DATABASE (VERSI AMAN DENGAN SECRETS) ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Gagal memuat kunci keamanan. Pastikan Secrets sudah diatur di Streamlit.")
    st.stop()

# --- KODE PEMBERSIH TAMPILAN (POJOK KANAN BERSIH) ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu { display: none !important; visibility: hidden !important; }
    .stApp { margin-bottom: -60px !important; padding-bottom: 0px !important; background-color: #FFFDF9; }
    </style>
    """, unsafe_allow_html=True)

# --- DAFTAR KATA UMUM (OTOMATIS) ---
DAFTAR_KATA = {
    "🦴 Anatomi Tubuh": ["Kepala", "Rambut", "Mata", "Telinga", "Hidung", "Mulut", "Tangan", "Kaki", "Jantung", "Darah"],
    "👨‍👩‍👧‍👦 Panggilan Keluarga": ["Bapak/Ayah", "Ibu/Mama", "Kakak Laki-laki", "Kakak Perempuan", "Adik", "Kakek", "Nenek", "Paman", "Bibi", "Sepupu"],
    "🍳 Peralatan Dapur": ["Parang", "Kapak", "Periuk", "Piring", "Sendok", "Kayu Bakar", "Api", "Air Minum", "Tungku"],
    "🍲 Makanan & Alam": ["Sagu", "Ikan", "Ulat Sagu", "Babi Hutan", "Burung", "Hutan", "Sungai", "Dusun", "Perahu", "Dayung"],
    "🚲 Kendaraan": ["Perahu (Kole-kole)", "Perahu Motor (Longboat)", "Kapal", "Speedboat", "Motor", "Sepeda Listrik", "Pesawat Capung"],
    "🐾 Hewan Papua": ["Cendrawasih", "Kasuari", "Kakatua", "Mambruk", "Walabi", "Kuskus", "Buaya", "Ular Piton", "Ikan Arwana", "Rusa"]
}

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #8B4513;'>🏹 KAMUS ASMAT BISMAM</h1>", unsafe_allow_html=True)
st.divider()

# --- MENU SAMPING ---
menu = st.sidebar.radio("Pilih Menu:", ["🔍 Cari Kata", "📝 Kontribusi Kata", "🛡️ Admin"])

# --- MENU 1: CARI KATA ---
if menu == "🔍 Cari Kata":
    st.subheader("Cari Kosakata")
    search = st.text_input("Ketik kata Indonesia atau Asmat...")
    if search:
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Verified").or_(f"kata_asmat.ilike.%{search}%,arti_indonesia.ilike.%{search}%").execute()
        if res.data:
            for item in res.data:
                st.success(f"**{item['kata_asmat']}** = {item['arti_indonesia']}")
        else:
            st.info("Kata belum ditemukan.")

# --- MENU 2: KONTRIBUSI (TERMASUK AUDIO) ---
elif menu == "📝 Kontribusi Kata":
    st.subheader("Bantu Terjemahkan Kata")
    metode = st.radio("Pilih Cara Kontribusi:", ["⌨️ Teks (Menulis)", "🎙️ Audio (Bicara/Rekam)"])
    
    if metode == "⌨️ Teks (Menulis)":
        kat_pilihan = st.selectbox("Pilih Kategori:", list(DAFTAR_KATA.keys()) + ["✨ Lainnya"])
        kata_indo = ""
        if kat_pilihan == "✨ Lainnya":
            kata_indo = st.text_input("Ketik Kata Bahasa Indonesia:")
        else:
            opsi = st.radio("Pilihan Kata:", ["Dari Daftar", "Ketik Baru"])
            if opsi == "Dari Daftar":
                kata_indo = st.selectbox("Pilih Kata:", DAFTAR_KATA[kat_pilihan])
            else:
                kata_indo = st.text_input("Ketik Kata Indonesia Baru:")

        with st.form("form_teks"):
            nama = st.text_input("Nama Penyumbang")
            kata_asmat = st.text_input(f"Bahasa Asmat dari '{kata_indo}'")
            if st.form_submit_button("Kirim Teks"):
                if kata_asmat:
                    data = {"nama_penyumbang": nama, "kata_asmat": kata_asmat, "arti_indonesia": kata_indo, "kategori": kat_pilihan, "status_verifikasi": "Pending"}
                    supabase.table("kamus_bismam").insert(data).execute()
                    st.success("Terima kasih! Data sudah terkirim ke Admin.")

    else:
        st.info("Bapak/Ibu silakan bicara, sebutkan kata Indonesia dan bahasa Asmat-nya.")
        audio_file = st.audio_input("Rekam Suara")
        if audio_file:
            st.audio(audio_file)
            nama_audio = st.text_input("Nama Penyumbang")
            if st.button("Kirim Rekaman"):
                st.success(f"Terima kasih {nama_audio}! Rekaman diterima. Admin akan mengetikkannya untuk Anda.")

# --- MENU 3: ADMIN ---
elif menu == "🛡️ Admin":
    pwd = st.text_input("Password Admin", type="password")
    if pwd == st.secrets.get("ADMIN_PASSWORD", "Bismam2026"):
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
        if res.data:
            for item in res.data:
                with st.expander(f"Verifikasi: {item['kata_asmat']}"):
                    if st.button("Setujui", key=f"v_{item['id']}"):
                        supabase.table("kamus_bismam").update({"status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                        st.rerun()
        else:
            st.write("Tidak ada antrean verifikasi.")
