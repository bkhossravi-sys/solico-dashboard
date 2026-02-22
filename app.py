import streamlit as st
import pandas as pd
import pdfplumber
import plotly.express as px

# 1. تنظیمات ظاهری شیک (Power BI Inspired)
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;800&display=swap');
    * { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .app-header {
        background: linear-gradient(90deg, #0f172a 0%, #ef394e 100%);
        padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;
    }
    .search-container { background: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    </style>
    <div class="app-header">
        <h2 style="margin:0;">Market Intelligence Matrix</h2>
        <p style="font-size: 11px; opacity:0.8;">Smart PDF Extraction | Solico Strategic Dashboard</p>
    </div>
""", unsafe_allow_html=True)

# 2. تابع استخراج داده از PDF
@st.cache_data
def extract_data_from_pdf(file_path):
    all_data = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    df_page = pd.DataFrame(table[1:], columns=table[0])
                    all_data.append(df_page)
        
        final_df = pd.concat(all_data, ignore_index=True)
        # تمیز کردن داده‌ها: حذف ردیف‌های خالی
        final_df.dropna(how='all', inplace=True)
        return final_df
    except Exception as e:
        st.error(f"خطا در خواندن PDF: {e}")
        return None

# بارگذاری فایل (نام فایل را دقیقاً مطابق فایل آپلود شده قرار دادم)
file_name = "SolicoPlus  - Material Price -feb 2026.pdf"
df_master = extract_data_from_pdf(file_name)

if df_master is not None:
    # 3. بخش جستجو
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    query = st.text_input("🔍 جستجوی محصول یا برند (مثلاً: زیتون، کالباس، سس):", "")
    st.markdown('</div>', unsafe_allow_html=True)

    if query:
        # جستجو در تمام ستون‌ها (حتی اگر بخشی از کلمه باشد)
        mask = df_master.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
        results = df_master[mask]

        if not results.empty:
            st.success(f"تعداد {len(results)} ردیف یافت شد.")
            
            # نمایش جدول نتایج
            st.subheader("📋 لیست قیمت استخراج شده")
            st.dataframe(results, use_container_width=True, hide_index=True)

            # ۴. تحلیل ستون "فروش" (در صورت وجود)
            # تلاش برای پیدا کردن ستون فروش (ممکن است نام ستون فارسی یا انگلیسی با فاصله باشد)
            sell_col = [c for c in results.columns if "فروش" in str(c) or "Sell" in str(c)]
            
            if sell_col:
                col_name = sell_col[0]
                # تبدیل قیمت به عدد برای رسم نمودار
                results[col_name] = pd.to_numeric(results[col_name].astype(str).str.replace(',', ''), errors='coerce')
                
                fig = px.bar(results.dropna(subset=[col_name]), 
                             x=results.columns[0], y=col_name,
                             title=f"تحلیل ستون {col_name}",
                             color_discrete_sequence=['#ef394e'])
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("نتیجه‌ای یافت نشد.")
    else:
        st.info("💡 نام محصول را وارد کنید تا تحلیل قیمت و رقبا نمایش داده شود.")
else:
    st.error("فایل PDF در مسیر مورد نظر یافت نشد.")

st.markdown("<center style='color:#888; font-size:10px;'>Version 3.0 | 2026 Data Sync</center>", unsafe_allow_html=True)
