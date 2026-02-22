import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. تنظیمات پیشرفته صفحه
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide", initial_sidebar_state="collapsed")

# 2. تزریق CSS برای استایل مدرن و فونت فارسی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;800&display=swap');
    
    * { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .main { background-color: #f0f2f6; }
    
    /* استایل هدر مشابه اپلیکیشن‌های مدیریتی */
    .app-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 0 0 30px 30px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    .subtitle { font-size: 0.8rem; opacity: 0.8; font-weight: 300; }
    
    /* کارت‌های شاخص */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-right: 5px solid #3b82f6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    .price-val { color: #ef4444; font-size: 1.4rem; font-weight: 800; }
    </style>
    
    <div class="app-header">
        <h1 style="margin:0; font-weight:800; letter-spacing:-1px;">Market Intelligence Matrix</h1>
        <p class="subtitle">Strategic Analysis Dashboard | Powered by Solico Intelligence Group</p>
    </div>
""", unsafe_allow_html=True)

# 3. دیتابیس جامع لیدرهای بازار (Data Matrix)
MARKET_DATA = {
    "سس و چاشنی": [
        {"Brand": "مهرام", "Share": 32, "Price": 58500, "Trend": "+2%", "Status": "Market Leader"},
        {"Brand": "دلپذیر", "Share": 28, "Price": 56000, "Trend": "0%", "Status": "Challenger"},
        {"Brand": "کاله (سولیکو)", "Share": 18, "Price": 62000, "Trend": "+5%", "Status": "Premium/Niche"},
        {"Brand": "بیژن", "Share": 12, "Price": 54000, "Trend": "-1%", "Status": "Mass Market"}
    ],
    "سوسیس و کالباس": [
        {"Brand": "سولیکو (کاله)", "Share": 45, "Price": 245000, "Trend": "+3%", "Status": "Dominant Leader"},
        {"Brand": "آندره", "Share": 20, "Price": 285000, "Trend": "+1%", "Status": "High-End"},
        {"Brand": "۲۰۲", "Share": 15, "Price": 210000, "Trend": "0%", "Status": "Retail Focus"},
        {"Brand": "شام شام", "Share": 10, "Price": 195000, "Trend": "-2%", "Status": "Regional Strong"}
    ],
    "تن ماهی و کنسرو": [
        {"Brand": "طبیعت", "Share": 35, "Price": 92000, "Trend": "+8%", "Status": "Volume Leader"},
        {"Brand": "تحفه", "Share": 25, "Price": 105000, "Trend": "+2%", "Status": "Quality Focus"},
        {"Brand": "شیلتون", "Share": 20, "Price": 98000, "Trend": "0%", "Status": "Stable"},
        {"Brand": "ایلیکا", "Share": 10, "Price": 88000, "Trend": "+1%", "Status": "Economy"}
    ],
    "زیتون و فرآورده‌ها": [
        {"Brand": "بدر", "Share": 30, "Price": 125000, "Trend": "+4%", "Status": "Traditional Leader"},
        {"Brand": "مهرام", "Share": 25, "Price": 118000, "Trend": "+2%", "Status": "Retail Giant"},
        {"Brand": "سمیه", "Share": 15, "Price": 110000, "Trend": "0%", "Status": "Classic Choice"},
        {"Brand": "کاله (سولیکو)", "Share": 12, "Price": 140000, "Trend": "+6%", "Status": "Innovation Leader"}
    ]
}

# 4. بخش جستجو و فیلتر
query = st.selectbox("انتخاب دسته‌بندی استراتژیک محصول:", list(MARKET_DATA.keys()))

if query:
    df = pd.DataFrame(MARKET_DATA[query])
    
    # ردیف اول: کارت‌های خلاصه وضعیت
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card">🟢 لیدر بازار<br><b>{df.iloc[0]["Brand"]}</b></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card">💰 میانگین قیمت<br><b>{int(df["Price"].mean()):,}</b></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card">📊 رقابت‌پذیری<br><b>High</b></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card">🚀 رشد صنعت<br><b>{df.iloc[0]["Trend"]}</b></div>', unsafe_allow_html=True)

    st.write("---")

    # ردیف دوم: نمودارهای پیشرفته
    c1, c2 = st.columns([1, 1])
    
    with c1:
        # نمودار Donut برای سهم بازار
        fig_pie = px.pie(df, values='Share', names='Brand', hole=0.6,
                         title=f"توزیع سهم بازار: {query}",
                         color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_layout(showlegend=True, margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        # نمودار قیمت vs سهم بازار (Bubble Chart)
        fig_bubble = px.scatter(df, x="Price", y="Share", size="Share", color="Brand",
                                 hover_name="Brand", text="Brand", size_max=60,
                                 title="ماتریس قیمت و قدرت بازار")
        fig_bubble.update_layout(xaxis_title="قیمت (تومان)", yaxis_title="سهم بازار (%)")
        st.plotly_chart(fig_bubble, use_container_width=True)

    # ردیف سوم: جدول جزئیات با استایل
    st.subheader("📋 جزئیات عملیاتی رقبای اصلی")
    st.table(df.style.format({"Price": "{:,.0f}"}).background_gradient(subset=['Share'], cmap='BuGn'))

    # فوتر
    st.markdown(f"""
        <div style="text-align:center; padding:20px; color:#666; font-size:12px;">
            دیتای استخراج شده بر اساس گزارش‌های بازاریابی فوریه ۲۰۲۶ | استعلام قیمت از پلتفرم‌های آنلاین
        </div>
    """, unsafe_allow_html=True)
