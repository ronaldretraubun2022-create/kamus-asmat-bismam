import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Papsel Digital Hub", page_icon="🏹", layout="centered")

# --- 2. KONEKSI DATABASE (SUPABASE) ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Konfigurasi Secrets belum lengkap di Streamlit Cloud.")
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

# --- 4. DATA STATIC & KONSTANTA ---
DAFTAR_KATA = {
    "🦴 Anatomi Tubuh": ["Kepala", "Rambut", "Mata", "Telinga", "Hidung", "Mulut", "Tangan", "Kaki", "Jantung", "Darah"],
    "👨‍👩‍👧‍👦 Keluarga": ["Bapak/Ayah", "Ibu/Mama", "Kakak Laki-laki", "Kakak Perempuan", "Adik", "Kakek", "Nenek", "Paman", "Bibi"],
    "🍳 Dapur & Rumah": ["Parang", "Kapak", "Periuk", "Piring", "Sendok", "Kayu Bakar", "Api", "Air", "Tungku"],
    "🍲 Makanan & Alam": ["Sagu", "Ikan", "Ulat Sagu", "Babi Hutan", "Burung", "Hutan", "Sungai", "Dusun", "Perahu", "Dayung"],
    "🐾 Hewan Papua": ["Cendrawasih", "Kasuari", "Kakatua", "Mambruk", "Walabi", "Kuskus", "Buaya", "Ular", "Rusa"]
}

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h2 style='text-align: center;'>🏹 PAPSEL HUB</h2>", unsafe_allow_html=True)
main_menu = st.sidebar.selectbox(
    "PILIH LAYANAN:", 
    ["📖 Kamus Bismam", "🛒 POS UMKM Merauke", "🎨 Studio Info Papsel"]
)
st.sidebar.divider()

# --- MODUL 1: KAMUS ASMAT BISMAM ---
if main_menu == "📖 Kamus Bismam":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #8B4513;'>KAMUS BISMAM</h1>", unsafe_allow_html=True)
    
    sub_menu = st.tabs(["🔍 Cari", "📝 Kontribusi", "🛡️ Admin"])

    with sub_menu[0]:
        search = st.text_input("Ketik kata Indonesia atau Asmat...")
        if search:
            res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Verified").or_(f"kata_asmat.ilike.%{search}%,arti_indonesia.ilike.%{search}%").execute()
            if res.data:
                for item in res.data:
                    st.markdown(f"""<div style="background-color: #F5F5DC; border-left: 10px solid #8B4513; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                        <h3 style="margin:0; color: #8B4513;">{item['kata_asmat']}</h3>
                        <p style="margin:0; color: #5D4037;">Artinya: <b>{item['arti_indonesia']}</b></p>
                    </div>""", unsafe_allow_html=True)
            else: st.warning("Kata belum ditemukan.")

    with sub_menu[1]:
        metode = st.radio("Metode:", ["⌨️ Teks", "🎙️ Audio"])
        if metode == "⌨️ Teks":
            with st.form("form_kamus"):
                kat = st.selectbox("Kategori:", list(DAFTAR_KATA.keys()))
                kata_indo = st.text_input("Kata Indonesia:")
                asmat = st.text_input("Bahasa Asmat:")
                if st.form_submit_button("KIRIM"):
                    supabase.table("kamus_bismam").insert({"kata_asmat": asmat, "arti_indonesia": kata_indo, "kategori": kat, "status_verifikasi": "Pending"}).execute()
                    st.success("Berhasil dikirim!")
        else:
            audio = st.audio_input("Rekam Suara")
            if audio: st.success("Rekaman diterima untuk verifikasi!")

    with sub_menu[2]:
        admin_pass = st.text_input("Akses Admin", type="password")
        if admin_pass == st.secrets.get("ADMIN_PASSWORD", "Bismam2026"):
            res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
            for item in res.data:
                st.write(f"Verifikasi: {item['kata_asmat']} -> {item['arti_indonesia']}")
                if st.button("SETUJUI", key=item['id']):
                    supabase.table("kamus_bismam").update({"status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                    st.rerun()

# --- MODUL 2: POS UMKM MERAUKE ---
elif main_menu == "🛒 POS UMKM Merauke":
    st.markdown("<h1 style='color: #8B4513;'>🛒 Kasir UMKM Merauke</h1>", unsafe_allow_html=True)
    
    if "cart" not in st.session_state: st.session_state.cart = []

    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.subheader("Daftar Produk")
        # Contoh Produk
        items = [("Sagu Lempeng", 15000), ("Minyak Kayu Putih", 35000), ("Noken Asmat", 120000)]
        for name, price in items:
            c1, c2 = st.columns([2, 1])
            c1.write(f"**{name}** - Rp{price:,}")
            if c2.button(f"Tambah", key=name):
                st.session_state.cart.append({"nama": name, "harga": price})
    
    with col_b:
        st.subheader("Keranjang")
        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.dataframe(df_cart, hide_index=True)
            total = df_cart['harga'].sum()
            st.write(f"### Total: Rp{total:,}")
            if st.button("Kosongkan"):
                st.session_state.cart = []
                st.rerun()
            if st.button("Bayar & Cetak"): st.success("Transaksi Berhasil!")
        else: st.info("Keranjang Kosong")

# --- MODUL 3: STUDIO INFO PAPSEL ---
elif main_menu == "🎨 Studio Info Papsel":
    st.markdown("<h1 style='color: #8B4513;'>🎨 Studio Info Papsel</h1>", unsafe_allow_html=True)
    st.write("Buat layout berita sosial media otomatis.")
    
    up_file = st.file_uploader("Pilih Foto Berita", type=['jpg', 'png'])
    headline = st.text_area("Masukkan Headline Berita:")
    preset = st.selectbox("Pilih Filter:", ["Normal", "Vibrant Papua", "Bismam Brown", "Streetwear Gray"])
    
    if st.button("GENERATE KONTEN"):
        if up_file and headline:
            st.image(up_file, caption=headline, use_container_width=True)
            st.success("Konten siap diunduh! (Fitur download sedang dikembangkan)")
        else:
            st.warning("Mohon isi foto dan headline.")
