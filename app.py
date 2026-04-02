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
    
    /* Styling Box Input & Selectbox */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
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
        z-index: 999;
    }

    /* Styling khusus Google Translate */
    .goog-te-gadget { font-family: sans-serif !important; color: #EADDCA !important; }
    .goog-te-gadget-simple {
        background-color: #3E2723 !important;
        border: 1px solid #8B4513 !important;
        padding: 5px !important;
        border-radius: 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA KOSA KATA LENGKAP (SESUAI INPUT ANDA) ---
DAFTAR_KATA = {
    "🦴 Anatomi: Bagian Luar": [
        "Kepala", "Rambut", "Dahi", "Mata", "Alis", "Bulu mata", "Hidung", "Pipi", "Mulut", "Bibir", 
        "Gigi", "Lidah", "Telinga", "Dagu", "Leher", "Bahu", "Dada", "Perut", "Punggung", "Pinggang", 
        "Lengan", "Siku", "Tangan", "Jari tangan", "Kuku", "Paha", "Lutut", "Betis", "Kaki", "Tumit", "Jari kaki"
    ],
    "🫀 Anatomi: Dalam & Sistem": [
        "Otak", "Jantung", "Paru-paru", "Hati", "Lambung", "Usus", "Ginjal", "Pankreas", "Limpa", "Kandung kemih",
        "Darah", "Arteri", "Vena", "Kapiler", "Denyut nadi", "Tulang", "Sendi", "Otot", "Ligamen", "Tendon", 
        "Saraf", "Sumsum tulang belakang", "Sel", "Jaringan", "Organ", "Sistem tubuh", "Hormon", "Enzim"
    ],
    "🍳 Alat Masak": [
        "Kompor", "Wajan", "Panci", "Dandang", "Teko", "Oven", "Microwave", "Rice cooker", "Pemanggang (grill)", "Kukusan",
        "Pisau dapur", "Talenan", "Parutan", "Blender", "Cobek", "Ulekan", "Saringan", "Pengupas (peeler)", "Gunting dapur"
    ],
    "🍽️ Alat Makan & Wadah": [
        "Piring", "Mangkok", "Sendok", "Garpu", "Pisau makan", "Gelas", "Cangkir", "Sumpit", "Sedotan",
        "Lemari dapur", "Rak piring", "Toples", "Botol", "Kaleng", "Kotak makanan", "Kulkas", "Freezer", "Wadah plastik"
    ],
    "🧼 Perabot & Tambahan Dapur": [
        "Lap dapur", "Spons", "Sabun cuci piring", "Ember", "Tempat sampah", "Sarung tangan dapur", 
        "Penjepit makanan", "Sendok sayur", "Spatula", "Meja dapur", "Kursi", "Wastafel", "Keran air", "Rak bumbu"
    ],
    "🧂 Bumbu & Protein Sagu": [
        "Garam", "Gula", "Minyak goreng", "Kecap", "Saus", "Merica", "Bawang merah", "Bawang putih", "Cabai",
        "Sagu", "Papeda", "Sagu bakar", "Sagu lempeng", "Sagu bola-bola", "Sagu campur ikan", "Sagu kuah kuning",
        "Ulat sagu", "Ikan bakar", "Ikan asap", "Ikan kuah kuning", "Udang sungai", "Kepiting rawa", "Kerang sungai", 
        "Kura-kura", "Babi bakar", "Ulat sagu bakar", "Ulat sagu goreng", "Sate ulat sagu", "Ikan bakar batu"
    ],
    "🏹 Budaya & Ritual Asmat": [
        "Upacara adat", "Ritual leluhur", "Pesta adat", "Tarian adat", "Nyanyian adat", "Persembahan", 
        "Inisiasi (pendewasaan)", "Penghormatan leluhur", "Pembukaan lahan adat", "Upacara kematian",
        "Ukiran kayu", "Patung Asmat", "Perisai ukir", "Topeng adat", "Hiasan tubuh", "Anyaman", 
        "Jew (Rumah adat)", "Tifa", "Noken", "Tombak", "Panah", "Busur", "Perahu kano"
    ],
    "🐾 Hewan (Darat & Khas Papua)": [
        "Anjing", "Kucing", "Babi", "Kambing", "Sapi", "Kuda", "Tikus", "Kelelawar", "Kanguru pohon", 
        "Kasuari", "Rusa", "Babi hutan", "Kuskus", "Walabi", "Burung nuri", "Burung cenderawasih", "Burung elang"
    ],
    "🐊 Hewan (Air, Melata, Serangga)": [
        "Ikan", "Udang", "Kepiting", "Kerang", "Buaya", "Belut", "Ikan gabus", "Ikan arwana", 
        "Ular", "Kadal", "Biawak", "Penyu", "Kura-kura", "Katak", "Kodok",
        "Semut", "Nyamuk", "Lalat", "Kupu-kupu", "Lebah", "Belalang", "Kumbang", "Rayap"
    ],
    "✨ Kategori Lainnya": []
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
    st.info("Fokus: Pelestarian Bahasa Asmat Rumpun Bismam.")

# --- 6. HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try: st.image("MUSEUM ASMAT.png", width=150)
    except: st.markdown("<h1 style='text-align: center; color: #8B4513;'>🏹</h1>", unsafe_allow_html=True)

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

# --- TAB 2: KONTRIBUSI (DINAMIS & LENGKAP) ---
with tab_kontribusi:
    st.subheader("📝 Sumbangkan Kata Baru")
    st.write("Pilih kategori dan kata Indonesia, lalu isi padanan Bahasa Asmat-nya.")
    
    # Letakkan di luar form agar selectbox kedua bisa merespon selectbox pertama
    kat_pilihan = st.selectbox("1. Pilih Kategori:", list(DAFTAR_KATA.keys()))
    
    with st.form("form_kontribusi", clear_on_submit=True):
        if kat_pilihan == "✨ Kategori Lainnya":
            kata_indo_final = st.text_input("2. Ketik Kata Bahasa Indonesia Baru:")
        else:
            # Dropdown ini sekarang otomatis terupdate sesuai kategori di atas
            kata_indo_final = st.selectbox("2. Pilih Kata Bahasa Indonesia:", DAFTAR_KATA[kat_pilihan])
        
        kata_asmat = st.text_input("3. Tuliskan Bahasa Asmat Rumpun Bismam-nya:")
        nama_p = st.text_input("Nama Penyumbang (Opsional)")
        
        if st.form_submit_button("KIRIM TERJEMAHAN"):
            if kata_indo_final and kata_asmat:
                supabase.table("kamus_bismam").insert({
                    "kata_asmat": kata_asmat, "arti_indonesia": kata_indo_final, 
                    "kategori": kat_pilihan, "nama_penyumbang": nama_p if nama_p else "Anonim",
                    "status_verifikasi": "Pending"
                }).execute()
                st.success(f"Terima kasih! Terjemahan untuk '{kata_indo_final}' telah dikirim ke Admin.")
            else:
                st.error("Mohon isi terjemahan Bahasa Asmat.")

# --- TAB 3: ADMIN ---
with tab_admin:
    st.subheader("🛡️ Verifikasi Admin")
    admin_pass = st.text_input("Kode Akses", type="password")
    if admin_pass == st.secrets.get("ADMIN_PASSWORD", "Bismam2026"):
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
        if res.data:
            for item in res.data:
                with st.expander(f"📌 {item['kata_asmat']} - {item['arti_indonesia']}"):
                    c1, c2 = st.columns(2)
                    if c1.button("SETUJUI ✅", key=f"s_{item['id']}"):
                        supabase.table("kamus_bismam").update({"status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                        st.rerun()
                    if c2.button("HAPUS ❌", key=f"h_{item['id']}"):
                        supabase.table("kamus_bismam").delete().eq("id", item['id']).execute()
                        st.rerun()
        else: st.info("Tidak ada data pending.")

# --- FOOTER ---
st.markdown("""<div class="footer">© 2026 Kamus Digital Asmat Rumpun Bismam - Papua Selatan</div>""", unsafe_allow_html=True)
