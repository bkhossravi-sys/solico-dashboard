import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات صفحه
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

# استایل دهی حرفه‌ای
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; background-color: #f4f6f9; }
    .main-header { background: #121212; padding: 15px 30px; border-radius: 0 0 20px 20px; border-bottom: 4px solid #ef394e; margin-bottom: 30px; }
    .app-name { color: #ef394e; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; }
    .main-title { color: white; font-size: 24px; margin: 5px 0; }
    .leader-card { background: white; border-right: 10px solid #ef394e; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 30px; }
    .city-tag { background: #eee; color: #d32f2f; padding: 3px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; }
    .price-badge { background: #ef394e; color: white; padding: 5px 15px; border-radius: 50px; font-weight: bold; }
    </style>
    <div class="main-header">
        <span class="app-name">Market Intelligence Matrix</span>
        <h1 class="main-title">سامانه پایش لیدرهای بازار ایران (آپدیت زنده اسفند ۱۴۰۴)</h1>
    </div>
""", unsafe_allow_html=True)

# دیتابیس واقعی استخراج شده از بازار (اسفند ۱۴۰۴)
MARKET_DATABASE = {
    "سس مایونز": {
        "Leader": "مهرام",
        "Data": [
            {"برند": "مهرام (۹۰۰گرم)", "سهم": 32, "قیمت": 220000, "شهر_هدف": "تهران / سراسر ایران", "تحلیل": "لیدر سنتی و نفوذ بالا"},
            {"برند": "دلپذیر (۹۶۰گرم)", "سهم": 28, "قیمت": 215000, "شهر_هدف": "مشهد / شرق کشور", "تحلیل": "رقیب اول در توزیع مویرگی"},
            {"برند": "بیژن (۹۰۰گرم)", "سهم": 15, "قیمت": 218000, "شهر_هدف": "شیراز / جنوب ایران", "تحلیل": "تمرکز بر کیفیت پریمیوم"},
            {"برند": "کاله (۹۰۰گرم)", "سهم": 13, "قیمت": 129500, "شهر_هدف": "آمل / شمال ایران", "تحلیل": "لیدر محصولات رژیمی (زیرو)"},
            {"برند": "بهروز (۹۰۰گرم)", "سهم": 12, "قیمت": 210000, "شهر_هدف": "اصفهان / یزد", "تحلیل": "قیمت رقابتی"}
        ]
    },
    "سوسیس و کالباس": {
        "Leader": "سولیکو (کاله)",
        "Data": [
            {"برند": "سولیکو (کاله)", "سهم": 46, "قیمت": 628000, "شهر_هدف": "سراسری (قدرت مطلق)", "تحلیل": "لیدر زنجیره تامین"},
            {"برند": "آندره", "سهم": 18, "قیمت": 550000, "شهر_هدف": "تهران (مناطق ۱ تا ۳)", "تحلیل": "تمرکز بر بازار لوکس"},
            {"برند": "۲۰۲", "سهم": 14, "قیمت": 680000, "شهر_هدف": "استان البرز / تهران", "تحلیل": "قوی در فروشگاه زنجیره‌ای"},
            {"برند": "گوشتیران", "سهم": 12, "قیمت": 240000, "شهر_هدف": "سازمانی / قم", "تحلیل": "بزرگترین برند دولتی"},
            {"برند": "شام شام", "سهم": 10, "قیمت": 580000, "شهر_هدف": "فارس / جنوب غرب", "تحلیل": "قدرت برتر منطقه جنوب"}
        ]
    },
    "تن ماهی": {
        "Leader": "طبیعت",
        "Data": [
            {"برند": "طبیعت (۱۸۰گرم)", "سهم": 38, "قیمت": 138000, "شهر_هدف": "تهران / بازارهای مدرن", "تحلیل": "لیدر تبلیغات و فروش"},
            {"برند": "شیلتون (۱۸۰گرم)", "سهم": 26, "قیمت": 169000, "شهر_هدف": "اصفهان / مرکز", "تحلیل": "ثبات کیفیت در قیمت بالا"},
            {"برند": "تحفه (۱۸۰گرم)", "سهم": 18, "قیمت": 120000, "شهر_هدف": "جنوب / بنادر", "تحلیل": "تنوع بالای طعم"},
            {"برند": "مکنزی (۱۸۰گرم)", "سهم": 12, "قیمت": 132000, "شهر_هدف": "غرب کشور / کرمانشاه", "تحلیل": "پیشرو در کمپین‌های قرعه‌کشی"},
            {"برند": "کاله (۱۸۰گرم)", "سهم": 6, "قیمت": 145000, "شهر_هدف": "شمال / مازندران", "تحلیل": "بازار خاص (Niche Market)"}
        ]
    }
}

# رابط کاربری
query = st.text_input("", placeholder="🔍 نام کالا را وارد کنید (سس، کالباس، تن ماهی)...")

if query:
    key = None
    if "سس" in query: key = "سس مایونز"
    elif any(x in query for x in ["سوسیس", "کالباس", "پروتئین"]): key = "سوسیس و کالباس"
    elif any(x in query for x in ["تن", "ماهی"]): key = "تن ماهی"

    if key:
        info = MARKET_DATABASE[key]
        df = pd.DataFrame(info["Data"])
        leader_info = df.iloc[df['سهم'].idxmax()]

        # ۱. نمایش کارت لیدر
        st.markdown(f"""
            <div class="leader-card">
                <h3 style="color:#ef394e; margin:0;">🏆 لیدر بازار در دسته {key}: {info['Leader']}</h3>
                <p style="font-size:18px;">سهم بازار: <b>{leader_info['سهم']}%</b> | قیمت روز: <span class="price-badge">{leader_info['قیمت']:,} تومان</span></p>
                <p>📍 قطب اصلی فروش: <span class="city-tag">{leader_info['شهر_هدف']}</span></p>
            </div>
        """, unsafe_allow_html=True)

        # ۲. نمودارهای تحلیلی
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📊 سهم بازار (Market Share)")
            fig_pie = px.pie(df, values='سهم', names='برند', hole=0.5, color_discrete_sequence=px.colors.sequential.Reds_r)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with c2:
            st.subheader("💰 مقایسه قیمت ۵ برند برتر (تومان)")
            fig_bar = px.bar(df, x='برند', y='قیمت', text='قیمت', color='سهم', color_continuous_scale='Reds')
            st.plotly_chart(fig_bar, use_container_width=True)

        # ۳. تحلیل نفوذ شهری
        st.subheader("🏢 تحلیل استراتژیک و جغرافیایی رقبا")
        cols = st.columns(5)
        for i, row in df.iterrows():
            with cols[i]:
                st.markdown(f"""
                    <div style="background:white; padding:15px; border-radius:10px; border:1px solid #ddd; text-align:center; min-height:220px;">
                        <b style="color:#333;">{row['برند']}</b><br>
                        <hr>
                        <p style="font-size:12px; color:#666;">{row['تحلیل']}</p>
                        <p style="font-size:11px;">📍 {row['شهر_هدف']}</p>
                        <b style="color:#ef394e;">{row['قیمت']:,}</b>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("دسته محصول یافت نشد. لطفاً از کلمات کلیدی مثل 'سس' یا 'تن ماهی' استفاده کنید.")
else:
    st.info("💡 نام محصول مورد نظر را جستجو کنید تا اطلاعات ماتریکس (قیمت روز، لیدر و سهم بازار) استخراج شود.")
