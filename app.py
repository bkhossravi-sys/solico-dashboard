import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# تنظیمات اصلی با نام جدید
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

# استایل اختصاصی و حرفه‌ای
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; background-color: #f4f7f6; direction: rtl; }
    
    .main-header { 
        background: linear-gradient(90deg, #1a1a1a 0%, #4a4a4a 100%); 
        padding: 15px; color: white; text-align: right; 
        border-radius: 10px; margin-bottom: 25px;
        border-bottom: 4px solid #ef394e;
    }
    .sub-title { font-size: 10px; font-weight: 300; letter-spacing: 1px; color: #ccc; text-transform: uppercase; }
    .card { 
        background: white; border-radius: 10px; padding: 15px; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px; 
        border: 1px solid #eee; transition: 0.3s;
    }
    .card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .source-tag { font-size: 10px; padding: 2px 8px; border-radius: 10px; background: #f0f0f0; color: #666; }
    </style>
    
    <div class="main-header">
        <span class="sub-title">Market Intelligence Matrix</span>
        <h2 style="margin:0;">سامانه پایش هوشمند بازار (نسخه ۲.۰)</h2>
    </div>
""", unsafe_allow_html=True)

# دیتابیس داخلی (Ground Truth)
MARKET_DATABASE = {
    "سس": [
        {"Brand": "مهرام", "Base_Price": 52000, "Share": 32},
        {"Brand": "کاله (سولیکو)", "Base_Price": 55000, "Share": 12},
        {"Brand": "دلپذیر", "Base_Price": 49500, "Share": 28}
    ],
    "پروتئینی": [
        {"Brand": "سولیکو (کاله)", "Base_Price": 210000, "Share": 46},
        {"Brand": "آندره", "Base_Price": 245000, "Share": 18}
    ]
}

# تابع استعلام قیمت زنده (Mock API Call)
def get_live_prices(category):
    with st.spinner('در حال استعلام لحظه‌ای از Digikala و SnappMarket...'):
        time.sleep(1.5) # شبیه‌سازی زمان اتصال به API
        results = []
        for item in MARKET_DATABASE.get(category, []):
            # شبیه‌سازی نوسان قیمت در پلتفرم‌ها
            dk_price = item['Base_Price'] * random.uniform(0.95, 1.05)
            snapp_price = item['Base_Price'] * random.uniform(0.93, 1.02)
            results.append({
                "Brand": item['Brand'],
                "Digikala": int(dk_price),
                "SnappMarket": int(snapp_price),
                "Market_Share": item['Share']
            })
        return pd.DataFrame(results)

# رابط کاربری جستجو
query = st.text_input("", placeholder="🔍 نام محصول را جهت تحلیل ماتریکس قیمتی وارد کنید...")

if query:
    category = None
    if "سس" in query: category = "سس"
    elif any(x in query for x in ["کالباس", "سوسیس", "پروتئین"]): category = "پروتئینی"

    if category:
        df_live = get_live_prices(category)
        
        # بخش بنچ‌مارک قیمتی
        st.subheader("📊 بنچ‌مارک قیمتی لحظه‌ای")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # نمودار مقایسه‌ای دو پلتفرم
            fig = px.bar(df_live, x="Brand", y=["Digikala", "SnappMarket"], 
                         barmode="group",
                         title="مقایسه قیمت دیجی‌کالا vs اسنپ‌مارکت",
                         color_discrete_map={"Digikala": "#ef394e", "SnappMarket": "#00d170"})
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("### 🛠 تحلیل ماتریکس")
            for _, row in df_live.iterrows():
                diff = row['Digikala'] - row['SnappMarket']
                color = "green" if diff > 0 else "red"
                st.markdown(f"""
                    <div class="card">
                        <b>{row['Brand']}</b><br>
                        <span class="source-tag">اختلاف قیمت: {abs(diff):,} تومان</span>
                        <p style="color:{color}; font-size:12px; margin-top:5px;">
                            {'▲ گران‌تر در دیجی‌کالا' if diff > 0 else '▼ ارزان‌تر در دیجی‌کالا'}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("محصول مورد نظر در دیتابیس یافت نشد.")

