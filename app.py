import streamlit as st
import pandas as pd
import plotly.express as px

# ۱. تنظیمات ظاهری خفن و فونت‌های حرفه‌ای
st.set_page_config(page_title="MIM | Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTitle {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #00d4ff;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 800;
        text-shadow: 2px 2px 10px rgba(0,212,255,0.3);
    }
    .market-header {
        background: linear-gradient(90deg, #00d4ff 0%, #004e92 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# ۲. دیتابیس غنی‌شده با کانال‌های توزیع و داده‌های فایل PDF
# قیمت‌ها بر اساس لیست اسفند ۱۴۰۴ و تصاویر شما تنظیم شده‌اند
MARKET_DB = {
    "سس مایونز": {
        "لیدر": "مهرام",
        "سهم_دسته": "۳۸٪",
        "رقیبان": [
            {"برند": "مهرام", "قیمت": 520000, "تمرکز": "سوپرمارکتی / زنجیره‌ای", "سهم": 35},
            {"برند": "دلپذیر", "قیمت": 510000, "تمرکز": "زنجیره‌ای / B2B", "سهم": 28},
            {"برند": "کاله (سولیکو)", "قیمت": 495000, "تمرکز": "مدرن / B2W", "سهم": 15},
            {"برند": "تبرک", "قیمت": 485000, "تمرکز": "سوپرمارکتی / مناطق حاشیه", "سهم": 12},
            {"برند": "بیژن", "قیمت": 515000, "تمرکز": "فروشگاه‌های آنلاین / زنجیره‌ای", "سهم": 10}
        ]
    },
    "ژامبون و پروتئینی": {
        "لیدر": "سولیکو (کاله)",
        "سهم_دسته": "۴۵٪",
        "رقیبان": [
            [span_0](start_span){"برند": "سولیکو (کاله)", "قیمت": 2736842, "تمرکز": "زنجیره‌ای / B2W (سراسری)", "سهم": 40}, #[span_0](end_span)
            {"برند": "آندره", "قیمت": 3100000, "تمرکز": "پروتئینی‌های لوکس / B2B", "sهم": 20},
            {"برند": "۲۰۲", "قیمت": 2950000, "تمرکز": "سوپرمارکتی / تهران و کرج", "سهم": 15},
            {"برند": "شام شام", "قیمت": 2600000, "تمرکز": "بخش دولتی / ارگان‌ها", "سهم": 15},
            {"برند": "میکائیلیان", "قیمت": 4200000, "تمرکز": "تک‌فروشی لوکس (بوتیک پروتئین)", "سهم": 10}
        ]
    }
}

# --- بخش اصلی برنامه ---
st.markdown('<p class="market-header">MARKET INTELLIGENCE MATRIX</p>', unsafe_allow_html=True)
st.markdown("---")

# جستجوی هوشمند
col_search, col_space = st.columns([2, 2])
with col_search:
    query = st.selectbox("🎯 انتخاب حوزه تحلیل استراتژیک:", [""] + list(MARKET_DB.keys()))

if query:
    data = MARKET_DB[query]
    df = pd.DataFrame(data["رقیبان"])
    
    # نمایش شاخص‌های کلیدی (Metrics)
    c1, c2, c3 = st.columns(3)
    c1.metric("لیدر فعلی بازار", data["لیدر"])
    c2.metric("سهم کل این دسته در بازار", data["سهم_دسته"])
    c3.metric("میانگین قیمت بازار", f"{int(df['قیمت'].mean()):,}")

    st.markdown("### 📊 تحلیل بصری رقبا")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # نمودار مقایسه قیمت (Plotly)
        fig_price = px.bar(df, x='برند', y='قیمت', color='برند', 
                          title="بنچ‌مارک قیمتی (تومان)",
                          color_discrete_sequence=px.colors.sequential.Blues_r)
        fig_price.update_layout(template="plotly_dark")
        st.plotly_chart(fig_price, use_container_width=True)

    with col_chart2:
        # نمودار سهم بازار و نفوذ
        fig_pie = px.pie(df, values='سهم', names='برند', hole=.4,
                        title="سهم بازار و نفوذ در کانال‌های فروش")
        fig_pie.update_layout(template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    # جدول استراتژیک توزیع
    st.markdown("### 🏘️ تحلیل کانال‌های نفوذ (Distribution Channels)")
    
    # استایل‌دهی به جدول
    styled_df = df.style.format({"قیمت": "{:,}"}).background_gradient(subset=["سهم"], cmap="Blues")
    st.table(styled_df)

    # تحلیل نهایی جمینای (متصل به دانش اسفند ۱۴۰۴)
    st.markdown("### 🤖 Strategic Insight (Gemini AI)")
    st.success(f"""
    1. **تمرکز کانال توزیع:** برند **{data['لیدر']}** با تسلط بر کانال‌های **B2W** و **زنجیره‌ای** بیشترین رشد را داشته، در حالی که برندی مثل **آندره** یا **میکائیلیان** با تمرکز بر **پروتئینی‌های لوکس و B2B** حاشیه سود خود را حفظ کرده‌اند.
    2. **تحلیل قیمت:** شکاف قیمتی در بازار {query} نشان می‌دهد که تمایل مشتریان به سمت برندهای با قیمت اقتصادی در کانال‌های **سوپرمارکتی** افزایش یافته است.
    3. **[span_1](start_span)[span_2](start_span)پیشنهاد استراتژیک:** برای ورود به این بازار، تمرکز بر کانال **B2B (رستوران‌ها و کترینگ‌ها)** با قیمت رقابتی برندهایی مثل کاله، بهینه‌ترین مسیر نفوذ است.[span_1](end_span)[span_2](end_span)
    """)

else:
    st.warning("👈 حوزه محصول را برای دریافت ماتریکس تحلیلی انتخاب کنید.")
