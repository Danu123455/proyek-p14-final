import streamlit as st
import numpy as np
import pandas as pd
import joblib

# ======================================
# Langkah 1: Load Model yang Sudah Dilatih
# ======================================
model = joblib.load("model_toko.pkl")

# ======================================
# Baseline (Kondisi Saat Ini)
# ======================================
baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]

# ======================================
# Fungsi Simulasi What-If
# ======================================
def run_simulation(new_iklan, new_diskon):

    # Input baru dari user
    intervention_input = np.array([[new_iklan, new_diskon]])

    # Prediksi hasil
    prediction = model.predict(intervention_input)[0]

    # Hitung perubahan terhadap baseline
    delta_y = prediction - baseline_pred

    return prediction, delta_y


# ======================================
# Tampilan Streamlit
# ======================================
st.title("🚀🚀 Simulator Kebijakan Keuntungan Toko")
st.header("Analisis Skenario What-If")
st.write("Gunakan slider untuk menguji skenario 'What-If'.")

# ======================================
# Sidebar
# ======================================
st.sidebar.header("Tuas Kebijakan (Intervensi)")

iklan_slider = st.sidebar.slider(
    "Anggaran Iklan (Juta)",
    min_value=0,
    max_value=50,
    value=10
)

diskon_slider = st.sidebar.slider(
    "Besaran Diskon (%)",
    min_value=0,
    max_value=50,
    value=10
)

# ======================================
# Pilihan Tema
# ======================================
tema = st.sidebar.selectbox(
    "🎨 Pilih Tema",
    ["❄️ Ice Mode", "🌿 Earth Mode"]
)

if tema == "❄️ Ice Mode":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #E0F7FF, #BFEFFF, #FFFFFF);
        color: #003366;
    }
    </style>
    """, unsafe_allow_html=True)

elif tema == "🌿 Earth Mode":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #F5FFF5, #D8F3DC, #FFFFFF);
        color: #1B4332;
    }
    </style>
    """, unsafe_allow_html=True)

# ======================================
# Jalankan Simulasi
# ======================================
hasil_pred, delta = run_simulation(
    iklan_slider,
    diskon_slider
)

# ======================================
# Tampilkan Hasil
# ======================================
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Prediksi Keuntungan",
        value=f"Rp {hasil_pred:.2f} Jt",
        delta=f"{delta:.2f} Jt"
    )

with col2:
    st.write(
        f"Skenario ini menghasilkan perubahan sebesar "
        f"{delta:.2f} juta dibanding kondisi baseline."
    )

# ======================================
# Analisis Hasil Simulasi
# ======================================
st.subheader("Analisis Hasil Simulasi")

if delta > 0:
    st.success(
        f"Intervensi menghasilkan peningkatan keuntungan sebesar Rp {delta:.2f} juta dibanding kondisi baseline."
    )

elif delta < 0:
    st.warning(
        f"Intervensi menghasilkan penurunan keuntungan sebesar Rp {abs(delta):.2f} juta dibanding kondisi baseline sehingga skenario ini kurang menguntungkan dibanding kondisi saat ini."
    )

else:
    st.info(
        "Intervensi tidak memberikan perubahan terhadap kondisi baseline."
    )

# ======================================
# Data Visualisasi
# ======================================
data_plot = pd.DataFrame({
    "Skenario": ["Baseline", "Intervensi"],
    "Keuntungan": [baseline_pred, hasil_pred]
})

# ======================================
# Grafik Perbandingan / memvisualisasikan data
# ======================================
st.subheader("Perbandingan Baseline vs Intervensi")
st.bar_chart(
    data=data_plot,
    x="Skenario",
    y="Keuntungan"
)