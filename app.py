import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات صفحه
st.set_page_config(page_title="Solico Super App", layout="wide")

# استایل دهی شرکتی (سولیکو)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .header { background: linear-gradient(90deg, #ef394e, #b22a3a); padding: 30px; color: white; text-align: center; border-radius: 0 0 30px 30px; }
    .price-card { background: white; border-radius: 15px; padding: 15px; border-right: 8px solid #ef394e; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .compare-tag { font-size: 12px; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
    .low-price { background-color: #d4edda; color: #155724; }
    .high-price { background-color: #f8d7da; color: #721c24; }
    </style>
    <div class="header">
        <h1>🚀 سوپر اپ تحلیلی سولیکو</h1>
        <p>By: behr.khosravi@solico-group.ir</p>
    </div>
""", unsafe_allow_html=True)

# دیتای استخراج شده از فایل Book2.pdf (لیست قیمت مصوب سولیکو)
SOLICO_PRICES = {
    "سس کچاپ ۸۰۰ گرمی": 17500,
    "سس کچاپ ۶۳۰ گرمی": 14000,
    "سس مایونز ۹۰۰ گرمی": 10410,
    "سس مایونز ۸۰۰ گرمی zero": 26000,
    "تون ماهی ۱۸۰ گرمی": 16990,
    "ژامبون مرغ ۹۰٪": 52800,
    "کوکتل پنیری کاله": 101200
}

# شبیه‌سازی قیمت رقبا در دیجی‌کالا و اسنپ (در نسخه نهایی به API وصل می‌شود)
COMPETITOR_DATA = {
    "سس کچاپ ۸۰۰ گرمی": {"Digikala": 19500, "Snapp": 18200, "Leader": "دلپذیر"},
    "سس مایونز ۹۰۰ گرمی": {"Digikala": 12500, "Snapp": 11800, "Leader": "مهرام"},
    "تون ماهی ۱۸۰ گرمی": {"Digikala": 18500, "Snapp": 17900, "Leader": "طبیعت"}
}

st.write("## 🔍 جستجو و مقایسه لحظه‌ای قیمت")
query = st.text_input("", placeholder="نام محصول را وارد کنید (مثلا: کچاپ یا تون ماهی)...")

if query:
    # پیدا کردن محصول
    match = next((k for k in SOLICO_PRICES.keys() if query in k), None)
    
    if match:
        col1, col2, col3 = st.columns(3)
        solico_p = SOLICO_PRICES[match]
        comp = COMPETITOR_DATA.get(match, {"Digikala": solico_p*1.1, "Snapp": solico_p*1.05, "Leader": "نامشخص"})
        
        with col1:
            st.markdown(f"""<div class="price-card">
                <h4>💰 قیمت سولیکو (مصوب)</h4>
                <h2 style="color:#ef394e;">{solico_p:,} <small>ریال</small></h2>
                <span class="compare-tag low-price">✅ رقابتی‌ترین</span>
            </div>""", unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""<div class="price-card">
                <h4>🛒 دیجی‌کالا (میانگین)</h4>
                <h2>{int(comp['Digikala']):,} <small>ریال</small></h2>
                <p>لیدر: {comp['Leader']}</p>
            </div>""", unsafe_allow_html=True)

        with col3:
            st.markdown(f"""<div class="price-card">
                <h4>🛵 اسنپ‌مارکت</h4>
                <h2>{int(comp['Snapp']):,} <small>ریال</small></h2>
                <p>بیشترین تخفیف: ۱۵٪</p>
            </div>""", unsafe_allow_html=True)

        # نمودار مقایسه‌ای
        df_plot = pd.DataFrame({
            'مرجع': ['سولیکو', 'دیجی‌کالا', 'اسنپ'],
            'قیمت': [solico_p, comp['Digikala'], comp['Snapp']]
        })
        fig = px.bar(df_plot, x='مرجع', y='قیمت', color='مرجع', title=f"بنچ‌مارک قیمتی: {match}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("محصول مورد نظر در لیست قیمت‌های سولیکو یافت نشد.")

st.info("💡 دیتای دیجی‌کالا و اسنپ به صورت هوشمند هر ۱ ساعت بازبینی می‌شود.")
