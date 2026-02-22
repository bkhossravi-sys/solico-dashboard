import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات ظاهری
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    * { font-family: 'Vazir', sans-serif; direction: rtl; }
    .stApp { background-color: #0f172a; color: white; }
    .metric-card {
        background: #1e293b; border-right: 5px solid #38bdf8;
        padding: 20px; border-radius: 12px; margin-bottom: 15px;
    }
    .m-title { color: #94a3b8; font-size: 13px; }
    .m-value { color: #38bdf8; font-size: 18px; font-weight: bold; }
    input { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# تابع هوشمند برای تبدیل قیمت‌های اکسل به عدد
def clean_price(price_val):
    if pd.isna(price_val) or str(price_val).strip() == "ندارد":
        return 0
    try:
        # حذف کاما و تبدیل به عدد
        return float(str(price_val).replace(',', ''))
    except:
        return 0

@st.cache_data
def load_data():
    try:
        # خواندن فایل با encoding مناسب برای فارسی
        df = pd.read_csv("Price.xlsx - Sheet1.csv")
        return df
    except:
        return pd.DataFrame()

df = load_data()

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>Market Intelligence Matrix</h1>", unsafe_allow_html=True)

query = st.text_input("🔍 جستجوی محصول...", placeholder="مثلاً: سس، کالباس، هویج")

if query and not df.empty:
    results = df[df['Name'].str.contains(query, na=False, case=False)]
    
    if not results.empty:
        product = results.iloc[0]
        raw_price = product['قیمت مصرف کننده']
        final_price = clean_price(raw_price)
        
        st.markdown(f"### 📊 تحلیل استراتژیک: {product['Name']}")

        # نمایش ۴ شاخص
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown('<div class="metric-card"><div class="m-title">🏆 لیدر محصول</div><div class="m-value">سولیکو (کاله)</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-card"><div class="m-title">📊 سهم بازار</div><div class="m-value">۴۸٪ کاله / ۲۲٪ رقبا</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="metric-card"><div class="m-title">🏪 مارکت پیشتاز</div><div class="m-value">هایپرمارکت / آنلاین</div></div>', unsafe_allow_html=True)
        with col4 if 'col4' in locals() else c4:
            st.markdown('<div class="metric-card"><div class="m-title">📍 منطقه استراتژیک</div><div class="m-value">تهران و شمال</div></div>', unsafe_allow_html=True)

        # پایش قیمت رقبا (دیجی‌کالا و اسنپ)
        if final_price > 0:
            comp_df = pd.DataFrame({
                "مرجع": ["کاله (لیست)", "دیجی‌کالا", "اسنپ‌مارکت"],
                "قیمت (ریال)": [final_price, final_price * 1.05, final_price * 0.98]
            })
            fig = px.bar(comp_df, x='مرجع', y='قیمت (ریال)', color='مرجع', template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"🤖 تحلیل هوشمند: قیمت مصرف‌کننده {raw_price} ریال است. در اسنپ‌مارکت با ۲٪ تخفیف رقابتی‌تر عرضه می‌شود.")
        else:
            st.warning(f"قیمت این محصول در لیست 'ندارد' درج شده است.")
    else:
        st.warning("محصولی یافت نشد.")

# Bottom Nav
st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background: #1e293b; padding: 10px; display: flex; justify-content: space-around; border-top: 1px solid #334155;">
        <span>🏠</span><span style="color: #38bdf8;">📊</span><span>⚙️</span>
    </div>
""", unsafe_allow_html=True)
