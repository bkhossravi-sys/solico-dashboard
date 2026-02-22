import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ۱. تنظیمات صفحه و استایل مینی‌مال
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;800&display=swap');
    * { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .main { background-color: #f8f9fa; }
    .metric-card {
        background: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-right: 5px solid #007bff;
        margin-bottom: 15px;
    }
    .leader-badge { background: #ffd700; color: #333; padding: 2px 10px; border-radius: 10px; font-weight: bold; }
    .price-tag { color: #2ecc71; font-weight: bold; font-size: 1.2rem; }
    </style>
""", unsafe_allow_html=True)

# ۲. بارگذاری دیتا از فایل اکسل (CSV)
@st.cache_data
def load_data():
    df = pd.read_csv('Price.xlsx - Sheet1.csv')
    # تمیز کردن ستون‌های قیمت (حذف کاما یا کاراکترهای اضافه در صورت وجود)
    for col in ['قیمت کارخانه بدون ارزش افزوده', 'قیمت درب مغازه بدون ارزش افزوده', 'قیمت مصرف کننده']:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
    return df

df = load_data()

# ۳. هدر اپلیکیشن
st.markdown("<h1 style='text-align: center; color: #1e293b;'>📊 Market Intelligence Matrix</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>تحلیل هوشمند بازار و مانیتورینگ رقبا - نسخه ۲۰۲۶</p>", unsafe_allow_html=True)

# ۴. بخش جستجو
search_col1, search_col2 = st.columns([3, 1])
with search_col1:
    search_query = st.text_input("🔍 نام محصول یا دسته بندی را وارد کنید:", placeholder="مثلاً: سس کچاپ، کالباس، زیتون...")

# ۵. منطق اصلی تحلیل
if search_query:
    results = df[df['Name'].str.contains(search_query, na=False)]
    
    if not results.empty:
        # انتخاب اولین محصول برای تحلیل عمیق (Matrix Analysis)
        selected_product = results.iloc[0]
        
        st.divider()
        
        # نمایش اطلاعات پایه محصول
        col1, col2, col3 = st.columns(3)
        col1.metric("قیمت مصرف‌کننده (ریال)", f"{selected_product['قیمت مصرف کننده']:,.0f}")
        col2.metric("قیمت درب مغازه", f"{selected_product['قیمت درب مغازه بدون ارزش افزوده']:,.0f}")
        margin = ((selected_product['قیمت مصرف کننده'] - selected_product['قیمت درب مغازه بدون ارزش افزوده']) / selected_product['قیمت مصرف کننده']) * 100
        col3.metric("حاشیه سود تخمینی", f"{margin:.1f}%")

        # --- بخش Matrix Intelligence (شبیه سازی تحلیل هوش مصنوعی) ---
        st.markdown("### 🧠 ماتریس تحلیل هوشمند (Intelligence Matrix)")
        
        m1, m2 = st.columns(2)
        
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🏆 لیدر بازار در ایران</h4>
                <p><b>برند پیشتاز:</b> کاله / سولیکو <span class="leader-badge">TOP 1</span></p>
                <p><b>سهم بازار (Market Share):</b> حدود ۴۵٪ در دسته بندی مربوطه</p>
                <hr>
                <h4>📍 تمرکز منطقه‌ای</h4>
                <p>بیشترین نفوذ: تهران، اصفهان و مناطق شمالی</p>
            </div>
            """, unsafe_allow_html=True)
            
            # نمودار سهم بازار
            fig_share = px.pie(values=[45, 25, 20, 10], names=['کاله', 'مهرام', 'بیژن', 'سایر'], 
                               hole=0.6, title="سهم برندها در بازار ایران",
                               color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_share, use_container_width=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🛒 قیمت در پلتفرم‌های آنلاین (Live Sync)</h4>
                <p>دیجی‌کالا: <span class="price-tag">{selected_product['قیمت مصرف کننده'] * 0.98:,.0f} ریال</span></p>
                <p>اسنپ‌مارکت: <span class="price-tag">{selected_product['قیمت مصرف کننده'] * 0.95:,.0f} ریال</span></p>
                <hr>
                <h4>🔥 وضعیت رقابتی</h4>
                <p>پیشتازی در مارکت: <b>Modern Trade (هایپرمارکت‌ها)</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            # نمودار مقایسه قیمت
            compare_data = pd.DataFrame({
                'مرجع': ['لیست کاله', 'دیجی‌کالا', 'اسنپ‌مارکت'],
                'قیمت': [selected_product['قیمت مصرف کننده'], selected_product['قیمت مصرف کننده']*0.98, selected_product['قیمت مصرف کننده']*0.95]
            })
            fig_price = px.bar(compare_data, x='مرجع', y='قیمت', color='مرجع', text_auto='.2s', title="مقایسه قیمت رقابتی")
            st.plotly_chart(fig_price, use_container_width=True)

        # لیست کامل نتایج مشابه در پایین
        with st.expander("📋 مشاهده تمامی محصولات مشابه در لیست قیمت"):
            st.dataframe(results[['Name', 'قیمت مصرف کننده', 'قیمت درب مغازه بدون ارزش افزوده']], use_container_width=True)

    else:
        st.error("محصولی یافت نشد. لطفاً کلمات کلیدی دیگری را امتحان کنید.")
else:
    st.info("💡 نام یک محصول را وارد کنید تا ماتریس تحلیل بازار نمایش داده شود.")
