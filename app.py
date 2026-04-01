import streamlit as st
from supabase import create_client, Client

# --- KONEKSI KE DATABASE ---
SUPABASE_URL = "https://obmomopxcmsgzjjseevh.supabase.co"
SUPABASE_KEY = "sb_publishable_dblztCyFjxkydZCGjlEMCQ_1CMxgsuI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- TAMPILAN HEADER ---
st.set_page_config(page_title="Kamus Asmat Bismam", page_icon="🏹")
st.markdown("<h1 style='text-align: center; color: #8B4513;'>🏹 KAMUS BAHASA ASMAT</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #5D4037;'>RUMPUN BISMAM</h3>", unsafe_allow_html=True)
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
            for item in res.data:
                st.success(f"**{item['kata_asmat']}** = {item['arti_indonesia']}")
                st.write(f"*Contoh: {item['contoh_kalimat']}*")
        else:
            st.info("Kata belum ditemukan atau masih menunggu verifikasi.")

# --- MENU 2: SETOR KATA ---
elif menu == "📝 Setor Kata (Murid/Guru)":
    st.subheader("Kontribusi Kata Baru")
    with st.form("form_setor"):
        nama = st.text_input("Nama Lengkap")
        peran = st.selectbox("Peran", ["Murid", "Guru", "Masyarakat"])
        asmat = st.text_input("Kata Asmat Bismam")
        indo = st.text_input("Arti dalam Indonesia")
        submit = st.form_submit_button("Kirim ke Tim Tata Bahasa")
        
        if submit:
            data = {"kata_asmat": asmat, "arti_indonesia": indo, "kontributor_nama": nama, "peran_pengisi": peran, "status_verifikasi": "Pending"}
            supabase.table("kamus_bismam").insert(data).execute()
            st.success(f"Terima kasih {nama}! Data sedang diproses.")

# --- MENU 3: VERIFIKASI ADMIN ---
elif menu == "🛡️ Verifikasi Admin":
    st.subheader("Panel Verifikasi Tim Tata Bahasa")
    password = st.text_input("Masukkan Kode Akses Admin", type="password")
    
    if password == "Bismam2026": # Ganti password ini sesuai keinginanmu
        res = supabase.table("kamus_bismam").select("*").eq("status_verifikasi", "Pending").execute()
        if res.data:
            for item in res.data:
                with st.expander(f"Cek: {item['kata_asmat']}"):
                    new_indo = st.text_input("Koreksi Arti", value=item['arti_indonesia'], key=f"id_{item['id']}")
                    if st.button("Verifikasi & Terbitkan", key=f"btn_{item['id']}"):
                        supabase.table("kamus_bismam").update({"arti_indonesia": new_indo, "status_verifikasi": "Verified"}).eq("id", item['id']).execute()
                        st.rerun()
        else:
            st.write("Semua data sudah diverifikasi.")
            # --- LANJUTAN DI BAWAH KODE PENCARIAN ---
        if res.data:
            df_download = pd.DataFrame(res.data)
            
            st.divider()
            st.subheader("📥 Download Hasil")
            
            # Fungsi PDF
            def buat_pdf(data):
                buf = io.BytesIO()
                c = canvas.Canvas(buf, pagesize=letter)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(100, 750, "Kamus Asmat Rumpun Bismam")
                y = 720
                c.setFont("Helvetica", 12)
                for item in data:
                    c.drawString(100, y, f"- {item['kata_asmat']}: {item['arti_indonesia']}")
                    y -= 20
                c.save()
                return buf.getvalue()

            # Fungsi Excel
            def buat_excel(df):
                buf = io.BytesIO()
                with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                return buf.getvalue()

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📊 Download Excel", data=buat_excel(df_download), file_name="Kamus_Asmat.xlsx")
            with col2:
                st.download_button("📄 Download PDF", data=buat_pdf(res.data), file_name="Kamus_Asmat.pdf")
