import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. تنظیمات اولیه برای ظاهر اپلیکیشن موبایل
st.set_page_config(page_title="Solico Analytics", layout="centered")

# 2. تزریق CSS پیشرفته برای شبیه‌سازی اپلیکیشن حرفه‌ای
st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    
    * { font-family: 'Vazir', sans-serif; }
    .stApp { background-color: #0e1117; color: white; }
    
    /* استایل کارت‌های KPI */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .metric-value { font-size: 28px; font-weight: 800; color: #38bdf8; }
    .metric-label { font-size: 12px; color: #94a3b8; margin-bottom: 5px; }
    
    /* استایل بخش جستجو */
    .stTextInput input {
        background-color: #1e293b !format;
        border-radius: 10px !important;
        border: 1px solid #38bdf8 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. دیتای فرضی محصولات (قابل اتصال به دیتابیس شما)
data = {
    "برند": ["کاله", "مهرام", "بیژن", "بهروز", "سولیکو"],
    "سهم_بازار": [45, 25, 15, 10, 5],
    "رشد": [12.4, -2.1, 5.8, 8.2, 1.5],
    "تنوع": [120, 85, 45, 60, 30],
    "امتیاز": [4.8, 4.5, 4.2, 4.3, 4.9]
}
df = pd.DataFrame(data)

# --- شروع طراحی بصری ---

# هدر اپلیکیشن شبیه دیجی‌کالا
col_h1, col_h2 = st.columns([1, 4])
with col_h1:
    st.image("https://cdn-icons-png.flaticon.com/512/3502/3502688.png", width=50) # لوگوی فرضی
with col_h2:
    st.markdown("<h2 style='margin-top:0;'>پنل مدیریتی سولیکو</h2>", unsafe_allow_html=True)

# بخش جستجوی هوشمند (Input کاربر)
search_query = st.text_input("🔍 جستجوی محصول یا برند (مثلاً: کاله)...", "")

# فیلتر کردن دیتا بر اساس جستجو
filtered_df = df[df['برند'].str.contains(search_query)] if search_query else df

# نمایش کارت‌های شاخص (KPIs)
st.markdown("### شاخص‌های کلیدی")
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>میانگین رضایت</div>
        <div class='metric-value'>⭐ {filtered_df['امتیاز'].mean():.1f}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>تنوع سبد کالایی</div>
        <div class='metric-value'>{filtered_df['تنوع'].sum()}</div>
    </div>""", unsafe_allow_html=True)

st.write("---")

# نمایش نمودار راداری یا میله‌ای (شبیه تصویر Power BI)
st.markdown("### تحلیل بصری عملکرد")
if not filtered_df.empty:
    fig = px.bar(
        filtered_df, x='برند', y='سهم_بازار', 
        color='رشد', template="plotly_dark",
        color_continuous_scale='Tealgrn'
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# جدول جزئیات با استایل تمیز
st.markdown("### لیست جزئیات محصولات")
st.dataframe(filtered_df.style.highlight_max(axis=0, color='#1e3a8a'))

# فوتر اپلیکیشن (Navigation Bar شبیه‌سازی شده)
st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background: #1e293b; padding: 10px; display: flex; justify-content: space-around; border-top: 1px solid #334155;">
        <span style="font-size:20px;">🏠</span>
        <span style="font-size:20px;">📊</span>
        <span style="font-size:20px;">👤</span>
    </div>
    <br><br>
""", unsafe_allow_html=True)
