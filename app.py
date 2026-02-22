import streamlit as st
import pandas as pd
import plotly.express as px
import random

# تنظیمات صفحه
st.set_page_config(page_title="Solico Deep Market Analysis", layout="wide")

# استایل RTL و فونت
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; }
    .card { background: white; border-radius: 12px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 10px; border-right: 5px solid #ef394e; }
    .price-tag { color: #ef394e; font-weight: bold; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# دیتابیس با لینک‌های استعلام قیمت زنده
MARKET_DATA = {
    "کنسرو": [
        {"Brand": "طبیعت", "Share": 38, "Base": 87000, "Link": "https://snappmarket.com/search?q=تن%20ماهی%20طبیعت"},
        {"Brand": "تحفه", "Share": 26, "Base": 99000, "Link": "https://snappmarket.com/search?q=تن%20ماهی%20تحفه"},
        {"Brand": "شیلتون", "Share": 18, "Base": 92000, "Link": "https://snappmarket.com/search?q=تن%20ماهی%20شیلتون"}
    ],
    "سس": [
        {"Brand": "مهرام", "Share": 32, "Base": 52000, "Link": "https://snappmarket.com/search?q=سس%20مهرام"},
        {"Brand": "کاله", "Share": 15, "Base": 55000, "Link": "https://snappmarket.com/search?q=سس%20کاله"}
    ]
}

st.title("📊 ماتریس هوشمندی بازار (نسخه تعاملی)")

query = st.text_input("جستجوی محصول یا برند:", placeholder="مثلاً: تن ماهی")

if query:
    # منطق پیدا کردن دسته بندی
    cat = "کنسرو" if "تن" in query or "ماهی" in query else "سس" if "سس" in query else None
    
    if cat:
        data = MARKET_DATA[cat]
        st.subheader(f"تحلیل رقابتی دسته {cat}")
        
        cols = st.columns(len(data))
        for i, item in enumerate(data):
            # شبیه‌سازی نوسان قیمت برای واقعی‌تر شدن (تا زمان اتصال به API)
            live_price = item['Base'] + random.randint(-2000, 5000)
            
            with cols[i]:
                st.markdown(f"""
                <div class="card">
                    <h4>{item['Brand']}</h4>
                    <p>سهم بازار: {item['Share']}%</p>
                    <p class="price-tag">{live_price:,} تومان</p>
                    <a href="{item['Link']}" target="_blank">🔗 استعلام زنده از اسنپ‌مارکت</a>
                </div>
                """, unsafe_allow_html=True)
        
        # نمودار
        df = pd.DataFrame(data)
        fig = px.bar(df, x='Brand', y='Share', title="سهم بازار برندها", color='Brand')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("محصول مورد نظر در دیتابیس فعلی یافت نشد.")

