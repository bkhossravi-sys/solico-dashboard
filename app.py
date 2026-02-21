import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اصلی داشبورد
st.set_page_config(page_title="Solico Plus Intelligence", layout="wide")

# استایل CSS حرفه‌ای
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .stHeader { background: #ef394e; padding: 1rem; border-radius: 10px; color: white; text-align: center; }
    .leader-card { border: 2px solid #ef394e; border-radius: 15px; padding: 20px; background: #fff5f6; }
    .strategy-text { background: #e8f4fd; padding: 15px; border-left: 5px solid #2196f3; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='stHeader'><h1>🚀 سوپر اپ تحلیلی سولیکو پلاس (Feb 2026)</h1><p>By: behr.khosravi@solico-group.ir</p></div>", unsafe_allow_html=True)

# دیتابیس استخراج شده از فایل SolicoPlus (فقط قیمت‌های ستون فروش)
SOLICO_DATA = {
    "بیرونی": {"price": 4140351, "cat": "پروتئینی", "leader": "سولیکو", "region": "کل ایران"},
    "ژامبون راسته": {"price": 5096291, "cat": "پروتئینی", "leader": "سولیکو", "region": "تهران/شمال"},
    "مارشن": {"price": 5271929, "cat": "پروتئینی", "leader": "۲۰۲ / آندره", "region": "تهران"},
    "سوسیس هلندی": {"price": 2842105, "cat": "پروتئینی", "leader": "گوشتیران", "region": "مرکزی"},
    "کچاپ ۸۰۰": {"price": 1750000, "cat": "سس", "leader": "دلپذیر", "region": "سراسری"},
    "مایونز ۹۰۰": {"price": 1041000, "cat": "سس", "leader": "مهرام", "region": "البرز/تهران"},
    "تن ماهی ۱۸۰": {"price": 1699000, "cat": "کنسرو", "leader": "طبیعت", "region": "خراسان/آنلاین"}
}

# بخش جستجوی هوشمند
query = st.text_input("🔍 جستجوی محصول (مثلاً: بیرونی، ژامبون، مایونز)...")

if query:
    # جستجو در نام کلیدها
    match = next((k for k in SOLICO_DATA.keys() if query in k), None)
    
    if match:
        data = SOLICO_DATA[match]
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.markdown(f"""
            <div class='leader-card'>
                <h3>{match}</h3>
                <p>💰 <b>قیمت فروش مبنا:</b> {data['price']:,} ریال</p>
                <p>🏆 <b>لیدر بازار:</b> {data['leader']}</p>
                <p>📍 <b>تمرکز جغرافیایی لیدر:</b> {data['region']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            # نمودار سهم بازار فرضی بر اساس تحلیل مارکت
            fig = px.pie(names=['سولیکو', 'رقیب اصلی', 'سایر'], values=[45, 35, 20], 
                         title="سهم بازار تخمینی (Online + Offline)", hole=0.4,
                         color_discrete_sequence=['#ef394e', '#333', '#ccc'])
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 💡 استراتژی افزایش سهم بازار")
        if data['leader'] == "سولیکو":
            st.info("وضعیت: **حاکمیت بر بازار**. پیشنهاد: حفظ حاشیه سود و جلوگیری از نفوذ برندهای لوکس مثل آندره.")
        else:
            st.warning(f"وضعیت: **رقابتی**. لیدر این بخش {data['leader']} است. پیشنهاد: تمرکز بر پروموشن در اسنپ‌مارکت برای بازپس‌گیری سهم.")

# جدول نهایی لیدرها (درخواستی شما)
st.write("---")
st.write("### 🏁 گزارش نهایی لیدرهای بازار ایران (۲۰۲۶)")
final_report = pd.DataFrame({
    "دسته محصول": ["سوسیس کالباس (High-End)", "سوسیس کالباس (Mass)", "سس مایونز", "سس کچاپ", "تن ماهی", "زیتون"],
    "برند لیدر": ["آندره / ۲۰۲", "سولیکو (کاله)", "مهرام", "دلپذیر", "طبیعت", "بدر / اصالت"],
    "بازار هدف": ["اسنپ مارکت / تهران", "سراسری / هایپرها", "فروشگاه زنجیره‌ای", "خرده‌فروشی", "دیجی‌کالا / عمده", "بازار سنتی"],
    "قطب جغرافیایی": ["تهران - منطقه ۱ تا ۵", "اصفهان / مشهد / شمال", "قزوین / زنجان", "سراسری", "خراسان / سیستان", "مرکز ایران"]
})
st.table(final_report)
