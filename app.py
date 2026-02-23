import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اصلی صفحه
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

# استایل CSS برای ظاهر مدرن و تم تیره
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@900&display=swap');
    .main { background-color: #0e1117; }
    .title-text {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(45deg, #00d4ff, #004e92);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }
    .subtitle-text {
        color: #808495;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    </style>
    <p class="title-text">MARKET INTELLIGENCE MATRIX</p>
    <p class="subtitle-text">Strategic Analysis - Esfand 1404</p>
    """, unsafe_allow_html=True)

# دیتابیس هوشمند بر اساس واقعیت اسفند ۱۴۰۴
MARKET_DATA = {
    "سس مایونز": {
        "لیدر": "مهرام",
        "سهم_کل": "۳۸٪",
        "تحلیل": "تسلط کامل مهرام در کانال‌های زنجیره‌ای و خرده‌فروشی مشهود است.",
        "رقیبان": [
            {"برند": "مهرام", "قیمت": 520000, "سهم": 35, "کانال": "زنجیره‌ای / سوپرمارکتی"},
            {"برند": "دلپذیر", "قیمت": 510000, "سهم": 28, "کانال": "B2B / رستوران‌ها"},
            {"برند": "بیژن", "قیمت": 515000, "سهم": 12, "کانال": "B2W / آنلاین"},
            {"برند": "تبرک", "قیمت": 485000, "سهم": 15, "کانال": "سوپرمارکتی / مناطق حاشیه"},
            {"برند": "کاله", "قیمت": 495000, "سهم": 10, "کانال": "زنجیره‌ای / B2W"}
        ]
    },
    "پروتئینی (لوکس و عمومی)": {
        "لیدر": "سولیکو (کاله)",
        "سهم_کل": "۴۵٪",
        "تحلیل": "آندره در بازار پروتئینی‌های لوکس لیدر است، در حالی که سولیکو حجم اصلی زنجیره‌ای را دارد.",
        "رقیبان": [
            {"برند": "سولیکو (کاله)", "قیمت": 2736842, "سهم": 40, "کانال": "زنجیره‌ای / B2W"},
            {"برند": "آندره", "قیمت": 3150000, "سهم": 20, "کانال": "پروتئینی‌های لوکس / B2B"},
            {"برند": "۲۰۲", "قیمت": 2980000, "سهم": 15, "کانال": "سوپرمارکتی (تهران)"},
            {"برند": "میکائیلیان", "قیمت": 4250000, "سهم": 10, "کانال": "B2B لوکس / بوتیک‌ها"},
            {"برند": "شام شام", "قیمت": 2550000, "سهم": 15, "کانال": "B2B دولتی / سوپرمارکتی"}
        ]
    }
}

# بخش جستجو
query = st.selectbox("🎯 انتخاب حوزه برای تحلیل عمیق:", [""] + list(MARKET_DATA.keys()))

if query:
    data = MARKET_DATA[query]
    df = pd.DataFrame(data["رقیبان"])
    
    # نمایش کارت‌های شاخص
    c1, c2, c3 = st.columns(3)
    c1.metric("لیدر بازار", data["لیدر"])
    c2.metric("سهم بازار دسته", data["سهم_کل"])
    c3.metric("میانگین قیمت", f"{int(df['قیمت'].mean()):,}")

    # نمودارهای پیشرفته
    col_left, col_right = st.columns(2)
    
    with col_left:
        fig_bar = px.bar(df, x='برند', y='قیمت', color='کانال', 
                         title="شکاف قیمتی و تمرکز کانال فروش",
                         color_discrete_sequence=px.colors.sequential.Deep)
        fig_bar.update_layout(template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        fig_pie = px.pie(df, values='سهم', names='برند', hole=.4, 
                         title="توزیع قدرت برندها")
        fig_pie.update_layout(template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    # جدول استراتژیک نهایی
    st.markdown("### 📋 ماتریس نفوذ در مارکت")
    st.table(df.style.format({"قیمت": "{:,}"}))

    # تحلیل هوشمند Gemini
    st.markdown("---")
    st.markdown("### 🤖 Strategic Insight (AI)")
    st.info(f"""
    1. در دسته {query}، استراتژی برند **{data['لیدر']}** بر نفوذ حداکثری در کانال‌های زنجیره‌ای استوار است.
    2. برندهایی مثل **آندره** و **میکائیلیان** با حاشیه سود بالاتر در پروتئینی‌های لوکس، بخش B2B ممتاز را قبضه کرده‌اند.
    3. داده‌های اسفند ۱۴۰۴ نشان می‌دهد که قیمت **{df.loc[df['قیمت'].idxmin(), 'برند']}** رقابتی‌ترین گزینه برای نفوذ در مارکت‌های سوپرمارکتی است.
    """)
else:
    st.write("👈 لطفا یک محصول را انتخاب کنید تا ماتریکس تحلیل ظاهر شود.")
