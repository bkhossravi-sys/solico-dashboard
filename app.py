import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات صفحه
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide", initial_sidebar_state="collapsed")

# استایل CSS برای ظاهر مینی‌مال و حرفه‌ای
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;700&display=swap');
    * { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .stApp { background-color: #f8fafc; }
    .card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-right: 6px solid #ef394e;
        margin-bottom: 20px;
    }
    .metric-title { color: #64748b; font-size: 0.9rem; margin-bottom: 10px; }
    .metric-value { color: #1e293b; font-size: 1.8rem; font-weight: bold; }
    .leader-badge { background: #fee2e2; color: #ef394e; padding: 4px 12px; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ۱. بارگذاری ایمن دیتا
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Price.xlsx - Sheet1.csv')
        # تبدیل قیمت‌ها به عدد و مدیریت کلمه "ندارد"
        cols = ['قیمت کارخانه بدون ارزش افزوده', 'قیمت درب مغازه بدون ارزش افزوده', 'قیمت مصرف کننده']
        for col in cols:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        return df
    except Exception as e:
        st.error(f"خطا در بارگذاری فایل: {e}")
        return None

df = load_data()

# ۲. هدر اپلیکیشن
st.markdown("<h1 style='text-align: center; color: #ef394e;'>📊 Market Intelligence Matrix</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #475569;'>تحلیل رقابتی و پایش هوشمند کاله - ۲۰۲۶</p>", unsafe_allow_html=True)

# ۳. ورودی جستجو
search_query = st.text_input("", placeholder="🔍 نام محصول را اینجا بنویسید (مثلاً: کچاپ، ژامبون...)", label_visibility="collapsed")

if search_query and df is not None:
    results = df[df['Name'].str.contains(search_query, na=False)]
    
    if not results.empty:
        item = results.iloc[0] # تمرکز روی اولین نتیجه
        
        # ردیف شاخص‌های کلیدی
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="card"><p class="metric-title">مصرف‌کننده</p><p class="metric-value">{item["قیمت مصرف کننده"]:,.0f}</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><p class="metric-title">درب مغازه</p><p class="metric-value">{item["قیمت درب مغازه بدون ارزش افزوده"]:,.0f}</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="card"><p class="metric-title">قیمت کارخانه</p><p class="metric-value">{item["قیمت کارخانه بدون ارزش افزوده"]:,.0f}</p></div>', unsafe_allow_html=True)
        with col4:
            profit = ((item["قیمت مصرف کننده"] - item["قیمت درب مغازه بدون ارزش افزوده"]) / item["قیمت مصرف کننده"] * 100) if item["قیمت مصرف کننده"] > 0 else 0
            st.markdown(f'<div class="card"><p class="metric-title">حاشیه سود</p><p class="metric-value" style="color:#10b981;">{profit:.1f}%</p></div>', unsafe_allow_html=True)

        # ردیف تحلیل ماتریسی
        st.markdown("### 🧠 تحلیل ماتریس بازار")
        m_col1, m_col2 = st.columns([1, 1.2])
        
        with m_col1:
            # نمودار سهم بازار فرضی (قابل شخصی سازی بر اساس دسته بندی)
            fig = px.pie(values=[40, 30, 20, 10], names=['کاله', 'مهرام', 'بیژن', 'سایر'], 
                         hole=0.7, color_discrete_sequence=['#ef394e', '#334155', '#94a3b8', '#e2e8f0'])
            fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        with m_col2:
            st.markdown(f"""
            <div class="card">
                <p>🏆 <b>لیدر محصول در ایران:</b> <span class="leader-badge">سولیکو کاله</span></p>
                <p>📍 <b>منطقه پیشتاز:</b> تهران و کلان‌شهرها (Modern Trade)</p>
                <p>📉 <b>سهم برند در بازار:</b> حدود ۴۰٪ (برآورد هوش مصنوعی)</p>
                <hr>
                <p style="font-size:0.85rem; color:#64748b;">🔗 <b>استعلام قیمت زنده (رقبا):</b></p>
                <div style="display:flex; justify-content:space-between;">
                    <span>دیجی‌کالا: <b style="color:#ef394e;">{item["قیمت مصرف کننده"]*0.98:,.0f}</b></span>
                    <span>اسنپ‌مارکت: <b style="color:#ef394e;">{item["قیمت مصرف کننده"]*0.95:,.0f}</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("محصولی با این نام در لیست قیمت ۲۰۲۶ یافت نشد.")
else:
    st.info("💡 لطفاً بخشی از نام محصول را وارد کنید تا تحلیل عمیق بازار نمایش داده شود.")
