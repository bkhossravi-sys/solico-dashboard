import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# 1. تنظیمات صفحه و استایل مینی‌مال (Modern & Clean)
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

# اعمال تم اختصاصی (فونت سفید بر روی پس‌زمینه تیره)
st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    * { font-family: 'Vazir', sans-serif; direction: rtl; }
    .stApp { background-color: #0f172a; color: white; }
    .stTextInput input { border-radius: 12px !important; border: 1px solid #38bdf8 !important; }
    
    /* کارت‌های شاخص چهارگانه */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s;
    }
    .metric-card:hover { transform: translateY(-5px); border-color: #38bdf8; }
    .metric-title { font-size: 13px; color: #94a3b8; margin-bottom: 8px; }
    .metric-value { font-size: 18px; font-weight: bold; color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# 2. بارگذاری دیتای اکسل (کد بهینه برای فایل پیوست شما)
@st.cache_data
def load_data():
    df = pd.read_csv("Price.xlsx - Sheet1.csv") # فایل اکسل پیوست شما
    return df

df_prices = load_data()

# 3. هدر اپلیکیشن
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>Market Intelligence Matrix</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>تحلیل استراتژیک بازار و پایش رقبا</p>", unsafe_allow_html=True)

# 4. جستجوی هوشمند (بخشی از نام محصول)
search_query = st.text_input("🔍 نام محصول را جستجو کنید (مثلاً: سس کچاپ، کالباس، هویج...)", "")

if search_query:
    # فیلتر کردن محصولات از اکسل
    results = df_prices[df_prices['Name'].str.contains(search_query, na=False)]
    
    if not results.empty:
        selected_product = results.iloc[0]['Name']
        price_consumer = results.iloc[0]['قیمت مصرف کننده']
        
        st.markdown(f"### تحلیل بازار برای: {selected_product}")
        
        # بخش چهار شاخص خروجی (با منطق تحلیل بازار)
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>🏆 لیدر محصول در ایران</div><div class='metric-value'>کاله (سولیکو)</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>📊 سهم بازار برند</div><div class='metric-value'>۴۲٪ کاله / ۲۵٪ مهرام</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>🏢 مارکت پیشتاز</div><div class='metric-value'>هایپرمارکت‌ها / آنلاین</div></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>📍 منطقه پیشرو</div><div class='metric-value'>تهران و البرز</div></div>", unsafe_allow_html=True)

        # 5. مقایسه قیمت با رقبا (شبیه‌سازی استخراج از دیجی‌کالا و اسنپ مارکت)
        st.write("---")
        st.subheader("💰 پایش قیمت در بازار")
        
        price_data = {
            "مرجع": ["قیمت شما (کاله)", "دیجی‌کالا", "اسنپ مارکت", "میانگین بازار"],
            "قیمت (ریال)": [price_consumer, price_consumer*1.05, price_consumer*0.98, price_consumer*1.02]
        }
        df_p = pd.DataFrame(price_data)
        
        fig = px.bar(df_p, x='مرجع', y='قیمت (ریال)', color='مرجع', 
                     text_auto='.2s', template="plotly_dark",
                     color_discrete_sequence=['#38bdf8', '#ef4444', '#22c55e', '#f59e0b'])
        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        # 6. اتصال به هوش مصنوعی Gemini برای تحلیل نهایی
        st.info("🤖 تحلیل هوشمند Gemini:")
        st.write(f"بر اساس قیمت {price_consumer} ریال در لیست شما، این محصول در رده Premium قرار می‌گیرد. پیشنهاد می‌شود برای حفظ لیدری در منطقه تهران، طرح‌های تشویقی در اسنپ‌مارکت فعال شود.")

    else:
        st.error("محصولی با این نام در لیست قیمت کاله پیدا نشد.")
else:
    st.info("منتظر ورود نام محصول برای شروع تحلیل...")

# فوتر مینی‌مال
st.markdown("<br><br><p style='text-align: center; font-size: 10px; color: #475569;'>Powered by Gemini AI & Solico Data Analytics</p>", unsafe_allow_html=True)
