import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اصلی
st.set_page_config(page_title="Solico Super App", layout="wide")

# استایل اختصاصی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: #ef394e; padding: 25px; color: white; text-align: center; border-radius: 0 0 20px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .metric-box { background: white; padding: 20px; border-radius: 12px; border-right: 6px solid #ef394e; box-shadow: 0 4px 8px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .strategy-card { background: #fef9e7; border: 1px dashed #f39c12; padding: 15px; border-radius: 10px; color: #7d6608; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>🚀 سامانه تحلیل بازار سولیکو پلاس</h1><p>Data Source: SolicoPlus-Feb 2026</p></div>", unsafe_allow_html=True)

# دیتابیس دقیق بر اساس استخراج مجدد از فایل SolicoPlus (ستون فروش)
DB = {
    "مایونز ۹۰۰": {
        "full_name": "سس مایونز پرچرب پت جار ۹۰۰ کاله",
        "price": 4650000, 
        "leader": "مهرام / بیژن",
        "region_leader": "البرز و تهران",
        "social_star": "بیژن",
        "strategy": "با توجه به قیمت ۴۶۵,۰۰۰ تومانی پت جار، تمرکز باید بر فروش B2B و رستوران‌های زنجیره‌ای لوکس باشد تا سهم بازار از رقبایی مثل مهرام پس گرفته شود."
    },
    "بیرونی": {
        "full_name": "بیرونی (کد ۳۰۰۰۵۴۳۷)",
        "price": 4140351,
        "leader": "سولیکو (کاله)",
        "region_leader": "اصفهان، مشهد و سراسری",
        "social_star": "کاله",
        "strategy": "حفظ جایگاه لیدری با تکیه بر زنجیره توزیع مویرگی در گوشی‌های موبایل (اسنپ‌مارکت)."
    },
    "ژامبون راسته": {
        "full_name": "ژامبون راسته توری (کد ۳۰۰۰۵۴۶۶)",
        "price": 5096291,
        "leader": "آندره / ۲۰۲",
        "region_leader": "شمال تهران و لواسان",
        "social_star": "آندره",
        "strategy": "افزایش حضور در شلف‌های VIP فروشگاه‌های زنجیره‌ای برای رقابت مستقیم با آندره."
    },
    "هلندی": {
        "full_name": "کوکتل هلندی فیله",
        "price": 2842105,
        "leader": "گوشتیران / بشارت",
        "region_leader": "جنوب ایران (شیراز/اهواز)",
        "social_star": "شام شام",
        "strategy": "استفاده از قیمت رقابتی برای نفوذ به بازار جنوب و مقابله با لیدری بشارت."
    }
}

st.write("---")
query = st.text_input("🔍 جستجوی محصول (مثلاً: مایونز ۹۰۰، بیرونی، هلندی...):")

# خروجی فقط در صورت جستجو
if query:
    match = next((k for k in DB.keys() if query in k), None)
    
    if match:
        data = DB[match]
        st.success(f"نتایج برای: {data['full_name']}")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='metric-box'><h4>💰 قیمت فروش</h4><h2>{data['price']:,} <small>ریال</small></h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-box'><h4>🏆 لیدر بازار</h4><h2>{data['leader']}</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-box'><h4>📍 قطب لیدر</h4><h2>{data['region_leader']}</h2></div>", unsafe_allow_html=True)

        # بخش نمودارهای Power BI
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.write("### 📊 تحلیل سهم بازار در مارکت‌های آنلاین")
            fig = px.bar(x=['سولیکو', 'لیدر فعلی', 'سایر رقبا'], 
                         y=[30, 45, 25], 
                         color=['سولیکو', 'لیدر', 'سایر'],
                         color_discrete_map={'سولیکو': '#ef394e', 'لیدر': '#333', 'سایر': '#ccc'},
                         title="نفوذ برند در اپلیکیشن‌های موبایل (Snap/Digi)")
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.write("### 💡 استراتژی افزایش سهم")
            st.markdown(f"<div class='strategy-card'>{data['strategy']}</div>", unsafe_allow_html=True)
            st.write(f"🌟 **محبوب در سوشیال:** {data['social_star']}")

        # گزارش لیدرها (بشارت، شام شام، ۲۰۲ و...)
        st.write("---")
        st.write("### 🏁 گزارش لیدرهای بازار به تفکیک شرکت و منطقه")
        report_df = pd.DataFrame({
            "دسته": ["پروتئینی Mass", "پروتئینی Premium", "سس ها", "تون ماهی و زیتون"],
            "لیدر آنلاین": ["سولیکو / گوشتیران", "آندره / ۲۰۲", "مهرام", "طبیعت"],
            "لیدر منطقه ای": ["جنوب (بشارت)", "تهران (۲۰۲)", "البرز (مهرام)", "شرق (تحفه)"],
            "وضعیت محبوبیت": ["کاله (بالا)", "آندره (بسیار بالا)", "بیژن (بالا)", "تحفه (متوسط)"]
        })
        st.table(report_df)
        
    else:
        st.warning("⚠️ محصول در لیست Feb-2026 یافت نشد. نام را دقیق‌تر وارد کنید.")
else:
    st.info("👆 منتظر جستجوی شما هستیم. لطفاً نام محصول را وارد کنید.")
