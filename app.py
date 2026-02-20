import streamlit as st

# تنظیمات صفحه برای موبایل
st.set_page_config(layout="centered")

# استایل‌دهی به سبک Power BI
st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    
    /* کل صفحه */
    .stApp {
        font-family: 'Vazir', sans-serif;
        background-color: #f0f2f5;
    }
    
    /* کارت‌های شاخص (KPI Cards) */
    .kpi-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 15px;
    }
    
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #1f2937;
    }
    
    .kpi-label {
        font-size: 12px;
        color: #6b7280;
    }
    </style>
    """, unsafe_allow_html=True)

# هدر سایت
st.title("📊 داشبورد تحلیلی سولیکو")

# بخش شاخص‌ها (شبیه تصویر Power BI)
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="kpi-card"><div class="kpi-label">سهم کاله</div><div class="kpi-value">۴۵.۸٪</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="kpi-card"><div class="kpi-label">رشد فروش</div><div class="kpi-value text-green-500">۱۲.۴٪+</div></div>', unsafe_allow_html=True)

# دیتای محصولات (مثال با جزئیات زیاد)
st.subheader("جزئیات عملکرد برندها")
brand_data = {
    "برند": ["کاله", "مهرام", "بیژن", "بهروز"],
    "تنوع محصول": [120, 85, 45, 60],
    "امتیاز کیفی": [4.8, 4.5, 4.2, 4.3],
    "وضعیت تامین": ["عالی", "متوسط", "خوب", "عالی"]
}
st.table(brand_data)

# در اینجا می‌توانید نمودار رادار قبلی خود را فراخوانی کنید
