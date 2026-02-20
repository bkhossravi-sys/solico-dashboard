import streamlit as st
import pandas as pd
import plotly.express as px

# 1. تنظیمات ظاهری برای حل مشکل فونت و رنگ
st.set_page_config(page_title="Market Leader Dashboard", layout="wide")

st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    * { font-family: 'Vazir', sans-serif; direction: rtl; }
    .stApp { background-color: #0e1117; } /* پس‌زمینه تیره */
    
    /* اصلاح رنگ فونت‌ها برای دیده شدن در تم تیره */
    h1, h2, h3, p, span, label { color: #e2e8f0 !important; }
    
    /* کارت‌های شاخص حرفه‌ای */
    .leader-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 5px solid #38bdf8;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    .leader-title { color: #38bdf8; font-size: 14px; margin-bottom: 10px; }
    .leader-name { font-size: 24px; font-weight: bold; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. دیتای محصول (سس مایونز به عنوان نمونه)
data = {
    "برند": ["کاله", "مهرام", "بیژن", "بهروز", "تبرک"],
    "سهم_بازار": [38, 28, 15, 12, 7],
    "محبوبیت_مجازی": [85000, 62000, 41000, 30000, 12000], # فالوور/تعامل
    "شهر_پیشرو": ["تهران", "اصفهان", "مشهد", "شیراز", "تبریز"],
    "مارکت_اصلی": ["هایپرمارکت", "فروشگاه زنجیره‌ای", "خرده‌فروشی", "آنلاین", "عمده‌فروشی"]
}
df = pd.DataFrame(data)

# 3. بخش جستجو
st.title("🔍 سامانه تحلیل هوشمند بازار")
search_item = st.text_input("نام محصول را وارد کنید (مثلاً: سس مایونز)", "سس مایونز")

if search_item:
    st.markdown(f"### گزارش وضعیت بازار: {search_item}")
    
    # ردیف اول: لیدرهای بازار
    col1, col2, col3 = st.columns(3)
    
    with col1:
        leader = df.iloc[df['سهم_بازار'].idxmax()]
        st.markdown(f"""<div class="leader-card">
            <div class="leader-title">🏆 لیدر فعلی بازار</div>
            <div class="leader-name">{leader['برند']}</div>
            <div style="color:#10b981">سهم بازار: {leader['سهم_بازار']}٪</div>
        </div>""", unsafe_allow_html=True)
        
    with col2:
        social_star = df.iloc[df['محبوبیت_مجازی'].idxmax()]
        st.markdown(f"""<div class="leader-card" style="border-left-color: #f472b6">
            <div class="leader-title">📱 محبوب شبکه‌های اجتماعی</div>
            <div class="leader-name">{social_star['برند']}</div>
            <div style="color:#f472b6">{social_star['محبوبیت_مجازی']:,} تعامل</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        top_city = df.iloc[0] # فرض بر برند اول
        st.markdown(f"""<div class="leader-card" style="border-left-color: #fbbf24">
            <div class="leader-title">📍 شهر و
