"""TA-03 Pemodelan & Simulasi - Monte Carlo Risiko Klaim Asuransi
Ari Mauludin | NIM 301240044 | Kelas 5C
Jalankan lokal : streamlit run app.py
Dataset        : insurance.csv (Kaggle: Medical Cost Personal Datasets)
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Monte Carlo Risiko Klaim Asuransi", layout="wide")
st.title("Simulasi Monte Carlo: Risiko Klaim Asuransi")
st.caption("TA-03 Pemodelan dan Simulasi | Ari Mauludin | NIM 301240044 | Kelas 5C")


@st.cache_data
def load_data(file):
    return pd.read_csv(file)


# ---------- Sidebar ----------
st.sidebar.header("Data")
upload = st.sidebar.file_uploader("Upload insurance.csv", type="csv")
if upload is not None:
    df = load_data(upload)
elif os.path.exists("insurance.csv"):
    df = load_data("insurance.csv")
else:
    st.info("Upload file insurance.csv (Kaggle: Medical Cost Personal Datasets) di sidebar untuk memulai.")
    st.stop()

if "charges" not in df.columns:
    st.error("Kolom 'charges' tidak ditemukan pada file.")
    st.stop()

st.sidebar.header("Parameter simulasi")
n_patients = st.sidebar.number_input("Jumlah pasien baru", 10, 1000, 100, step=10)
n_scen = st.sidebar.number_input("Jumlah skenario", 5000, 100000, 10000, step=5000)
buffer_pct = st.sidebar.slider("Buffer anggaran di atas ekspektasi (%)", 0, 50, 10)
dist = st.sidebar.selectbox("Distribusi klaim", ["Normal", "Lognormal", "Bootstrap (data historis)"])
seed = st.sidebar.number_input("Seed", value=301240044, step=1)

# ---------- Cleaning & parameter ----------
df = df.dropna().drop_duplicates()
q1, q3 = df["charges"].quantile([0.25, 0.75])
iqr = q3 - q1
clean = df[(df["charges"] >= q1 - 3 * iqr) & (df["charges"] <= q3 + 3 * iqr)]
ch = clean["charges"]
mu, sigma = ch.mean(), ch.std(ddof=1)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Baris data bersih", f"{len(clean):,}")
c2.metric("Mean (μ)", f"{mu:,.0f}")
c3.metric("Std Dev (σ)", f"{sigma:,.0f}")
c4.metric("Outlier ekstrem dibuang", f"{len(df) - len(clean)}")

with st.expander("Histogram data asli"):
    fig0, ax0 = plt.subplots(figsize=(7, 3.5))
    ax0.hist(ch, bins=40, color="steelblue", alpha=0.8)
    ax0.set_xlabel("charges"); ax0.set_ylabel("Frekuensi")
    st.pyplot(fig0)

# ---------- Simulasi ----------
rng = np.random.default_rng(int(seed))
shape = (int(n_scen), int(n_patients))
if dist == "Normal":
    sims = rng.normal(mu, sigma, shape)
elif dist == "Lognormal":
    lc = np.log(ch)
    sims = rng.lognormal(lc.mean(), lc.std(ddof=1), shape)
else:
    sims = rng.choice(ch.values, size=shape, replace=True)
total = sims.sum(axis=1)

budget = (1 + buffer_pct / 100) * n_patients * mu
prob = float(np.mean(total > budget))
se = np.sqrt(prob * (1 - prob) / n_scen)

st.subheader("Hasil analisis risiko")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Anggaran", f"{budget:,.0f}")
m2.metric("P(total klaim > anggaran)", f"{prob:.2%}")
m3.metric("Rata-rata total klaim", f"{total.mean():,.0f}")
m4.metric("VaR 95%", f"{np.percentile(total, 95):,.0f}")
st.write(f"Interval 95% galat Monte Carlo: {prob - 1.96 * se:.2%} sampai {prob + 1.96 * se:.2%}")

fig, ax = plt.subplots(figsize=(9, 4.5))
_, bins, patches = ax.hist(total, bins=60, color="steelblue", alpha=0.85)
for b, p in zip(bins[:-1], patches):
    if b >= budget:
        p.set_facecolor("crimson")
ax.axvline(budget, color="black", ls="--", lw=2, label=f"Anggaran = {budget:,.0f}")
ax.axvline(total.mean(), color="green", ls=":", lw=2, label=f"Rata-rata = {total.mean():,.0f}")
ax.set_title(f"Distribusi total klaim {n_patients} pasien ({n_scen:,} skenario, {dist})")
ax.set_xlabel("Total klaim"); ax.set_ylabel("Jumlah skenario"); ax.legend()
st.pyplot(fig)

st.markdown(
    f"**Kesimpulan:** dari {n_scen:,} skenario, total klaim {n_patients} pasien baru melebihi anggaran "
    f"sebesar {budget:,.0f} dengan probabilitas **{prob:.2%}**."
)
if dist == "Normal":
    st.caption("Catatan: model Normal tidak di-clip di 0 karena pemotongan membuat rata-rata simulasi bias ke atas.")
