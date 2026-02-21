import streamlit as st
import google.generativeai as genai
import os
import re
import requests
from datetime import datetime

# =========================
# تنظیمات اولیه
# =========================

st.set_page_config(page_title="Solico AI Market Analyzer", layout="wide")

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")

# =========================
# نرمال‌سازی ورودی
# =========================

def normalize_product(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

# =========================
# قیمت رقبا (نسخه MVP)
# بعداً میشه واقعی کرد
# =========================

def get_prices(product):

    # فعلاً شبیه‌سازی شده
    dummy_prices = [
        {"store": "Digikala", "price": "3,200,000"},
        {"store": "SnappMarket", "price": "3,350,000"},
        {"store": "Hyperstar Online", "price": "3,150,000"},
    ]

    return dummy_prices

# =========================
# تحلیل شبکه اجتماعی (MVP)
# =========================

def analyze_social(product):

    return {
        "top_brand": "کاله",
        "mention_volume": 1820,
        "sentiment": "مثبت",
        "top_city": "تهران"
    }

# =========================
# تحلیل AI حرفه‌ای
# =========================

def analyze_market(product, prices, social_data):

    if not GEMINI_API_KEY:
        return "⚠️ Gemini API Key تنظیم نشده است."

    prompt = f"""
    شما یک تحلیلگر حرفه‌ای بازار FMCG هستید.

    محصول: {product}

    قیمت رقبا:
    {prices}

    داده شبکه اجتماعی:
    {social_data}

    تحلیل کامل بده شامل:

    1- لیدر بازار کیست
    2- محبوب‌ترین برند
    3- تحلیل قیمت (ارزان‌ترین / گران‌ترین)
    4- تحلیل جغرافیایی
    5- پیشنهاد استراتژی فروش
    6- پیشنهاد پروموشن
    """

    response = model.generate_content(prompt)
    return response.text

# =========================
# UI
# =========================

st.title("📊 Solico AI Market Intelligence")
st.caption("تحلیل حرفه‌ای بازار سس، سوسیس، تن ماهی و ...")

product_input = st.text_input("🔍 نام کالا را وارد کنید (مثال: مایونز ۹۰۰ یا تون ماهی)")

if product_input:

    product = normalize_product(product_input)

    with st.spinner("در حال تحلیل بازار..."):

        prices = get_prices(product)
        social_data = analyze_social(product)
        analysis = analyze_market(product, prices, social_data)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 قیمت رقبا")
        st.table(prices)

    with col2:
        st.subheader("📱 تحلیل شبکه اجتماعی")
        st.json(social_data)

    st.subheader("🤖 تحلیل هوشمند بازار")
    st.write(analysis)

    st.caption(f"آخرین بروزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
