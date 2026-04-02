Minta maaf sekali, ini murni kesalahan teknis pada penulisan parameter `order`. Di versi terbaru pustaka Supabase untuk Python, parameter untuk mengurutkan data bukan lagi `descending=True`, melainkan menggunakan argumen `desc=True`.

Inilah penyebab munculnya pesan error *unexpected keyword argument 'descending'*. Saya sudah memperbaiki baris tersebut agar Panel Admin Anda bisa terbuka dengan lancar.

Berikut adalah kode lengkap yang sudah diperbaiki:

```python
import streamlit as st
from supabase import create_client, Client
import requests

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

# --- 4. DATA KOSA KATA LENGKAP ---
DAFTAR_KATA = {
    "🦴 Anatomi: Bagian Luar": ["Kepala", "Rambut", "Dahi", "Mata", "Alis", "Bulu mata", "Hidung", "Pipi", "Mulut", "Bibir", "Gigi", "Lidah", "Telinga", "Dagu", "Leher", "Bahu", "Dada", "Perut", "Punggung", "Pinggang", "Lengan", "Siku", "Tangan", "Jari tangan", "Kuku", "Paha", "Lutut", "Betis", "Kaki", "Tumit", "Jari kaki"],
    "🫀 Anatomi: Dalam & Sistem": ["Otak", "Jantung", "Paru-paru", "Hati", "Lambung", "Usus", "Ginjal", "Pankreas", "Limpa", "Kandung kemih", "Darah", "Arteri", "Vena", "Tulang", "Sendi", "Otot", "Ligamen", "Tendon", "Saraf", "Sumsum tulang belakang", "Sel", "Jaringan", "Organ", "Sistem tubuh", "Hormon", "Enzim"],
    "🍳 Alat Masak": ["Kompor", "Wajan", "Panci", "Dandang", "Teko", "Oven", "Microwave", "Rice cooker", "Pemanggang (grill)", "Kukusan", "Pisau dapur", "Talenan", "Parutan", "Blender", "Cobek", "Ulekan", "Saringan", "Pengupas (peeler)", "Gunting dapur"],
    "🍽️ Alat Makan & Wadah": ["Piring", "Mangkok", "Sendok", "Garpu", "Pisau makan", "Gelas", "Cangkir", "Sumpit", "Sedotan", "Lemari dapur", "Rak piring", "Toples", "Botol", "Kaleng", "Kotak makanan", "Kulkas", "Freezer", "Wadah plastik"],
    "🧼 Perabot & Tambahan Dapur": ["Lap dapur", "Spons", "Sabun cuci piring", "Ember", "Tempat sampah", "Sarung tangan dapur", "Penjepit makanan", "Sendok sayur", "Spatula", "Meja dapur", "Kursi", "Wastafel", "Keran air", "Rak bumbu"],
    "🧂 Bumbu & Protein Sagu": ["Garam", "Gula", "Minyak goreng", "Kecap", "Saus", "Merica", "Bawang merah", "Bawang putih", "Cabai", "Sagu", "Papeda", "Sagu bakar", "Sagu lempeng", "Sagu bola-bola", "Sagu campur ikan", "Sagu kuah kuning", "Ulat sagu", "Ikan bakar", "Ikan asap", "Ikan kuah kuning", "Udang sungai", "Kepiting rawa", "Kerang sungai", "Kura-kura", "Babi bakar", "Ulat sagu bakar", "Ulat sagu goreng", "Sate ulat sagu", "Ikan bakar batu"],
    "🏹 Budaya & Ritual Asmat": ["Upacara adat", "Ritual leluhur", "Pesta adat", "Tarian adat", "Nyanyian adat", "Persembahan", "Inisiasi (pendewasaan)", "Penghormatan leluhur", "Pembukaan lahan adat", "Upacara kematian", "Ukiran kayu", "Patung Asmat", "Perisai ukir", "Topeng adat", "Hiasan tubuh", "Anyaman", "Jew (Rumah adat)", "Tifa", "Noken", "Tombak", "Panah", "Busur", "Perahu kano"],
    "🐾 Hewan (Darat & Khas Papua)": ["Anjing", "Kucing", "Babi", "Kambing", "Sapi", "Kuda", "Tikus", "Kelelawar", "Kanguru pohon", "Kasuari", "Rusa", "Babi hutan", "Kuskus", "Walabi", "Burung nuri", "Burung cenderawasih", "Burung elang"],
    "🐊 Hewan (Air, Melata, Serangga)": ["Ikan", "Udang", "Kepiting", "Kerang", "Buaya", "Belut", "Ikan gabus", "Ikan arwana", "Ular", "Kadal", "Biawak", "Penyu", "Kura-kura", "Katak", "Kodok", "Semut", "Nyamuk", "Lalat", "Kupu-kupu", "Lebah", "Belalang", "Kumbang", "Rayap"],
    "✨ Kategori Lainnya": []
}

# --- 5. SIDEBAR: GOOGLE TRANSLATE ---
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
    """, height=100)
    st.divider()
    st.info("Fokus: Pelestarian Bahasa Asmat Rumpun Bismam.")

# --- 6. HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try: st.image("MUSEUM ASMAT.png", width=150)
    except: st.markdown("<h1 style='text-align: center;'>🏹</h1>", unsafe_allow_html=True)

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
        if res and hasattr(res, 'data') and res.data:
            for item in res.data:
                st.markdown(f"""
                <div style="background-color: #F5F5DC; border-left: 10px solid #8B4513; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <h3 style="margin:0; color: #8B4513;">{item['kata_asmat']}</h3>
                    <p style="margin:0; color: #5D4037;">Artinya: <b>{item['arti_indonesia']}</b></p>
                </div>
                """, unsafe_allow_html=True)
        else: st.warning("Kata belum ditemukan.")

# --- TAB 2: KONTRIBUSI ---
with tab_kontribusi:
    st.subheader("📝 Kontribusi Baru")
    kat_pilihan = st.selectbox("1. Pilih Kategori:", list(DAFTAR_KATA.keys()))
    with st.form("form_kontribusi", clear_on_submit=True):
        if kat_pilihan == "✨ Kategori Lainnya":
            kata_indo_input = st.text_input("2. Ketik Kata Indonesia Baru:")
        else:
            kata_indo_input = st.selectbox("2. Pilih Kata Bahasa Indonesia:", DAFTAR_KATA[kat_pilihan])
        
        kata_asmat = st.text_input("3. Tuliskan Bahasa Asmat Rumpun Bismam-nya:")
        nama_p = st.text_input("Nama Penyumbang (Opsional)")
        
        if st.form_submit_button("KIRIM TERJEMAHAN"):
            if kata_indo_input and kata_asmat:
                supabase.table("kamus_bismam").insert({
                    "kata_asmat": kata_asmat, "arti_indonesia": kata_indo_input, 
                    "kategori": kat_pilihan, "nama_penyumbang": nama_p if nama_p else "Anonim",
                    "status_verifikasi": "Pending"
                }).execute()
                st.success("Berhasil dikirim!")
            else: st.error("Lengkapi data.")

# --- TAB 3: ADMIN (PERBAIKAN PARAMETER ORDER) ---
with tab_admin:
    st.subheader("🛡️ Panel Verifikasi")
    admin_pass = st.text_input("Masukkan Kode Akses Admin", type="password")
    
    if admin_pass == st.secrets.get("ADMIN_PASSWORD", "Bismam2026"):
        try:
            # PERBAIKAN: Menggunakan desc=True untuk versi terbaru supabase-py
            res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").order("created_at", desc=True).execute()
            
            if res and hasattr(res, 'data') and len(res.data) > 0:
                st.info(f"Ada {len(res.data)} data baru yang perlu diperiksa.")
                
                for item in res.data:
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color: #EADDCA; padding: 10px; border-radius: 10px; border: 1px solid #8B4513; margin-bottom: 5px;">
                            <strong>Kategori: {item['kategori']}</strong><br>
                            <h4 style="margin:5px 0;">{item['kata_asmat']} = {item['arti_indonesia']}</h4>
                            <small>Penyumbang: {item.get('nama_penyumbang', 'Anonim')}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        c1, c2 = st.columns(2)
                        if c1.button(f"SETUJUI ✅", key=f"v_{item['id']}"):
                            supabase.table("kamus_bismam").update({"status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                            st.rerun()
                        if c2.button(f"HAPUS ❌", key=f"d_{item['id']}"):
                            supabase.table("kamus_bismam").delete().eq("id", item['id']).execute()
                            st.rerun()
                        st.write("---")
            else:
                st.success("Semua data sudah terverifikasi.")
        except Exception as e:
            st.error(f"Gagal mengambil data: {e}")
    elif admin_pass != "":
        st.error("Kode akses salah.")

# --- FOOTER ---
st.markdown("""<div class="footer">© 2026 Museum Kebudayaan dan Kemajuan Asmat - Papua Selatan</div>""", unsafe_allow_html=True)
```
