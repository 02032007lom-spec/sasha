import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# ⚙️ Налаштування сторінки
# -----------------------------
st.set_page_config(page_title="Система оцінки ризику підприємств", layout="wide")
st.title("📊 Система оцінки ризику підприємств")

# -----------------------------
# 📂 Автоматичне завантаження CSV
# -----------------------------
CSV_PATH = "companies.csv"

try:
    df = pd.read_csv(CSV_PATH)
    st.success(f"✅ Автоматично завантажено дані з '{CSV_PATH}'")
except FileNotFoundError:
    st.warning("⚠️ Файл не знайдено — створено прикладові дані.")
    df = pd.DataFrame({
        "company": ["A_Corp", "B_Ltd", "C_Group", "D_Holdings"],
        "financial_score": [0.8, 0.4, 0.3, 0.9],
        "tax_score": [0.6, 0.7, 0.2, 0.9],
        "public_reputation": [0.9, 0.5, 0.4, 0.8],
    })
    df.to_csv(CSV_PATH, index=False)
    st.info("💾 Збережено прикладовий файл 'companies.csv'")

# -----------------------------
# 🧮 Обчислення інтегрального індексу ризику
# -----------------------------
weights = np.array([0.5, 0.3, 0.2])
scores = df[["financial_score", "tax_score", "public_reputation"]].clip(0, 1).to_numpy()

# інтегральний індекс
df["risk_index"] = np.dot(scores, weights)

# рівень ризику (1 - індекс)
df["risk_level"] = 1 - df["risk_index"]

# категорії ризику
bins = [0, 0.33, 0.66, 1.0]
labels = ["Низький", "Середній", "Високий"]
df["risk_category"] = pd.cut(df["risk_level"], bins=bins, labels=labels)

# -----------------------------
# 📋 Таблиця з підсвічуванням
# -----------------------------
st.subheader("📋 Оцінка ризику компаній")

def highlight_risk(row):
    color = ""
    if row["risk_category"] == "Високий":
        color = "background-color: #f8d7da;"  # червоний
    elif row["risk_category"] == "Середній":
        color = "background-color: #fff3cd;"  # жовтий
    else:
        color = "background-color: #d4edda;"  # зелений
    return [color] * len(row)

st.dataframe(df.style.apply(highlight_risk, axis=1), use_container_width=True)

# -----------------------------
# 📊 Просте графічне відображення ризику
# -----------------------------
st.subheader("📈 Візуалізація ризику")

company_choice = st.selectbox("Оберіть компанію:", df["company"])
selected = df[df["company"] == company_choice].iloc[0]

risk_value = selected["risk_level"]
bar_length = int(risk_value * 50)  # шкала 0–50

bar = "🟩" * (50 - bar_length) + "🟥" * bar_length
st.markdown(f"**{company_choice} — ризик {risk_value:.2f} ({selected['risk_category']})**")
st.text(bar)

# -----------------------------
# ⚠️ Високоризикові компанії
# -----------------------------
high_risk = df[df["risk_category"] == "Високий"]
if not high_risk.empty:
    st.warning("⚠️ Компанії з високим рівнем ризику:")
    st.write(", ".join(high_risk["company"]))
else:
    st.success("✅ Усі компанії мають прийнятний рівень ризику.")
