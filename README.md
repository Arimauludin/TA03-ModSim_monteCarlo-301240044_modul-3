# TA03-ModSim_monteCarlo-301240044_modul-3
# Data-Driven Monte Carlo Simulation: Estimasi Risiko Klaim Asuransi

Repositori ini berisi proyek Tugas Akhir 03 (TA-03) untuk mata praktikum **Pemodelan dan Simulasi**. Proyek ini mengimplementasikan simulasi Monte Carlo berbasis data historis (*Medical Cost Personal Datasets*) untuk memprediksi risiko bengkaknya total klaim medis dari 100 pasien baru terhadap batas anggaran perusahaan asuransi.

---

## 👨‍💻 Identitas Mahasiswa

* **Nama:** Ari Mauludin
* **NIM:** 301240044 (Seed: `301240044`)
* **Kelas:** 5C (Teknik Informatika)
* **Program Studi:** S1 Teknik Informatika
* **Instansi:** Universitas Bale Bandung (UNIBBA)
* **Dosen Pengampu:** Mohammad Bayu Anggara, S.Kom., M.Kom.

---

## 📊 Ringkasan Hasil Simulasi

Berdasarkan penarikan 10.000 skenario eksperimen dengan random seed `301240044`:

| Parameter / Ukuran | Nilai / Hasil |
| :--- | :--- |
| **Jumlah Pasien Baru** | 100 Pasien |
| **Batas Anggaran (Buffer 10%)** | $1.457.797,00 |
| **Ekspektasi Total Klaim** | $1.325.270,00 |
| **Probabilitas Risiko ($P > \text{Anggaran}$)** | **23,84%** (2.384 dari 10.000 skenario) |
| **Interval Kepercayaan 95% Galat** | [0,2300, 0,2468] |
| **Value at Risk (VaR 95%)** | $1.524.230,00 |

---

## 🧪 Uji Sensitivitas Model

| Model Distribusi | Rata-rata Total Klaim | Probabilitas Risiko ($P > \text{Anggaran}$) |
| :--- | :--- | :--- |
| **Normal (Utama)** | $1.325.270,00 | **23,84%** |
| **Normal + Clip 0** | $1.335.800,00 | **26,80%** |
| **Lognormal** | $1.324.950,00 | **23,75%** |
| **Bootstrap Historis** | $1.325.100,00 | **23,90%** |

---

## 📁 Struktur Repositori

* `app.py` : Kode utama aplikasi interaktif berbasis Streamlit.
* `TA03_ModSim_301240044_Ari_Mauludin.ipynb` : Jupyter Notebook pemodelan dan simulasi Monte Carlo.
* `requirements.txt` : Daftar pustaka/library Python untuk deployment.
* `insurance.csv` / `insurance-metadata.json` : Dataset klaim biaya medis dari Kaggle.
* `README.md` : Dokumentasi repositori proyek.

---

## 🚀 Cara Menjalankan Aplikasi Secara Lokal

1. Clone repositori ini:
   ```bash
   git clone [https://github.com/Arimauludin/TA03-ModSim_monteCarlo-301240044_modul-3.git](https://github.com/Arimauludin/TA03-ModSim_monteCarlo-301240044_modul-3.git)
   cd TA03-ModSim_monteCarlo-301240044_modul-3
