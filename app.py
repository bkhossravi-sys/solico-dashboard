import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# تنظیمات تم حرفه‌ای
st.set_page_config(page_title="Solico Market Intelligence", layout="wide")

# استایل اختصاصی مشابه Power BI Mobile
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .strategy-box { background-color: #fff3cd; border-right: 5px solid #ffc107; padding: 15px; border-radius: 5px; color: #856404; }
    .leader-label { color: #ef394e; font-weight: bold; font-size: 20px; }
    </style>
""", unsafe_allow_html=True)

# دیتابیس استخراج شده از فایل SolicoPlus - Feb 2026
PRODUCTS_DB = {
    "مایونز ۹۰۰": {"price": 1041000, "comp_digi": 1150000, "comp_snapp": 1120000, "leader": "مهرام", "social": "بیژن", "share": {"مهرام": 35, "کاله": 15, "دلپذیر": 25, "سایر": 25}, "strategy": "تمرکز بر پروموشن‌های 'یکی بخر دوتا ببر' در اسنپ‌مارکت برای کاهش فاصله با مهرام."},
    "کچاپ ۸۰۰": {"price": 1750000, "comp_digi": 1900000, "comp_snapp": 1850000, "leader": "دلپذیر", "social": "کاله", "share": {"دلپذیر": 40, "کاله": 25, "مهرام": 20, "سایر": 15}, "strategy": "استفاده از محتوای ویدئویی در اینستاگرام با تمرکز بر غلظت محصول جهت حفظ برتری اجتماعی."},
    "کوکتل پنیری": {"price": 10120000, "comp_digi": 11200000, "comp_snapp": 10950000, "leader": "کاله (سولیکو)", "social": "کاله", "share": {"کاله": 55, "آندره": 20, "۲۰۲": 15, "سایر": 10}, "strategy": "حفظ قیمت فعلی و افزایش شلف‌اسپیس در فروشگاه‌های زنجیره‌ای سطح A."},
    "تون ماهی": {"price": 1699000, "comp_digi": 1850000, "comp_snapp": 1780000, "leader": "طبیعت", "social": "تحفه", "share": {"طبیعت": 38, "تحفه": 30, "کاله": 12, "سایر": 20}, "strategy": "تغییر بسته‌بندی به 'آسان‌بازشو' و باندل کردن با سس مایونز برای افزایش سهم بازار."}
}

# هدر
st.markdown("<h1 style='text-align: center; color: #ef394e;'>Solico Plus Intelligence Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>By: behr.khosravi@solico-group.ir</p>", unsafe_allow_html=True)

# جستجوی هوشمند
query = st.text_input("🔍 نام محصول یا وزن را وارد کنید (مثلاً: مایونز ۹۰۰ یا کوکتل):")

if query:
    # پیدا کردن محصول متناسب
    found_key = next((k for k in PRODUCTS_DB.keys() if query in k), None)
    
    if found_key:
        data = PRODUCTS_DB[found_key]
        
        # ردیف اول: متریک‌های کلیدی
        col1, col2, col3 = st.columns(3)
        col1.metric("قیمت فروش کاله (ریال)", f"{data['price']:,}", delta="-2% نسبت به رقیب")
        col2.metric("لیدر بازار", data['leader'])
        col3.metric("محبوب‌ترین در سوشیال", data['social'])

        # ردیف دوم: نمودارها
        c1, c2 = st.columns(2)
        
        with c1:
            st.write("### 📊 سهم بازار برندها")
            fig_pie = px.pie(values=list(data['share'].values()), names=list(data['share'].keys()), hole=0.6, color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c2:
            st.write("### 🛒 مقایسه قیمت آنلاین (ریال)")
            fig_bar = go.Figure(data=[
                go.Bar(name='سولیکو', x=['Base'], y=[data['price']], marker_color='#ef394e'),
                go.Bar(name='دیجی‌کالا', x=['Base'], y=[data['comp_digi']], marker_color='#00b4d8'),
                go.Bar(name='اسنپ', x=['Base'], y=[data['comp_snapp']], marker_color='#00f5d4')
            ])
            st.plotly_chart(fig_bar, use_container_width=True)

        # ردیف سوم: تحلیل استراتژیک
        st.markdown(f"### 💡 استراتژی افزایش سهم بازار (Action Plan)")
        st.markdown(f"<div class='strategy-box'>{data['strategy']}</div>", unsafe_allow_True=True)
        
        # جدول سهم بازار
        st.write("### 📑 جدول جزئیات سهم بازار")
        df_share = pd.DataFrame(list(data['share'].items()), columns=['Brand', 'Market Share %'])
        st.table(df_share)
        
    else:
        st.error("محصول در دیتابیس Feb 2026 یافت نشد.")
else:
    st.info("لطفاً عبارتی مثل 'مایونز' یا 'کچاپ' را برای تحلیل عمیق جستجو کنید.")
