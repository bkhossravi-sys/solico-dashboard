import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات تم حرفه‌ای
st.set_page_config(page_title="Solico Intelligence", layout="wide")

# استایل اختصاصی برای شبیه‌سازی Power BI
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stHeader { background: #ef394e; padding: 20px; color: white; text-align: center; border-radius: 10px; }
    .metric-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-right: 5px solid #ef394e; }
    </style>
""", unsafe_allow_html=True)

# دیتابیس دقیق استخراج شده از فایل SolicoPlus (ستون فروش)
SOLICO_DB = {
    "بیرونی": {"price": 4140351, "unit": "ریال", "leader": "سولیکو", "region": "سراسری", "social": "کاله"},
    "ژامبون راسته": {"price": 5096291, "unit": "ریال", "leader": "آندره / ۲۰۲", "region": "تهران (مناطق لوکس)", "social": "آندره"},
    "مایونز ۹۰۰": {"price": 1041000, "unit": "ریال", "leader": "مهرام", "region": "مرکز و البرز", "social": "بیژن"},
    "کچاپ ۸۰۰": {"price": 1750000, "unit": "ریال", "leader": "دلپذیر", "region": "سراسری", "social": "کاله"},
    "کوکتل هلندی": {"price": 2842105, "unit": "ریال", "leader": "گوشتیران / بشارت", "region": "جنوب و مرکز", "social": "شام شام"},
    "تون ماهی ۱۸۰": {"price": 1699000, "unit": "ریال", "leader": "طبیعت", "region": "شرق و آنلاین", "social": "تحفه"}
}

# بخش هدر ثابت
st.markdown("<div class='stHeader'><h1>📊 پنل هوشمند تحلیل بازار سولیکو</h1><p>By: behr.khosravi@solico-group.ir</p></div>", unsafe_allow_html=True)
st.write("---")

# جستجو
query = st.text_input("🔍 نام محصول را برای تحلیل وارد کنید (مثلاً: مایونز ۹۰۰، بیرونی، ژامبون):")

# منطق خروجی فقط بعد از جستجو
if query:
    # پیدا کردن دقیق‌ترین نتیجه
    match = next((k for k in SOLICO_DB.keys() if query in k), None)
    
    if match:
        data = SOLICO_DB[match]
        
        # نمایش قیمت و لیدر
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='metric-card'><h4>💰 قیمت فروش سولیکو</h4><h2>{data['price']:,} <small>ریال</small></h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-card'><h4>🏆 لیدر بازار</h4><h2>{data['leader']}</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-card'><h4>📍 لیدر منطقه‌ای</h4><h2>{data['region']}</h2></div>", unsafe_allow_html=True)
        
        # نمودار سهم بازار (Power BI Style)
        st.write("### 📉 سهم بازار و نفوذ برندها")
        fig_data = pd.DataFrame({
            'برند': [data['leader'], 'سولیکو', 'سایر رقبا'],
            'سهم': [40, 30, 30]
        })
        fig = px.bar(fig_data, x='برند', y='سهم', color='برند', text='سهم',
                     color_discrete_map={data['leader']: '#333', 'سولیکو': '#ef394e', 'سایر رقبا': '#ccc'})
        st.plotly_chart(fig, use_container_width=True)
        
        # تحلیل استراتژیک
        st.warning(f"💡 **استراتژی پیشنهادی:** لیدر این محصول در شبکه اجتماعی برند **{data['social']}** است. برای افزایش سهم بازار در **{data['region']}**، باید روی قیمت‌های رقابتی اسنپ‌مارکت تمرکز کرد.")
        
        # جدول مقایسه نهایی
        st.write("### 🏁 جدول لیدرهای کشوری")
        summary_df = pd.DataFrame({
            "دسته": ["پروتئینی Mass", "پروتئینی Premium", "سس", "کنسرو ماهی"],
            "لیدر پلتفرم آنلاین": ["سولیکو", "آندره", "مهرام", "طبیعت"],
            "لیدر بازار سنتی": ["گوشتیران", "۲۰۲", "دلپذیر", "تحفه"],
            "برند محبوب اینستاگرام": ["کاله", "آندره", "بیژن", "تحفه"]
        })
        st.table(summary_df)
        
    else:
        st.error("⚠️ محصولی با این نام در لیست قیمت جدید (Feb 2026) یافت نشد.")
else:
    # پیامی که فقط در حالت شروع نمایش داده می‌شود
    st.info("👆 منتظر جستجوی شما هستیم. نام محصول را وارد کنید تا تحلیل عمیق ظاهر شود.")
