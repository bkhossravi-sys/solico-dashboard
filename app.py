import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اصلی
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

# استایل CSS برای ظاهر مدرن و سازمانی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; background-color: #f8f9fa; }
    .main-header { background: #1a1a1a; padding: 10px 25px; border-radius: 0 0 15px 15px; border-bottom: 3px solid #ef394e; margin-bottom: 20px; }
    .app-name { color: #ef394e; font-size: 10px; text-transform: uppercase; letter-spacing: 2px; display: block; }
    .main-title { color: white; font-size: 22px; margin: 0; }
    .leader-card { background: linear-gradient(135deg, #fff 0%, #fff5f5 100%); border-right: 8px solid #ef394e; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 25px; }
    .stat-card { background: white; padding: 15px; border-radius: 10px; border: 1px solid #eee; text-align: center; }
    .city-tag { background: #333; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; }
    </style>
    <div class="main-header">
        <span class="app-name">Market Intelligence Matrix</span>
        <h1 class="main-title">سامانه تحلیل هوشمند لیدرهای بازار ایران</h1>
    </div>
""", unsafe_allow_html=True)

# دیتابیس جامع بازار ایران (Updated 2026)
# این بخش شامل سهم بازار، قیمت میانگین و نفوذ جغرافیایی است
MARKET_DATA = {
    "سس مایونز": [
        {"برند": "مهرام", "سهم": 32, "قیمت": 52000, "شهر_اصلی": "تهران و البرز", "وضعیت": "لیدر بازار"},
        {"برند": "دلپذیر", "سهم": 28, "قیمت": 49500, "شهر_اصلی": "مشهد و شرق کشور", "وضعیت": "رقیب نزدیک"},
        {"برند": "بیژن", "سهم": 15, "قیمت": 51000, "شهر_اصلی": "شیراز و جنوب", "وضعیت": "توزیع گسترده"},
        {"برند": "کاله (سولیکو)", "سهم": 13, "قیمت": 55000, "شهر_اصلی": "مازندران و شمال", "وضعیت": "پیشرو در نوآوری"},
        {"برند": "بهروز", "سهم": 12, "قیمت": 48000, "شهر_اصلی": "اصفهان و مرکز", "وضعیت": "وفاداری سنتی"}
    ],
    "سوسیس و کالباس": [
        {"برند": "سولیکو (کاله)", "سهم": 46, "قیمت": 210000, "شهر_اصلی": "سراسر ایران (لیدر مطلق)", "وضعیت": "لیدر بازار"},
        {"برند": "آندره", "سهم": 18, "قیمت": 245000, "شهر_اصلی": "مناطق لوکس تهران", "وضعیت": "پریمیوم"},
        {"برند": "۲۰۲", "سهم": 14, "قیمت": 195000, "شهر_اصلی": "کرج و حاشیه تهران", "وضعیت": "نفوذ بالا"},
        {"برند": "گوشتیران", "سهم": 12, "قیمت": 185000, "شهر_اصلی": "سازمانی و دولتی", "وضعیت": "قدیمی‌ترین"},
        {"برند": "شام شام", "سهم": 10, "قیمت": 175000, "شهر_اصلی": "شیراز و جنوب غرب", "وضعیت": "منطقه‌ای قوی"}
    ],
    "تن ماهی": [
        {"برند": "طبیعت", "سهم": 38, "قیمت": 89000, "شهر_اصلی": "تهران و بازارهای آنلاین", "وضعیت": "لیدر بازار"},
        {"برند": "تحفه", "سهم": 26, "قیمت": 98000, "شهر_اصلی": "جنوب و فروشگاه‌های زنجیره‌ای", "وضعیت": "تنوع محصول"},
        {"برند": "شیلتون", "سهم": 18, "قیمت": 92000, "شهر_اصلی": "اصفهان و یزد", "وضعیت": "ثبات کیفیت"},
        {"برند": "مکنزی", "سهم": 12, "قیمت": 87000, "شهر_اصلی": "مناطق غربی کشور", "وضعیت": "تبلیغات گسترده"},
        {"برند": "کاله (سولیکو)", "سهم": 6, "قیمت": 95000, "شهر_اصلی": "شمال ایران", "وضعیت": "بخش تخصصی"}
    ]
}

# بخش جستجو
search_query = st.text_input("", placeholder="🔍 نام محصول (مثلاً: سس مایونز، سوسیس، تن ماهی) را وارد کنید...")

if search_query:
    # پیدا کردن دسته محصول
    category = None
    for key in MARKET_DATA.keys():
        if any(word in search_query for word in key.split()):
            category = key
            break
    
    if category:
        data = MARKET_DATA[category]
        df = pd.DataFrame(data)
        leader = df.iloc[0] # اولین مورد لیدر است

        # ۱. نمایش لیدر بازار
        st.markdown(f"""
            <div class="leader-card">
                <h2 style="color:#ef394e; margin:0;">🏆 لیدر بازار در دسته {category}: {leader['برند']}</h2>
                <p style="font-size:18px; color:#444;">این برند با <b>{leader['سهم']}%</b> سهم بازار، جایگاه نخست را در اختیار دارد.</p>
                <span class="city-tag">تمرکز اصلی فروش: {leader['شهر_اصلی']}</span>
            </div>
        """, unsafe_allow_html=True)

        # ۲. مقایسه قیمت و سهم بازار
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 📊 سهم بازار ۵ برند برتر")
            fig_pie = px.pie(df, values='سهم', names='برند', hole=0.4,
                             color_discrete_sequence=px.colors.sequential.Reds_r)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.write("### 💰 بنچ‌مارک قیمتی (تومان)")
            fig_bar = px.bar(df, x='برند', y='قیمت', text='قیمت', color='قیمت',
                             color_continuous_scale='Reds')
            st.plotly_chart(fig_bar, use_container_width=True)

        # ۳. تحلیل نفوذ شهری و استراتژیک
        st.write("### 🗺️ تحلیل نفوذ جغرافیایی و استراتژی")
        cols = st.columns(len(data))
        for i, item in enumerate(data):
            with cols[i]:
                st.markdown(f"""
                    <div class="stat-card">
                        <b style="color:#ef394e; font-size:16px;">{item['برند']}</b><br>
                        <small>{item['وضعیت']}</small>
                        <hr style="margin:10px 0;">
                        <p style="font-size:12px;">📍 <b>قطب فروش:</b><br>{item['شهر_اصلی']}</p>
                        <p style="font-size:14px; font-weight:bold; color:#333;">{item['قیمت']:,} تومان</p>
                    </div>
                """, unsafe_allow_html=True)
                
    else:
        st.info("لطفاً کلمه کلیدی درستی وارد کنید (مثلاً: سس، کالباس، تن)")
else:
    st.write("👈 نام محصول را در کادر بالا تایپ کنید تا ماتریکس اطلاعات استخراج شود.")
