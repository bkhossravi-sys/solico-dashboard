import streamlit as st
import pandas as pd
import plotly.express as px

# 1. تنظیمات ظاهری (Modern Management Dashboard)
st.set_page_config(page_title="Solico Market Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;800&display=swap');
    * { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .main-header {
        background: linear-gradient(90deg, #1e293b 0%, #ef394e 100%);
        padding: 1.5rem; border-radius: 15px; color: white; 
        text-align: center; margin-bottom: 2rem;
    }
    .metric-container {
        background: white; padding: 15px; border-radius: 10px;
        border-right: 5px solid #ef394e; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
    <div class="main-header">
        <h2 style="margin:0;">Market Intelligence Matrix</h2>
        <p style="font-size: 0.8rem; opacity:0.8;">Material Price Analysis | Feb 2026</p>
    </div>
""", unsafe_allow_html=True)

# 2. دیتابیس استخراج شده از فایل‌های PDF و XLSX شما
raw_data = [
    # سوسیس و کالباس (دارفرش و فله)
    {"نام کالا": "پپرونی دارفرش", "دسته": "پروتئینی", "قیمت فروش": 4720000},
    {"نام کالا": "سالامی شکاری دارفرش", "دسته": "پروتئینی", "قیمت فروش": 2780000},
    {"نام کالا": "ژامبون راسته با توری", "دسته": "پروتئینی", "قیمت فروش": 5810000},
    {"نام کالا": "بیکن با توری دارفرش", "دسته": "پروتئینی", "قیمت فروش": 5900000},
    {"نام کالا": "مارتادلا دارفرش", "دسته": "پروتئینی", "قیمت فروش": 3120000},
    {"نام کالا": "ژامبون مخلوط دارفرش 250 گرمی", "دسته": "پروتئینی", "قیمت فروش": 5520000},
    {"نام کالا": "ژامبون نوروزی دارفرش 250 گرمی", "دسته": "پروتئینی", "قیمت فروش": 6360000},
    {"نام کالا": "کالباس با پنیر کراکف فله", "دسته": "پروتئینی", "قیمت فروش": 3090000},
    {"نام کالا": "کالباس خشک هلندی 60 فله", "دسته": "پروتئینی", "قیمت فروش": 5670000},
    {"نام کالا": "هات داگ گوشت توری", "دسته": "پروتئینی", "قیمت فروش": 6660000},
    
    # سس‌ها (کاله)
    {"نام کالا": "سس مایونز شیشه 900 گرمی کاله", "دسته": "سس", "قیمت فروش": 1700000},
    {"نام کالا": "سس سزار بطر پت 440 گرمی کاله", "دسته": "سس", "قیمت فروش": 2100000},
    {"نام کالا": "سس کچاپ گالن 2 کیلویی کاله", "دسته": "سس", "قیمت فروش": 3900000},
    {"نام کالا": "سس انار بالزامیک پت 400 گرمی کاله", "دسته": "سس", "قیمت فروش": 1850000},
    {"نام کالا": "سس کچاپ بطر 800 گرمی کاله", "دسته": "سس", "قیمت فروش": 1750000},
    
    # زیتون و سایر
    {"نام کالا": "زیتون پرورده محلی 80 گرمی", "دسته": "زیتون", "قیمت فروش": 550000},
    {"نام کالا": "کمبو دیلایت", "دسته": "سایر", "قیمت فروش": 3820000},
    {"نام کالا": "کمبو پارتی", "دسته": "سایر", "قیمت فروش": 4030000},
    {"نام کالا": "هویج فرمی 70 گرمی (بسته بندی رنگی)", "دسته": "سایر", "قیمت فروش": 735000},
]

df = pd.DataFrame(raw_data)

# 3. موتور جستجوی هوشمند
search_term = st.text_input("🔍 جستجو در محصولات (مثلاً: سس، ژامبون، کاله، دارفرش):", placeholder="نام کالا را وارد کنید...")

if search_term:
    # فیلتر کردن هوشمند
    results = df[df['نام کالا'].str.contains(search_term, case=False, na=False) | 
                df['دسته'].str.contains(search_term, case=False, na=False)]
    
    if not results.empty:
        # نمایش آمار سریع
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-box">🔢 تعداد یافت شده<br><b>{len(results)}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-box">💰 میانگین قیمت فروش<br><b>{int(results["قیمت فروش"].mean()):,} ریال</b></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-box">📈 گران‌ترین کالا<br><b>{results["قیمت فروش"].max():,} ریال</b></div>', unsafe_allow_html=True)

        st.write("---")

        # نمایش جدول و نمودار
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("📋 لیست قیمت مصرف‌کننده")
            st.dataframe(results[['نام کالا', 'قیمت فروش']], use_container_width=True, hide_index=True)

        with col_right:
            st.subheader("📊 بنچ‌
