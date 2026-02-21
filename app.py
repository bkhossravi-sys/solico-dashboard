import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اصلی
st.set_page_config(page_title="Kalleh Competitive Analysis", layout="wide")

# استایل‌دهی حرفه‌ای
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; }
    .main-card { background: white; border-radius: 15px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; border-right: 8px solid #ef394e; }
    .leader-label { background: #ffd700; color: #000; padding: 2px 10px; border-radius: 5px; font-weight: bold; font-size: 12px; }
    .price-tag { color: #ef394e; font-weight: bold; font-size: 20px; }
    </style>
""", unsafe_allow_html=True)

# ۱. دیتابیس جامع محصولات بر اساس برند کاله و رقبا
MARKET_DATA = [
    {
        "Group": "تون ماهی",
        "Product": "تن ماهی کاله 400 گرمی",
        "Price": 1699000,
        "Leader": "طبیعت",
        "Competitors": {"طبیعت": 1720000, "تحفه": 1750000, "شیلتون": 1680000},
        "Strong_Region": "خراسان و جنوب"
    },
    {
        "Group": "مایونز",
        "Product": "مایونز پرچرب کاله 900 گرمی",
        "Price": 4650000,
        "Leader": "کاله (لیدر تخصصی)",
        "Competitors": {"مهرام": 4800000, "بیژن": 4550000, "بهروز": 4450000},
        "Strong_Region": "مازندران و تهران"
    },
    {
        "Group": "کچاپ",
        "Product": "کچاپ کاله 450 گرمی",
        "Price": 1500000,
        "Leader": "مهرام",
        "Competitors": {"مهرام": 1550000, "دلپذیر": 1480000, "بیژن": 1420000},
        "Strong_Region": "اصفهان و مرکز"
    },
    {
        "Group": "پروتئینی",
        "Product": "بیکن ایرلندی کاله",
        "Price": 9820000,
        "Leader": "سولیکو (لیدر مطلق)",
        "Competitors": {"آندره": 10500000, "۲۰۲": 9500000},
        "Strong_Region": "سراسر کشور"
    }
]

st.title("🛡️ پنل مانیتورینگ محصولات کاله در بازار")

# فیلتر جستجو
search_term = st.text_input("🔍 نام برند یا کالا را وارد کنید (مثلاً: کاله):", value="کاله")

if search_term:
    # فیلتر کردن محصولات کاله از دیتابیس
    filtered_results = [item for item in MARKET_DATA if search_term.lower() in item["Product"].lower() or search_term.lower() in item["Group"].lower()]

    if filtered_results:
        for res in filtered_results:
            with st.container():
                st.markdown(f'<div class="main-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.subheader(f"📦 {res['Product']}")
                    st.write(f"📂 دسته بندی: **{res['Group']}**")
                    st.markdown(f"🚩 لیدر فعلی بازار: <span class='leader-label'>{res['Leader']}</span>", unsafe_allow_html=True)
                
                with col2:
                    st.write("📍 تمرکز منطقه ای:")
                    st.info(res['Strong_Region'])
                
                with col3:
                    st.write("💰 قیمت کاله (ریال):")
                    st.markdown(f"<span class='price-tag'>{res['Price']:,}</span>", unsafe_allow_html=True)
                
                # مقایسه با رقبا در قالب نمودار کوچک
                st.write("📊 **شکاف قیمتی با رقبا:**")
                all_prices = res['Competitors'].copy()
                all_prices["کاله (ما)"] = res['Price']
                df_plot = pd.DataFrame(list(all_prices.items()), columns=['برند', 'قیمت']).sort_values('قیمت')
                
                fig = px.bar(df_plot, x='برند', y='قیمت', text='قیمت', height=300,
                             color='برند', color_discrete_map={"کاله (ما)": "#ef394e"})
                fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("محصولی با این نام در لیست کاله یافت نشد.")
else:
    st.info("نام محصول یا برند را وارد کنید.")
