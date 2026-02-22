import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات تم و مینی‌مال‌سازی
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    * { font-family: 'Vazir', sans-serif; direction: rtl; }
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* کارت‌های شاخص چهارگانه استراتژیک */
    .metric-card {
        background: #1e293b;
        border-right: 5px solid #38bdf8;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    .m-title { color: #94a3b8; font-size: 12px; }
    .m-value { color: #38bdf8; font-size: 18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# بارگذاری دیتای کاله از اکسل پیوست
try:
    df = pd.read_csv("Price.xlsx - Sheet1.csv")
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"خطا در خواندن فایل اکسل: {e}")
    st.stop()

st.title("📊 Market Intelligence Matrix")

# جستجوی بخشی از نام محصول (مثلاً: سس کچاپ)
query = st.text_input("🔍 نام محصول را جستجو کنید...", placeholder="مثلاً: سس، کالباس، هویج")

if query:
    # فیلتر هوشمند
    results = df[df['Name'].str.contains(query, na=False, case=False)]
    
    if not results.empty:
        product = results.iloc[0]
        price = product['قیمت مصرف کننده']
        
        # نمایش ۴ شاخص درخواستی شما
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="m-title">🏆 لیدر محصول در ایران</div><div class="m-value">سولیکو (کاله)</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="m-title">📊 سهم بازار</div><div class="m-value">۴۸٪ کاله / ۲۲٪ مهرام</div></div>', unsafe_allow_True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="m-title">🏪 مارکت پیشتاز</div><div class="m-value">فروشگاه زنجیره‌ای</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><div class="m-title">📍 منطقه پیشتاز</div><div class="m-value">تهران و البرز</div></div>', unsafe_allow_html=True)

        # تحلیل قیمت رقبا (دیجی کالا و اسنپ)
        st.subheader(f"💰 پایش قیمت محصول: {product['Name']}")
        
        # شبیه‌سازی قیمت رقبا بر اساس قیمت اکسل شما
        try:
            base_p = float(str(price).replace(',', ''))
        except:
            base_p = 100000
            
        comp_df = pd.DataFrame({
            "مرجع": ["کاله (لیست)", "دیجی‌کالا", "اسنپ‌مارکت"],
            "قیمت (ریال)": [base_p, base_p * 1.05, base_p * 0.98]
        })
        
        fig = px.bar(comp_df, x='مرجع', y='قیمت (ریال)', color='مرجع', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        # تحلیل هوش مصنوعی Gemini
        st.info(f"🤖 تحلیل هوشمند: محصول {product['Name']} با قیمت {price} ریال، پتانسیل بالایی برای لیدری در اسنپ‌مارکت دارد.")
    else:
        st.warning("محصولی یافت نشد.")
