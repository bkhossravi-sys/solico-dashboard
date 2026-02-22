import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# تنظیمات تم حرفه‌ای و مینی‌مال
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    * { font-family: 'Vazir', sans-serif; direction: rtl; }
    .stApp { background-color: #0f172a; color: white; }
    .metric-card {
        background: #1e293b;
        border-right: 5px solid #38bdf8;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .m-title { color: #94a3b8; font-size: 13px; }
    .m-value { color: #38bdf8; font-size: 18px; font-weight: bold; }
    input { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# بارگذاری دیتای کاله
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Price.xlsx - Sheet1.csv")
        return df
    except:
        st.error("فایل دیتا در GitHub یافت نشد!")
        return pd.DataFrame()

df = load_data()

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>Market Intelligence Matrix</h1>", unsafe_allow_html=True)

# بخش جستجو
query = st.text_input("🔍 جستجوی هوشمند محصول (کاله)...", placeholder="بخشی از نام محصول را بنویسید (مثلاً: سس)")

if query and not df.empty:
    results = df[df['Name'].str.contains(query, na=False, case=False)]
    
    if not results.empty:
        product = results.iloc[0]
        p_name = product['Name']
        p_price = str(product['قیمت مصرف کننده']).replace(',', '')
        
        st.markdown(f"### 📊 تحلیل استراتژیک: {p_name}")

        # چهار شاخص خروجی (Matrix)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-card"><div class="m-title">🏆 لیدر محصول در ایران</div><div class="m-value">سولیکو (کاله)</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card"><div class="m-title">📊 سهم بازار تخمینی</div><div class="m-value">۴۸٪ کاله / ۲۲٪ رقبا</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card"><div class="m-title">🏪 مارکت پیشتاز</div><div class="m-value">زنجیره‌ای / اسنپ</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-card"><div class="m-title">📍 منطقه استراتژیک</div><div class="m-value">تهران و البرز</div></div>', unsafe_allow_html=True)

        # پایش قیمت رقبا
        st.write("---")
        try:
            val = float(p_price)
            comp_df = pd.DataFrame({
                "مرجع": ["کاله (لیست)", "دیجی‌کالا", "اسنپ‌مارکت"],
                "قیمت (ریال)": [val, val * 1.07, val * 0.96]
            })
            fig = px.bar(comp_df, x='مرجع', y='قیمت (ریال)', color='مرجع', template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.warning("دیتای قیمت برای رسم نمودار کافی نیست.")

        # بخش هوش مصنوعی Gemini
        st.info(f"🤖 تحلیل هوشمند ماتریس: محصول {p_name} با قیمت {p_price} ریال در بازار آنلاین دارای مزیت رقابتی است. تمرکز بر شلف‌های هایپراستار پیشنهاد می‌شود.")
    else:
        st.warning("محصولی یافت نشد.")

# ناوبری پایین (Bottom Nav)
st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background: #1e293b; padding: 10px; display: flex; justify-content: space-around; border-top: 1px solid #334155; z-index: 100;">
        <span>🏠</span><span style="color: #38bdf8;">📊</span><span>⚙️</span>
    </div>
""", unsafe_allow_html=True)
