import streamlit as st
import pandas as pd
import plotly.express as px

# بررسی نصب بودن کتابخانه برای جلوگیری از کرش
try:
    import pdfplumber
    PDF_READY = True
except ImportError:
    PDF_READY = False

# تنظیمات هدر و استایل
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;800&display=swap');
    * { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .main-title { color: #ef394e; font-weight: 800; text-align: center; border-bottom: 2px solid #ef394e; padding-bottom: 10px; }
    </style>
    <h1 class="main-title">Market Intelligence Matrix</h1>
""", unsafe_allow_html=True)

if not PDF_READY:
    st.error("❌ کتابخانه pdfplumber نصب نیست. لطفا فایل requirements.txt را در گیت‌هاب بسازید.")
    st.stop()

# تابع هوشمند استخراج داده
@st.cache_data
def load_pdf_data(file_path):
    all_rows = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    # استفاده از سطر اول به عنوان تیتر
                    df_temp = pd.DataFrame(table[1:], columns=table[0])
                    all_rows.append(df_temp)
        return pd.concat(all_rows, ignore_index=True)
    except Exception as e:
        st.error(f"خطا در پردازش فایل: {e}")
        return None

# نام فایل PDF شما
PDF_FILE = "SolicoPlus  - Material Price -feb 2026.pdf"

df = load_pdf_data(PDF_FILE)

if df is not None:
    # جستجوی هوشمند
    search_term = st.text_input("🔍 نام محصول یا برند را وارد کنید (مثلاً: زیتون یا کالباس):")

    if search_term:
        # فیلتر کردن در تمام ستون‌ها
        results = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)].copy()
        
        if not results.empty:
            st.success(f"✅ {len(results)} مورد پیدا شد.")
            
            # نمایش جدول
            st.dataframe(results, use_container_width=True)

            # پیدا کردن ستون فروش و رسم نمودار
            sale_col = [c for c in results.columns if "فروش" in str(c)]
            if sale_col:
                s_col = sale_col[0]
                # تبدیل قیمت به عدد (حذف ویرگول و کاراکترهای اضافه)
                results[s_col] = pd.to_numeric(results[s_col].astype(str).str.replace(',', '').str.extract('(\d+)')[0], errors='coerce')
                
                fig = px.bar(results.dropna(subset=[s_col]), 
                             x=results.columns[0], y=s_col, 
                             title="تحلیل قیمت فروش رقبای یافت شده",
                             color_discrete_sequence=['#ef394e'])
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("موردی یافت نشد.")
else:
    st.info("لطفاً مطمئن شوید فایل PDF در مخزن گیت‌هاب آپلود شده است.")

st.write("---")
st.caption("Solico Strategic Tool | Daily English Practice: 'Search query results'")
