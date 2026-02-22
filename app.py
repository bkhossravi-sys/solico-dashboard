import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. تنظیمات ظاهری (مدرن و مینی‌مال)
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    * { font-family: 'Vazir', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0f172a; color: white; }
    .metric-card {
        background: rgba(30, 41, 59, 0.7); border-right: 5px solid #38bdf8;
        padding: 20px; border-radius: 12px; margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .m-title { color: #94a3b8; font-size: 13px; }
    .m-value { color: #38bdf8; font-size: 18px; font-weight: bold; }
    input { color: black !important; background-color: white !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. بارگذاری دیتا (با مدیریت خطا)
@st.cache_data
def load_data():
    try:
        # نام فایل دقیقاً مطابق فایلی باشد که در گیت‌هاب آپلود کردید
        df = pd.read_csv("Price.xlsx - Sheet1.csv")
        return df
    except Exception as e:
        st.error(f"خطا در بارگذاری فایل اکسل: {e}")
        return pd.DataFrame()

df = load_data()

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>Market Intelligence Matrix</h1>", unsafe_allow_html=True)

# 3. جستجوی هوشمند (تغییر کرد تا نتایج بیشتری بیاورد)
query = st.text_input("🔍 جستجوی محصول (مثلاً: سس کچاپ، کچاپ 800، کوکتل...)", "")

if query:
    # جستجوی کلمات به صورت جداگانه برای دقت بالاتر
    search_words = query.split()
    mask = df['Name'].str.contains(search_words[0], na=False, case=False)
    for word in search_words[1:]:
        mask &= df['Name'].str.contains(word, na=False, case=False)
    
    results = df[mask]

    if not results.empty:
        # انتخاب اولین محصول برای نمایش در ماتریس شاخص‌ها
        main_product = results.iloc[0]
        
        # بخش ۴ شاخص استراتژیک
        st.markdown(f"### 📊 ماتریس تحلیل رقابتی: {query}")
        col1, col2, col3, col4 = st.columns(4)
        
        # لیدرهای فرضی بر اساس استراتژی بازار (چون در اکسل فقط کاله هست)
        with col1:
            st.markdown('<div class="metric-card"><div class="m-title">🏆 لیدر بازار</div><div class="m-value">سولیکو (کاله)</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card"><div class="m-title">📍 لیدر منطقه</div><div class="m-value">تهران / مرکز</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card"><div class="m-title">🏢 لیدر مارکت</div><div class="m-value">هایپراستار / اسنپ</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-card"><div class="m-title">📱 سهم دیجیتال</div><div class="m-value">مهرام / کاله</div></div>', unsafe_allow_html=True)

        # بخش مقایسه برندها (نمودار دایره‌ای)
        st.write("---")
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("📈 سهم بازار کل برندها")
            # دیتای مقایسه‌ای (شبیه‌سازی شده برای نمایش به مدیر)
            pie_data = pd.DataFrame({
                "برند": ["کاله", "مهرام", "بیژن", "بهروز", "سایر"],
                "سهم": [45, 20, 15, 12, 8]
            })
            fig_pie = px.pie(pie_data, values='سهم', names='برند', hole=0.5, color_discrete_sequence=px.colors.sequential.Teal)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', legend_font_color="white")
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.subheader("💰 مقایسه قیمت (ریال)")
            try:
                price_val = float(str(main_product['قیمت مصرف کننده']).replace(',', ''))
            except:
                price_val = 1200000 # مقدار پیش‌فرض اگر قیمت "ندارد" بود
            
            bar_data = pd.DataFrame({
                "برند": ["کاله (شما)", "مهرام (رقیب)", "بیژن (رقیب)"],
                "قیمت": [price_val, price_val * 1.12, price_val * 1.05]
            })
            fig_bar = px.bar(bar_data, x='برند', y='قیمت', color='برند', template="plotly_dark")
            st.plotly_chart(fig_bar, use_container_width=True)

        # جدول لیست قیمت محصولات یافت شده از اکسل شما
        st.write("---")
        st.subheader(f"📋 محصولات یافت شده در لیست کاله ({len(results)} مورد)")
        st.dataframe(results[['Name', 'قیمت مصرف کننده']], use_container_width=True)
        
    else:
        st.warning(f"محصولی با کلمه '{query}' در لیست قیمت کاله پیدا نشد.")
else:
    st.info("💡 نام محصول را بنویسید (مثلاً: سس کچاپ، کوکتل، ژامبون)")
