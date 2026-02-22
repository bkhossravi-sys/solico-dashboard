import streamlit as st
import pandas as pd
import plotly.express as px

# 1. تنظیمات ظاهری (UI/UX)
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;800&display=swap');
    * { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .main { background-color: #f8f9fa; }
    .app-header {
        background: #1e3a8a; padding: 1.5rem; border-radius: 15px;
        color: white; text-align: center; margin-bottom: 2rem;
    }
    .metric-box {
        background: white; padding: 15px; border-radius: 12px;
        border-bottom: 4px solid #3b82f6; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .small-title { font-size: 0.9rem; font-weight: 300; color: #e0e0e0; }
    </style>
    <div class="app-header">
        <h2 style="margin:0;">Market Intelligence Matrix</h2>
        <p class="small-title">Solico Group Strategic Dashboard</p>
    </div>
""", unsafe_allow_html=True)

# 2. دیتابیس جامع (Real-world Data Matrix)
DATA = {
    "صنعت سس": [
        {"برند": "مهرام", "سهم": 32, "قیمت": 58500, "وضعیت": "Market Leader"},
        {"برند": "دلپذیر", "سهم": 28, "قیمت": 56000, "وضعیت": "Challenger"},
        {"برند": "کاله (سولیکو)", "سهم": 18, "قیمت": 62000, "وضعیت": "Premium"},
        {"برند": "بیژن", "سهم": 12, "قیمت": 54000, "وضعیت": "Mass Market"}
    ],
    "سوسیس و کالباس": [
        {"برند": "سولیکو (کاله)", "سهم": 46, "قیمت": 245000, "وضعیت": "Dominant Leader"},
        {"برند": "آندره", "سهم": 20, "قیمت": 290000, "وضعیت": "High-End"},
        {"برند": "۲۰۲", "سهم": 15, "قیمت": 215000, "وضعیت": "Growth"},
        {"برند": "گوشتیران", "سهم": 10, "قیمت": 195000, "وضعیت": "Traditional"}
    ],
    "تن ماهی": [
        {"برند": "طبیعت", "سهم": 36, "قیمت": 94000, "وضعیت": "Volume Leader"},
        {"برند": "تحفه", "سهم": 24, "قیمت": 108000, "وضعیت": "Specialty"},
        {"برند": "شیلتون", "سهم": 18, "قیمت": 99000, "وضعیت": "Stable Quality"},
        {"برند": "مکنزی", "سهم": 12, "قیمت": 89000, "وضعیت": "Discount"}
    ],
    "زیتون": [
        {"برند": "بدر", "سهم": 28, "قیمت": 130000, "وضعیت": "Niche Leader"},
        {"برند": "مهرام", "سهم": 22, "قیمت": 122000, "وضعیت": "Retail Focus"},
        {"برند": "کاله", "سهم": 15, "قیمت": 145000, "وضعیت": "Innovation"},
        {"برند": "سمیه", "سهم": 12, "قیمت": 115000, "وضعیت": "Classic"}
    ]
}

# 3. انتخاب محصول
category = st.selectbox("🎯 انتخاب حوزه تحلیل استراتژیک:", list(DATA.keys()))
df = pd.DataFrame(DATA[category])

# 4. شاخص‌های کلیدی (KPIs)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="metric-box">🏆 لیدر فعلی<br><b>{df.iloc[0]["برند"]}</b></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-box">💰 میانگین قیمت بازار<br><b>{int(df["قیمت"].mean()):,} تومان</b></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-box">📈 شدت رقابت<br><b>بسیار بالا</b></div>', unsafe_allow_html=True)

st.write("---")

# 5. نمودارهای زیبا
col_left, col_right = st.columns(2)

with col_left:
    # نمودار دایره‌ای توخالی (Donut)
    fig1 = px.pie(df, values='سهم', names='برند', hole=0.5, 
                 title="سهم بازار برندهای اصلی",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    # نمودار حبابی (Bubble Chart) برای نشان دادن قدرت
    fig2 = px.scatter(df, x="قیمت", y="سهم", size="سهم", color="برند",
                 hover_name="برند", title="ماتریس قیمت - سهم بازار",
                 size_max=50)
    st.plotly_chart(fig2, use_container_width=True)

# 6. جدول نهایی (اصلاح شده برای جلوگیری از خطا)
st.subheader("📋 دیتای عملیاتی و بنچ‌مارک")
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("""
    <div style="text-align:center; margin-top:50px; color:#888;">
        Market Intelligence Dashboard v2.0 | Strategic Insights for Solico Group
    </div>
""", unsafe_allow_html=True)
