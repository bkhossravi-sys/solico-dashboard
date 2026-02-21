import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات ظاهر حرفه‌ای
st.set_page_config(page_title="Solico Super App", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; }
    .stMetric { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-right: 5px solid #ef394e; }
    </style>
""", unsafe_allow_html=True)

# دیتای واقعی استخراج شده از Book2.pdf
REAL_DATA = [
    {"Name": "سس مایونز پرچرب شیشه ۹۰۰ کاله", "Price": 1041000, "Brand": "Kalleh", "Social": 88},
    {"Name": "سس مایونز کم‌چرب شیشه ۹۰۰ کاله", "Price": 960000, "Brand": "Kalleh", "Social": 75},
    {"Name": "سس مایونز پرچرب پت جار ۹۰۰ کاله", "Price": 4650000, "Brand": "Kalleh", "Social": 60},
    {"Name": "سس مایونز شیشه ۹۰۰ کوچین", "Price": 960000, "Brand": "Cochin", "Social": 45}
]

# دیتای رقبا (تحلیل بازار آنلاین)
COMPETITORS = [
    {"Brand": "مهرام", "Price": 1150000, "Share": 32, "Leader": True},
    {"Brand": "دلپذیر", "Price": 1120000, "Share": 28, "Leader": False},
    {"Brand": "بیژن", "Price": 1090000, "Share": 15, "Leader": False}
]

st.title("🚀 سامانه هوشمند تحلیل بازار")
query = st.text_input("جستجوی سریع محصول (مثلاً: مایونز ۹۰۰)", "")

if query:
    # فیلتر هوشمند بر اساس کلمات کلیدی
    keywords = query.split()
    results = [item for item in REAL_DATA if all(k in item["Name"] for k in keywords)]
    
    if results:
        for res in results:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(res["Name"])
                st.write(f"**قیمت مصوب:** {res['Price']:,} ریال")
            with col2:
                st.metric("محبوبیت اجتماعی", f"{res['Social']}%", "High")
        
        st.write("---")
        st.write("### 📊 تحلیل رقابتی و سهم بازار")
        
        # ترکیب دیتای کاله و رقبا برای نمودار
        chart_data = pd.DataFrame(COMPETITORS + [{"Brand": "کاله", "Price": results[0]["Price"], "Share": 12}])
        
        fig = px.bar(chart_data, x='Brand', y='Price', color='Brand', 
                     title="مقایسه قیمت با رقبا در بازار (ریال)",
                     color_discrete_map={'کاله': '#ef394e'})
        st.plotly_chart(fig, use_container_width=True)
        
        # نمایش لیدر
        leader = next(c["Brand"] for c in COMPETITORS if c["Leader"])
        st.success(f"🏆 لیدر فعلی بازار آنلاین در دسته مایونز: **{leader}** با ۳۲٪ سهم بازار")
    else:
        st.warning("محصولی با این مشخصات در لیست قیمت یافت نشد.")
