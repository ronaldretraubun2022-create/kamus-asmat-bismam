import streamlit as st
from supabase import create_client, Client
import pandas as pd
import io

# --- KONEKSI KE DATABASE ---
SUPABASE_URL = "https://obmomopxcmsgzjjseevh.supabase.co"
SUPABASE_KEY = "sb_publishable_dblztCyFjxkydZCGjlEMCQ_1CMxgsuI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- TAMPILAN HEADER ---
# --- KODE PEMBERSIH TOTAL ---
st.markdown(
    """
    <style>
    /* 1. Hilangkan Header & Footer Atas */
    header, footer, .stDeployButton, #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    /* 2. PAKSA HILANGKAN TOMBOL GITHUB (POJOK KANAN BAWAH) */
    [data-testid="stStatusWidget"], 
    .viewerBadge_container__1QS1n, 
    .viewerBadge_link__1QS1n, 
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- TAMPILAN HEADER DENGAN LOGO ---
col1, col2, col3 = st.columns([1, 1, 1])
# --- TAMPILAN HEADER DENGAN LOGO ---
col1, col2, col3 = st.columns([1, 1, 1])
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    # Menggunakan gambar perisai Asmat sebagai identitas budaya
    # Menampilkan logo Museum Asmat yang baru diupload
        st.image("MUSEUM ASMAT.png", width=150)

st.markdown("<h1 style='text-align: center; color: #8B4513; margin-bottom: 0;'>🏹 KAMUS BAHASA ASMAT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #5D4037; font-weight: bold; font-size: 20px;'>RUMPUN BISMAM</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6F4E37; font-style: italic;'>Melestarikan Budaya Lewat Bahasa - Papua Selatan</p>", unsafe_allow_html=True)
st.divider()

# Menu Samping
menu = st.sidebar.radio("Pilih Menu:", ["🔍 Cari Kata", "📝 Setor Kata (Murid/Guru)", "🛡️ Verifikasi Admin"])

# --- MENU 1: CARI KATA ---
if menu == "🔍 Cari Kata":
    st.subheader("Cari Kosakata")
    search = st.text_input("Ketik kata dalam Asmat atau Indonesia...")
    if search:
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Verified").or_(f"kata_asmat.ilike.%{search}%,arti_indonesia.ilike.%{search}%").execute()
        if res.data:
                    # --- TAMPILAN KARTU KAMUS ETNIK ---
                    for item in res.data:
                        st.markdown(f"""
                        <div style="
                            border: 1px solid #EADDCA; 
                            border-left: 8px solid #8B4513; 
                            padding: 20px; 
                            border-radius: 15px; 
                            background-color: #FFFDF9; 
                            margin-bottom: 15px; 
                            box-shadow: 2px 4px 8px rgba(0,0,0,0.05);
                        <h2 style="margin: 0; color: #8B4513; font-family: sans-serif;">{item['kata_asmat']}</h2>
                    <hr style="border: 0.5px solid #EADDCA; margin: 10px 0;">
                    <p style="margin: 5px 0; color: #5D4037; font-size: 18px;">
                        <span style="background-color: #8B4513; color: white; padding: 2px 8px; border-radius: 5px; font-size: 14px; margin-right: 10px;">Arti</span>
                        <b>{item['arti_indonesia']}</b>
                    </p>
                    <div style="margin-top: 10px; padding: 10px; background-color: #F5F5DC; border-radius: 8px; border-left: 3px solid #6F4E37;">
                        <p style="margin: 0; color: #6F4E37; font-style: italic; font-size: 15px;">
                            "Contoh: {item['contoh_kalimat']}"
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Kata belum ditemukan atau masih menunggu verifikasi.")

# --- MENU 2: SETOR KATA ---
elif menu == "📝 Setor Kata (Murid/Guru)":
    st.subheader("Kontribusi Kosa Kata Baru")
    with st.form("form_setor", clear_on_submit=True):
        nama = st.text_input("Nama Penyumbang")
        kata_asmat = st.text_input("Kata dalam Bahasa Asmat")
        arti_indo = st.text_input("Arti dalam Bahasa Indonesia")
        contoh = st.text_area("Contoh Kalimat (Opsional)")
        
        submit = st.form_submit_button("Kirim ke Tim Tata Bahasa")
        
        if submit:
            if kata_asmat and arti_indo:
                data = {
                    "nama_penyumbang": nama,
                    "kata_asmat": kata_asmat,
                    "arti_indonesia": arti_indo,
                    "contoh_kalimat": contoh,
                    "status_verifikasi": "Pending"
                }
                supabase.table("kamus_bismam").insert(data).execute()
                st.success(f"Terima kasih {nama}! Data sedang diproses untuk verifikasi.")
            else:
                st.error("Mohon isi kata Asmat dan artinya.")

# --- MENU 3: VERIFIKASI ADMIN ---
elif menu == "🛡️ Verifikasi Admin":
    st.subheader("Panel Verifikasi Tim Tata Bahasa")
    password = st.text_input("Masukkan Kode Akses Admin", type="password")
    
    if password == "Bismam2026":
        # --- TOMBOL DOWNLOAD DATABASE UNTUK ADMIN ---
        st.info("📊 Panel Download Database")
        all_data = supabase.table("kamus_bismam").select("*").execute()
        if all_data.data:
            df_admin = pd.DataFrame(all_data.data)
            output_admin = io.BytesIO()
            with pd.ExcelWriter(output_admin, engine='openpyxl') as writer:
                df_admin.to_excel(writer, index=False)
            
            st.download_button(
                label="📥 Download Database Lengkap (Excel)",
                data=output_admin.getvalue(),
                file_name="Kamus_Asmat_Bismam_Lengkap.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        st.divider()
        
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
        if res.data:
            for item in res.data:
                with st.expander(f"Cek: {item['kata_asmat']}"):
                    new_indo = st.text_input("Koreksi Arti", value=item['arti_indonesia'], key=f"id_{item['id']}")
                    if st.button("Verifikasi & Terbitkan", key=f"btn_{item['id']}"):
                        supabase.table("kamus_bismam").update({"arti_indonesia": new_indo, "status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                        st.rerun()
        else:
            st.info("Semua data sudah diverifikasi.")
