import streamlit as st
import pandas as pd
import plotly.express as px

# 1. تنظیمات ظاهری (Power BI Style)
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;800&display=swap');
    * { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .app-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 100%);
        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;
    }
    .result-card {
        background: white; padding: 20px; border-radius: 15px;
        border-right: 8px solid #ef394e; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
    <div class="app-header">
        <h2 style="margin:0; font-size: 25px;">Market Intelligence Matrix</h2>
        <p style="font-size: 12px; opacity:0.7;">Strategic Search Engine | Solico Group</p>
    </div>
""", unsafe_allow_html=True)

# 2. بارگذاری دیتا با مدیریت خطا
@st.cache_data
def load_data():
    try:
        # خواندن فایل آپلود شده
        df = pd.read_csv("Price.xlsx - Sheet1.csv")
        return df
    except:
        return None

df_master = load_data()

if df_master is not None:
    # 3. کادر جستجوی متمرکز
    search_query = st.text_input("🔍 نام محصول، برند یا دسته‌بندی را جستجو کنید:", placeholder="مثلاً: زیتون کاله، سس مهرام...")

    if search_query:
        # جستجوی داینامیک در تمام ستون‌ها
        mask = df_master.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        results = df_master[mask]

        if not results.empty:
            st.success(f"تعداد {len(results)} مورد یافت شد.")
            
            # نمایش شاخص‌های سریع
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.subheader("📋 لیست قیمت و رقبا")
                st.dataframe(results, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                # نمودار مقایسه قیمت محصولات یافت شده
                if 'قیمت' in results.columns or 'Price' in results.columns:
                    price_col = 'قیمت' if 'قیمت' in results.columns else 'Price'
                    name_col = results.columns[0] # فرض بر اینکه ستون اول نام محصول است
                    
                    fig = px.bar(results, x=name_col, y=price_col, 
                                 title="بنچ‌مارک قیمتی موارد یافت شده",
                                 color=price_col, color_continuous_scale='Reds')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("برای نمایش نمودار، ستونی با نام 'قیمت' در فایل اکسل نیاز است.")
        else:
            st.warning("موردی یافت نشد. لطفاً عبارت دیگری را امتحان کنید.")
    else:
        st.info("👆 برای شروع، نام محصول را در کادر بالا وارد کنید.")
else:
    st.error("❌ فایل Price.xlsx - Sheet1.csv پیدا نشد. لطفا مطمئن شوید فایل در کنار کد قرار دارد.")

st.markdown("<br><br><center style='color:#ccc; font-size:10px;'>Designed for Strategic Market Analysis</center>", unsafe_allow_html=True)
