import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# ⚙️ Налаштування сторінки
# -----------------------------
st.set_page_config(page_title="Система оцінки ризику підприємств", layout="wide")
st.title("📊 Система оцінки ризику підприємств")

# -----------------------------
# 📂 Завантаження CSV або приклад
# -----------------------------
uploaded_file = st.file_uploader("⬆️ Завантажте CSV-файл з даними компаній", type=["csv"])

if uploaded_file is None:
    st.info("Не завантажено файл — використовується приклад.")
    data = {
        "company": ["A_Corp", "B_Ltd", "C_Group", "D_Holdings"],
        "financial_score": [0.8, 0.4, 0.3, 0.9],
        "tax_score": [0.6, 0.7, 0.2, 0.9],
        "public_reputation": [0.9, 0.5, 0.4, 0.8],
    }
    df = pd.DataFrame(data)
else:
    df = pd.read_csv(uploaded_file)

# -----------------------------
# 🧮 Обчислення інтегрального індексу ризику
# -----------------------------
weights = {
    "financial_score": 0.5,
    "tax_score": 0.3,
    "public_reputation": 0.2
}

for col in weights.keys():
    df[col] = df[col].clip(0, 1)

df["risk_index"] = (
    df["financial_score"] * weights["financial_score"] +
    df["tax_score"] * weights["tax_score"] +
    df["public_reputation"] * weights["public_reputation"]
)

df["risk_level"] = 1 - df["risk_index"]

df["risk_category"] = pd.cut(
    df["risk_level"],
    bins=[0, 0.33, 0.66, 1],
    labels=["Низький", "Середній", "Високий"]
)

# -----------------------------
# 📋 Таблиця з підсвічуванням
# -----------------------------
st.subheader("📋 Оцінка ризику компаній")

def highlight_risk(row):
    if row["risk_category"] == "Високий":
        color = "background-color: #f8d7da;"  # червоний
    elif row["risk_category"] == "Середній":
        color = "background-color: #fff3cd;"  # жовтий
    else:
        color = "background-color: #d4edda;"  # зелений
    return [color] * len(row)

st.dataframe(df.style.apply(highlight_risk, axis=1), use_container_width=True)

# -----------------------------
# 🎯 Візуалізація gauge-chart
# -----------------------------
st.subheader("🎯 Візуалізація рівня ризику")

company_choice = st.selectbox("Оберіть компанію:", df["company"])
selected = df[df["company"] == company_choice].iloc[0]
risk_value = selected["risk_level"]

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=risk_value * 100,
    title={'text': f"Рівень ризику: {company_choice}"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "darkred" if risk_value > 0.66 else "orange" if risk_value > 0.33 else "green"},
        'steps': [
            {'range': [0, 33], 'color': "lightgreen"},
            {'range': [33, 66], 'color': "yellow"},
            {'range': [66, 100], 'color': "salmon"}
        ],
    }
))

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# ⚠️ Високоризикові компанії
# -----------------------------
high_risk = df[df["risk_category"] == "Високий"]

if not high_risk.empty:
    st.warning("⚠️ Компанії з високим рівнем ризику:")
    st.write(", ".join(high_risk["company"]))
else:
    st.success("✅ Усі компанії мають прийнятний рівень ризику.")
