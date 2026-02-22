import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# تنظیمات اصلی
st.set_page_config(page_title="MIM | Margin Analysis", layout="wide")

# استایل اختصاصی مدیریتی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; background-color: #0d1117; color: #e6edf3; }
    .main-header { background: #161b22; padding: 20px; border-radius: 15px; border-bottom: 4px solid #ef394e; margin-bottom: 25px; }
    .analysis-card { background: #1c2128; border: 1px solid #30363d; padding: 20px; border-radius: 12px; height: 100%; }
    .metric-val { color: #ef394e; font-size: 28px; font-weight: bold; }
    .city-tag { background: #238636; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; }
    </style>
    <div class="main-header">
        <span style="color: #ef394e; font-weight: bold; font-size: 10px; letter-spacing: 2px;">STRATEGIC MARGIN ANALYSIS</span>
        <h2 style="margin:5px 0;">تحلیل حاشیه سود و شکاف قیمتی بازار (اسفند ۱۴۰۴)</h2>
    </div>
""", unsafe_allow_html=True)

# داده‌های پایه بر اساس تصاویر ارسالی کاربر (مهرام حدود 520,000 تومان)
#
MARKET_LEADER_PRICE = 520000 
COMPETITORS = [
    {"Brand": "مهرام", "Share": 35, "Price": 520000, "City": "تهران"},
    {"Brand": "دلپذیر", "Share": 28, "Price": 495000, "City": "مشهد"},
    {"Brand": "بیژن", "Share": 15, "Price": 510000, "City": "شیراز"},
    {"Brand": "بهروز", "Share": 10, "Price": 480000, "City": "اصفهان"}
]

# سایدبار برای تنظیمات تعاملی کاله (سولیکو)
st.sidebar.header("⚙️ تنظیمات قیمت کاله")
kalleh_price = st.sidebar.slider("قیمت پیشنهادی کاله (تومان):", 400000, 600000, 485000, step=5000)
cost_price = st.sidebar.number_input("بهای تمام شده تخمینی (تومان):", value=350000)

# محاسبات تحلیلی
margin_per_unit = kalleh_price - cost_price
margin_percent = (margin_per_unit / kalleh_price) * 100
price_gap = ((MARKET_LEADER_PRICE - kalleh_price) / MARKET_LEADER_PRICE) * 100

# نمایش داشبورد
col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.markdown(f"""<div class="analysis-card">
        <small>حاشیه سود ناخالص کاله</small><br>
        <span class="metric-val">{margin_percent:.1f}%</span><br>
        <small>{margin_per_unit:,} تومان در هر واحد</small>
    </div>""", unsafe_allow_html=True)

with col_m2:
    status_color = "#238636" if price_gap > 5 else "#d29922"
    st.markdown(f"""<div class="analysis-card">
        <small>شکاف قیمتی با لیدر (مهرام)</small><br>
        <span class="metric-val" style="color:{status_color};">{price_gap:.1f}%</span><br>
        <small>کاله ارزان‌تر از لیدر بازار</small>
    </div>""", unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""<div class="analysis-card">
        <small>قدرت نفوذ در بازار</small><br>
        <span class="metric-val">{"بالا" if price_gap > 8 else "متوسط"}</span><br>
        <span class="city-tag">تمرکز: آمل / شمال ایران</span>
    </div>""", unsafe_allow_html=True)

st.write("---")

# نمودار مقایسه‌ای حاشیه سود و قیمت
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📊 بنچ‌مارک قیمتی کل رقبا (Updated)")
    all_data = COMPETITORS + [{"Brand": "کاله (سولیکو)", "Share": 12, "Price": kalleh_price, "City": "آمل"}]
    df = pd.DataFrame(all_data)
    fig = px.bar(df, x='Brand', y='Price', text='Price', color='Brand',
                 color_discrete_map={'کاله (سولیکو)': '#ef394e', 'مهرام': '#30363d'},
                 title="مقایسه قیمت کاله با سایر لیدرهای بازار")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("🏢 سهم بازار و نفوذ شهری")
    # نمایش لیست شهرها به صورت متنی برای وضوح بیشتر
    for index, row in df.iterrows():
        st.markdown(f"**{row['Brand']}**: {row['City']} ({row['Share']}%)")
    
    fig_pie = px.pie(df, values='Share', names='Brand', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.Reds_r)
    fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_pie, use_container_width=True)

st.info(f"💡 تحلیل استراتژیک: با قیمت {kalleh_price:,} تومان، کاله دارای {price_gap:.1f}% مزیت رقابتی نسبت به لیدر بازار (مهرام) است.")
