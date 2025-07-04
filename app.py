import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------- Helper functions ----------
def savings_rate(savings, income):
    return savings / income if income else 0

def expense_rate(expenses, income):
    return expenses / income if income else 0

def debt_service_ratio(debt_payment, income):
    return debt_payment / income if income else 0

def emergency_months(savings, monthly_expenses):
    return savings / monthly_expenses if monthly_expenses else 0

def color_text(text, condition):
    """Return colored markdown text based on condition tuple (low, medium, high)."""
    low, medium, high = condition
    if text < low:
        color = "red"
    elif text < medium:
        color = "orange"
    else:
        color = "green"
    return f":{color}[{text:.1%}]"

# ---------- Streamlit UI ----------
st.set_page_config(page_title="FinCheck – Analisis Kesehatan Keuangan", page_icon="💰")
st.title("💰 FinCheck – Analisis Kesehatan Keuangan Pribadi")
st.write(
    """
Masukkan angka bulanan kamu di bawah ini.  
FinCheck akan menghitung **rasio tabungan, rasio pengeluaran, rasio cicilan**, dan
berapa bulan **dana darurat** yang sudah tersedia, lalu memberi saran cepat.
""")

with st.form("fin_form"):
    col1, col2 = st.columns(2)
    income        = col1.number_input("Pendapatan (Rp)", min_value=0.0, step=100_000.0)
    savings_input = col1.number_input("Tabungan/Berinvestasi bulan ini (Rp)", min_value=0.0, step=100_000.0)
    expenses      = col2.number_input("Total Pengeluaran (Rp)", min_value=0.0, step=100_000.0)
    debt_payment  = col2.number_input("Pembayaran Cicilan/Bunga (Rp)", min_value=0.0, step=100_000.0)
    submitted = st.form_submit_button("💡 Analisis")

if submitted:
    st.subheader("📊 Hasil Analisis")

    # --- Hitung metrik utama ---
    save_rate  = savings_rate(savings_input, income)
    exp_rate   = expense_rate(expenses, income)
    debt_ratio = debt_service_ratio(debt_payment, income)
    ef_months  = emergency_months(savings_input, expenses)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rasio Tabungan", f"{save_rate:.1%}",
                help="Ideal ≥ 20% (aturan 50/30/20)")
    col2.metric("Rasio Pengeluaran", f"{exp_rate:.1%}",
                help="Ideal ≤ 70% dari pendapatan")
    col3.metric("Rasio Cicilan", f"{debt_ratio:.1%}",
                help="Ideal ≤ 30% dari pendapatan")
    col4.metric("Dana Darurat (bulan)", f"{ef_months:.1f}",
                help="Ideal ≥ 3 (blended) atau ≥ 6 (aman)")

    # --- Grafik sederhana ---
    fig, ax = plt.subplots()
    labels = ["Tabungan", "Pengeluaran", "Cicilan"]
    values = [save_rate, exp_rate, debt_ratio]
    ax.bar(labels, values)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Persentase pendapatan")
    ax.set_title("Distribusi Pendapatan Bulanan")
    ax.bar_label(ax.containers[0], fmt="%.0f%%")
    st.pyplot(fig)

    # --- Saran cepat ---
    st.subheader("📝 Rekomendasi & Insight")

    # Tabungan
    if save_rate < 0.1:
        st.warning("• Tingkat tabungan kamu rendah. Coba alokasikan minimal 10–20 % pendapatan untuk tabungan/investasi.")
    elif save_rate < 0.2:
        st.info("• Tabungan sudah lumayan, tapi tingkatkan ke ≥ 20 % agar lebih aman.")
    else:
        st.success("• Tabungan ideal! Pertahankan kebiasaan baik ini.")

    # Pengeluaran
    if exp_rate > 0.7:
        st.warning("• Pengeluaran cukup besar. Pertimbangkan memotong biaya non‑esensial.")
    else:
        st.success("• Pengeluaran masih dalam batas sehat.")

    # Cicilan
    if debt_ratio > 0.4:
        st.error("• Beban cicilan tinggi. Usahakan melunasi atau restrukturisasi utang.")
    elif debt_ratio > 0.3:
        st.warning("• Cicilan mendekati batas aman (30 %). Hati‑hati menambah utang baru.")
    else:
        st.success("• Cicilan dalam batas aman.")

    # Dana darurat
    if ef_months < 3:
        st.warning(f"• Dana darurat hanya cukup {ef_months:.1f} bulan. Targetkan minimal 3–6 bulan.")
    else:
        st.success("• Dana darurat memadai. Bagus!")

    st.caption("FinCheck memberikan rekomendasi bersifat edukatif, bukan nasihat keuangan profesional.")