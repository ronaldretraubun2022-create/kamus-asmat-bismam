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
    "🦴 Anatomi": ["Kepala", "Rambut", "Mata", "Hidung", "Telinga", "Mulut", "Tangan", "Kaki"],
    "🍳 Alat Masak": ["Wajan", "Panci", "Pisau", "Teko", "Saringan"],
    "🧂 Bumbu & Protein": ["Sagu", "Papeda", "Ikan", "Udang", "Garam", "Gula"],
    "🏹 Budaya & Ritual": ["Tifa", "Noken", "Jew", "Ukiran", "Perahu"],
    "✨ Kategori Lainnya": []
}

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🌐 Navigasi")
    st.info("Fokus: Pelestarian Bahasa Asmat Rumpun Bismam.")
    st.divider()

# --- 6. HEADER ---
st.markdown("<h2 style='text-align: center; color: #8B4513; font-weight: bold;'>KAMUS DIGITAL BAHASA ASMAT<br>RUMPUN BISMAM</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #6F4E37;'>Melestarikan Budaya Lewat Bahasa - Papua Selatan</p>", unsafe_allow_html=True)
st.divider()

# --- 7. NAVIGASI TABS ---
tab_cari, tab_kontribusi, tab_admin = st.tabs(["🔍 CARI KATA", "📝 KONTRIBUSI", "🛡️ ADMIN"])

# --- TAB 1: CARI KATA ---
with tab_cari:
    search = st.text_input("Ketik kata dalam Bahasa Indonesia atau Asmat...", placeholder="Cari kata...")
    if search:
        # Menyesuaikan query dengan status_verifikasi 'Verified'
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Verified").or_(f"kata_asmat.ilike.%{search}%,arti_indonesia.ilike.%{search}%").execute()
        if res.data:
            for item in res.data:
                st.markdown(f"""
                <div style="background-color: #F5F5DC; border-left: 10px solid #8B4513; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <h3 style="margin:0; color: #8B4513;">{item['kata_asmat']}</h3>
                    <p style="margin:0; color: #5D4037;">Artinya: <b>{item['arti_indonesia']}</b></p>
                </div>
                """, unsafe_allow_html=True)
        else: st.warning("Kata belum ditemukan atau belum diverifikasi.")

# --- TAB 2: KONTRIBUSI (BAGIAN PERBAIKAN UTAMA) ---
with tab_kontribusi:
    st.subheader("📝 Kontribusi Baru")
    kat_pilihan = st.selectbox("1. Pilih Kategori:", list(DAFTAR_KATA.keys()))
    
    with st.form("form_kontribusi", clear_on_submit=True):
        if kat_pilihan == "✨ Kategori Lainnya":
            kata_indo_input = st.text_input("2. Ketik Kata Indonesia Baru:")
        else:
            kata_indo_input = st.selectbox("2. Pilih Kata Bahasa Indonesia:", DAFTAR_KATA[kat_pilihan])
        
        kata_asmat_input = st.text_input("3. Tuliskan Bahasa Asmat Rumpun Bismam-nya:")
        nama_p = st.text_input("Nama Penyumbang (Opsional)")
        
        if st.form_submit_button("KIRIM TERJEMAHAN"):
            if kata_indo_input and kata_asmat_input:
                try:
                    # PERBAIKAN: Nama kolom disamakan dengan Supabase (kontributor_name)
                    supabase.table("kamus_bismam").insert({
                        "kata_asmat": kata_asmat_input, 
                        "arti_indonesia": kata_indo_input, 
                        "kategori": kat_pilihan, 
                        "kontributor_name": nama_p if nama_p else "Anonim", # SESUAI GAMBAR DB
                        "status_verifikasi": "Pending"
                    }).execute()
                    st.success("Berhasil dikirim! Menunggu verifikasi admin.")
                except Exception as e:
                    st.error(f"Gagal mengirim data. Pastikan semua kolom di Supabase sudah benar. Detail: {e}")
            else: st.error("Mohon lengkapi data kata.")

# --- TAB 3: ADMIN ---
with tab_admin:
    admin_pass = st.text_input("Masukkan Kode Akses Admin", type="password")
    if admin_pass == st.secrets.get("ADMIN_PASSWORD", "Bismam2026"):
        try:
            res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
            if res.data:
                for item in res.data:
                    st.write(f"**{item['kata_asmat']}** = {item['arti_indonesia']} ({item['kategori']})")
                    c1, c2 = st.columns(2)
                    if c1.button("Setujui", key=f"v_{item['id']}"):
                        supabase.table("kamus_bismam").update({"status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                        st.rerun()
                    if c2.button("Hapus", key=f"d_{item['id']}"):
                        supabase.table("kamus_bismam").delete().eq("id", item['id']).execute()
                        st.rerun()
            else: st.success("Tidak ada data pending.")
        except Exception as e:
            st.error(f"Error admin: {e}")

# --- FOOTER ---
st.markdown("""<div class="footer">© 2026 Kamus Digital Asmat Rumpun Bismam - Papua Selatan</div>""", unsafe_allow_html=True)
