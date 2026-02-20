import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# تنظیمات صفحه برای نمایش بهینه در موبایل
st.set_page_config(page_title="Solico Sales Dashboard", layout="centered")

# --- استایل دهی سفارشی (CSS) برای شبیه شدن به اپلیکیشن ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stHeader { color: #e63946; }
    .report-header { font-size: 12px; color: #6c757d; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- هدر درخواستی شما ---
st.markdown(f"<p class='report-header'>By: behr.khosravi@solico-group.ir</p>", unsafe_allow_html=True)
st.title("📊 Sales Dashboard")
st.subheader("Market Intelligence: SnappMarket & DigiKala")

# --- بخش داده‌های فرضی (این بخش باید به دیتابیس یا کراولر شما وصل شود) ---
data = {
    'Category': ['سوسیس کالباس', 'سوسیس کالباس', 'سس', 'سس', 'تون ماهی', 'تون ماهی', 'زیتون', 'زیتون'],
    'Brand': ['Kalleh', 'Solico', 'Bijan', 'Kalleh', 'Tofreuh', ' تحفه', 'Solico', 'Mahram'],
    'MarketShare': [45, 30, 40, 25, 50, 20, 35, 15],
    'MarketName': ['SnappMarket', 'DigiKala', 'SnappMarket', 'DigiKala', 'DigiKala', 'SnappMarket', 'SnappMarket', 'DigiKala']
}
df = pd.DataFrame(data)

# --- بخش جستجو (Search Box) ---
search_query = st.text_input("🔍 جستجوی محصول یا برند (مثلاً: سوسیس یا کاله)...")

# فیلتر کردن دیتا بر اساس جستجو
if search_query:
    filtered_df = df[df['Category'].str.contains(search_query) | df['Brand'].str.contains(search_query)]
else:
    filtered_df = df

# --- نمودارهای حرفه‌ای (مشابه تصاویر ارسالی) ---

# 1. سهم بازار کلی (Donut Chart)
st.write("### 🏆 لیدر بازار و سهم برندها")
fig_share = px.pie(filtered_df, values='MarketShare', names='Brand', hole=0.5,
             color_discrete_sequence=px.colors.sequential.RdBu)
fig_share.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
st.plotly_chart(fig_share, use_container_width=True)

# 2. تحلیل مارکت (SnappMarket vs DigiKala)
st.write("### 📍 سرآمدی برند در مارکت")
fig_market = px.bar(filtered_df, x='Brand', y='MarketShare', color='MarketName', barmode='group',
                   title="مقایسه عملکرد در اسنپ مارکت و دیجی‌کالا")
st.plotly_chart(fig_market, use_container_width=True)

# 3. گیج (Gauge Chart) برای عملکرد کلی گروه سولیکو
solico_perf = df[df['Brand'] == 'Solico']['MarketShare'].mean()
fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = solico_perf,
    title = {'text': "Solico Performance Index"},
    gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#e63946"}}
))
st.plotly_chart(fig_gauge, use_container_width=True)

# --- نمایش لیست محصولات (خروجی متنی) ---
st.write("### 📋 لیست محصولات فیلتر شده")
st.dataframe(filtered_df, use_container_width=True)

# --- فوتر اپلیکیشن ---
st.markdown("---")
st.caption("Data Source: Gemini AI & Market Scrapers | Updated: 2026")
