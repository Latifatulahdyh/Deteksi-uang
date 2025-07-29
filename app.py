import streamlit as st
import numpy as np
import os
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import gdown

model_path = "model_uang_emisi22.keras"
gdrive_id = "1QqspVQu0Z6_Ex5Yvql39Bs9idAPpkpkk"

if not os.path.exists(model_path):
    url = f"https://drive.google.com/uc?id={gdrive_id}"
    gdown.download(url, model_path, quiet=False)

st.set_page_config(page_title="Mengenal Uang Rupiah", layout="wide")

# -------------------- CSS --------------------
st.markdown("""
<style>
    /* Font umum aplikasi */
    body {
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }

    /* Latar aplikasi */
    .stApp {
        background: url('https://www.transparenttextures.com/patterns/cubes.png');
        background-size: cover;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #00000;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(60,60,60,0.3);
        margin-top: 20px;
    }

    /* Judul sidebar — hanya ini yang rata tengah */
    .sidebar-title {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #fffff;
        margin-bottom: 10px;
    }

    /* Garis pemisah sidebar */
    .sidebar-line {
        border-top: 1px solid #ddd;
        margin: 10px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">📋 Menu</div>', unsafe_allow_html=True)
    menu_option = st.selectbox("Pilih Mode:", ["🏠 Deteksi Uang", "ℹ️ About"], index=0)
    st.markdown('<div class="sidebar-line"></div>', unsafe_allow_html=True)

# -------------------- Load Model --------------------
@st.cache_resource
def load_money_model():
    return load_model("model_uang_emisi22.keras")

model = load_money_model()

# -------------------- Mapping --------------------
label_mapping = {
    "1 RB": "Rp1.000",
    "2 RB": "Rp2.000",
    "5 RB": "Rp5.000",
    "10 RB": "Rp10.000",
    "20 RB": "Rp20.000",
    "50 RB": "Rp50.000",
    "100 RB": "Rp100.000"
}

file_mapping = {
    "Rp1.000": "1000",
    "Rp2.000": "2000",
    "Rp5.000": "5000",
    "Rp10.000": "10000",
    "Rp20.000": "20000",
    "Rp50.000": "50000",
    "Rp100.000": "100000"
}

deskripsi_uang = {
    "Rp1.000":  """
    **Uang Kertas Rp 1.000 (Emisi 2022)**
    - **Tokoh Utama**: Tjut Meutia (Pahlawan Nasional dari Aceh)
    - **Warna Dominan**: Hijau
    - **Gambar Belakang**: Tari Tifa dari Papua
    - **Ukuran**: 121 x 65 mm
    - **Ciri Khas**: Motif khas Indonesia dengan teknologi pengaman modern
    """ ,
    "Rp2.000":"""
    **Uang Kertas Rp 2.000 (Emisi 2022)**
    - **Tokoh Utama**: Mohammad Hoesni Thamrin (Tokoh Pergerakan Nasional)
    - **Warna Dominan**: Abu-abu
    - **Gambar Belakang**: Tari Piring dari Sumatera Barat
    - **Ukuran**: 126 x 65 mm  
    - **Ciri Khas**: Desain modern dengan unsur budaya Indonesia
    """,
    "Rp5.000": """
    **Uang Kertas Rp 5.000 (Emisi 2022)**
    - **Tokoh Utama**: Dr. K.H. Idham Chalid (Tokoh Nasional)
    - **Warna Dominan**: Cokelat
    - **Gambar Belakang**: Tari Gambyong dari Jawa Tengah
    - **Ukuran**: 131 x 65 mm
    - **Ciri Khas**: Kombinasi tradisi dan modernitas
    """,
    "Rp10.000": """
    **Uang Kertas Rp 10.000 (Emisi 2022)**
    - **Tokoh Utama**: Frans Kaisiepo (Pahlawan Nasional dari Papua)
    - **Warna Dominan**: Ungu
    - **Gambar Belakang**: Tari Pakarena dari Sulawesi Selatan  
    - **Ukuran**: 136 x 65 mm
    - **Ciri Khas**: Teknologi pengaman tinggi dan desain artistik
    """,
    "Rp20.000": """
    **Uang Kertas Rp 20.000 (Emisi 2022)**
    - **Tokoh Utama**: Dr. G.S.S.J. Ratulangi (Pahlawan Nasional dari Sulawesi Utara)
    - **Warna Dominan**: Hijau
    - **Gambar Belakang**: Tari Gong dari Sunda
    - **Ukuran**: 141 x 65 mm
    - **Ciri Khas**: Menggabungkan nilai sejarah dan seni budaya
    """,
    "Rp50.000": """
    **Uang Kertas Rp 50.000 (Emisi 2022)**
    - **Tokoh Utama**: Ir. H. Djuanda Kartawidjaja (Perdana Menteri Indonesia)
    - **Warna Dominan**: Biru
    - **Gambar Belakang**: Tari Legong dari Bali
    - **Ukuran**: 146 x 65 mm
    - **Ciri Khas**: Desain elegan dengan teknologi canggih
    """,
    "Rp100.000": """
    **Uang Kertas Rp 100.000 (Emisi 2022)**
    - **Tokoh Utama**: Dr. Ir. Soekarno dan Dr. Drs. Mohammad Hatta (Proklamator RI)
    - **Warna Dominan**: Merah
    - **Gambar Belakang**: Tari Topeng Betawi dari DKI Jakarta
    - **Ukuran**: 151 x 65 mm
    - **Ciri Khas**: Denominasi tertinggi dengan fitur keamanan terlengkap
    """
}

st.set_page_config(page_title="Mengenal Uang Rupiah", layout="wide")

# -------------------- CSS --------------------
st.markdown("""
<style>
    /* Font umum aplikasi */
    body {
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }

    /* Latar aplikasi */
    .stApp {
        background: url('https://www.transparenttextures.com/patterns/cubes.png');
        background-size: cover;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #00000;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(60,60,60,0.3);
        margin-top: 20px;
    }

    /* Judul sidebar — hanya ini yang rata tengah */
    .sidebar-title {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #fffff;
        margin-bottom: 10px;
    }

    /* Garis pemisah sidebar */
    .sidebar-line {
        border-top: 1px solid #ddd;
        margin: 10px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">📋 Menu</div>', unsafe_allow_html=True)
    menu_option = st.selectbox("Pilih Mode:", ["🏠 Deteksi Uang", "ℹ️ About"], index=0)
    st.markdown('<div class="sidebar-line"></div>', unsafe_allow_html=True)

# -------------------- Halaman utama - deteksi uang --------------------
if menu_option == "🏠 Deteksi Uang":
    st.markdown("""
    <div style='text-align: center;'>
        <h1>Deteksi Nominal Uang Rupiah</h1>
        <h3>🔍 Arahkan Uang ke Kamera</h3>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.camera_input("Ambil gambar uang untuk dideteksi")

    if uploaded_file:
        img = Image.open(uploaded_file).resize((150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions)
        predicted_label = list(label_mapping.keys())[predicted_index]
        predicted_nominal = label_mapping[predicted_label]

        st.success(f"Nominal terdeteksi: {predicted_nominal}")
        st.info(deskripsi_uang[predicted_nominal])

        audio_path = f"audio/{file_mapping[predicted_nominal]}.mp3"
        if os.path.exists(audio_path):
            st.audio(audio_path)

# -------------------- Halaman About --------------------
elif menu_option == "ℹ️ About":
    st.markdown("""
    <div style='text-align: center;'>
        <h1>Edukasi Uang Kertas Rupiah</h1>
        <p>
            Aplikasi ini bertujuan untuk memperkenalkan uang kertas Rupiah kepada anak-anak melalui tampilan visual menarik dan interaktif.<br>
            Klik gambar uang di bawah untuk mendengar suara dan mengenal nominalnya.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-line"></div>', unsafe_allow_html=True)

# -------------------- Halaman utama - deteksi uang --------------------
if menu_option == "🏠 Deteksi Uang":
    st.markdown("""
    <div style='text-align: center;'>
        <h1>Deteksi Nominal Uang Rupiah</h1>
        <h3>🔍 Arahkan Uang ke Kamera</h3>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.camera_input("Ambil gambar uang untuk dideteksi")

    if uploaded_file:
        img = Image.open(uploaded_file).resize((150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions)
        predicted_label = list(label_mapping.keys())[predicted_index]
        predicted_nominal = label_mapping[predicted_label]

        st.success(f"Nominal terdeteksi: {predicted_nominal}")
        st.info(deskripsi_uang[predicted_nominal])

        audio_path = f"audio/{file_mapping[predicted_nominal]}.mp3"
        if os.path.exists(audio_path):
            st.audio(audio_path)

# -------------------- Halaman About --------------------
elif menu_option == "ℹ️ About":
    st.markdown("""
    <div style='text-align: center;'>
        <h1>Edukasi Uang Kertas Rupiah</h1>
        <p>
            Aplikasi ini bertujuan untuk memperkenalkan uang kertas Rupiah kepada anak-anak melalui tampilan visual menarik dan interaktif.<br>
            Klik gambar uang di bawah untuk mendengar suara dan mengenal nominalnya.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-line"></div>', unsafe_allow_html=True)


    # Ambil daftar nominal
    nominals = list(label_mapping.values())

    # Tentukan jumlah kolom tergantung ukuran layar
    # (Misalnya 4 di desktop, 2-3 di tablet/mobile)
    max_columns = 4  # Bisa ubah jadi 3 jika ingin lebih besar gambarnya

    # Buat loop berdasarkan jumlah kolom
    rows = [nominals[i:i+max_columns] for i in range(0, len(nominals), max_columns)]

    # Buat baris per baris
    for row in rows:
        # Tambahkan margin kiri dan kanan agar konten berada di tengah
        col_layout = [1] + [4]*len(row) + [1]  # Kolom 1 untuk margin kiri dan kanan
        cols = st.columns(col_layout)

        for i, nominal in enumerate(row):
            with cols[i+1]:  # i+1 karena kolom ke-0 adalah margin kiri
                img_path = f"img/Rp.{file_mapping[nominal]}.png"
                audio_path = f"audio/{file_mapping[nominal]}.mp3"

                if os.path.exists(img_path):
                    st.image(img_path, caption=nominal, use_column_width=True)

                if st.button(f"▶️ Putar {nominal}", key=f"play_{nominal}"):
                    if os.path.exists(audio_path):
                        st.audio(audio_path)
                    st.info(deskripsi_uang[nominal])

    st.markdown("</div>", unsafe_allow_html=True)
