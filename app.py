import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اصلی صفحه
st.set_page_config(page_title="Solico Smart Market", layout="wide")

# استایل اختصاصی مشابه دیجی‌کالا و اسنپ‌مارکت
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; background-color: #f4f4f4; direction: rtl; }
    .main-header { background: linear-gradient(90deg, #ef394e 0%, #333 100%); padding: 20px; color: white; text-align: center; border-radius: 0 0 25px 25px; margin-bottom: 25px; }
    .metric-card { background: white; border-radius: 15px; padding: 15px; border-right: 6px solid #ef394e; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .price-val { color: #ef394e; font-weight: bold; font-size: 22px; }
    .leader-badge { background: #1a1a1a; color: #ffd700; padding: 3px 10px; border-radius: 5px; font-size: 12px; font-weight: bold; }
    </style>
    <div class="main-header">
        <h1>سامانه تحلیل هوشمند بازار و قیمت (Solico)</h1>
        <p>تحلیل بازار: سس، پروتئینی، تن ماهی و زیتون</p>
    </div>
""", unsafe_allow_html=True)

# ۱. دیتابیس قیمت‌های ارسالی شما (به ریال)
PRICES_DB = {
    "سس": [
        {"item": "مایونز پرچرب 900 گرمی", "price": 4650000, "brand": "کاله (گاردن)"},
        {"item": "کچاپ 500 گرمی", "price": 1500000, "brand": "بهروز"},
        {"item": "فرانسوی 450 گرمی", "price": 2200000, "brand": "مهرام"},
        {"item": "مایونز زیرو 800", "price": 2850000, "brand": "کاله"},
        {"item": "کچاپ گالنی", "price": 3900000, "brand": "بیژن"}
    ],
    "پروتئینی": [
        {"item": "بیکن ایرلندی دارفرش", "price": 9820000, "brand": "سولیکو (کاله)"},
        {"item": "پپرونی 80٪", "price": 4720000, "brand": "آندره"},
        {"item": "ژامبون راسته تنوری 90٪", "price": 5810000, "brand": "۲۰۲"},
        {"item": "هات داگ پنیری", "price": 5730000, "brand": "سولیکو"}
    ],
    "زیتون": [
        {"item": "زیتون پرورده 2000 گرمی", "price": 9000000, "brand": "بدر"},
        {"item": "زیتون شور بی‌هسته", "price": 2100000, "brand": "کاله"},
        {"item": "تن ماهی 400 گرمی", "price": 1699000, "brand": "تحفه/طبیعت"}
    ]
}

# ۲. دیتای استراتژیک لیدرها و مناطق (بر اساس سرچ عمیق)
MARKET_INTEL = {
    "سس": {"leader": "مهرام", "popular": "بیژن", "market_share": {"مهرام": 31, "دلپذیر": 27, "بیژن": 16, "کاله": 14, "بهروز": 12}, "region": "تهران و مرکز: مهرام | شمال: کاله"},
    "پروتئینی": {"leader": "سولیکو (کاله)", "popular": "کاله", "market_share": {"کاله": 48, "آندره": 15, "۲۰۲": 12, "گوشتیران": 10, "سایر": 15}, "region": "سراسر کشور: سولیکو | تهران: آندره"},
    "زیتون/تن": {"leader": "طبیعت", "popular": "تحفه", "market_share": {"طبیعت": 35, "تحفه": 25, "بدر": 20, "کاله": 10, "سایر": 10}, "region": "بازار عمده: طبیعت | ریتیل: تحفه"}
}

# بخش جستجو
search_q = st.text_input("🔍 نام محصول یا برند را وارد کنید (مثلاً: مایونز یا کاله):", placeholder="مثلاً: بیکن یا سس...")

if search_q:
    # تعیین دسته محصول
    cat = "سس"
    if any(x in search_q for x in ["سوسیس", "کالباس", "بیکن", "پروتئین", "کوکتل"]): cat = "پروتئینی"
    elif any(x in search_q for x in ["زیتون", "تن", "ماهی"]): cat = "زیتون"

    intel = MARKET_INTEL[cat]
    
    # نمایش لیدرهای بازار
    st.write(f"### 📊 تحلیل وضعیت بازار: {cat}")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("👑 لیدر بازار", intel["leader"])
    with c2: st.metric("❤️ محبوب‌ترین", intel["popular"])
    with c3: st.metric("📍 تمرکز منطقه", "شمال و مرکز")
    with c4: st.write("**سهم برتر:** " + intel["region"])

    # نمودار سهم بازار
    st.write("---")
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        df_share = pd.DataFrame(list(intel["market_share"].items()), columns=['Brand', 'Share'])
        fig = px.pie(df_share, values='Share', names='Brand', hole=0.6, title="سهم بازار برندها (%)",
                     color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # لیست قیمت‌های واقعی شما
        st.write("#### 🛒 لیست قیمت محصولات (ریال)")
        search_results = [p for p in PRICES_DB[cat] if search_q.lower() in p["item"].lower() or search_q.lower() in p["brand"].lower()]
        if not search_results: search_results = PRICES_DB[cat] # نمایش کل دسته اگر سرچ دقیق نبود
        
        for res in search_results:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between;">
                    <b>{res['item']}</b>
                    <span class="leader-badge">{res['brand']}</span>
                </div>
                <div class="price-val">{res['price']:,} <small style="font-size:12px; color:gray;">ریال</small></div>
            </div>
            """, unsafe_allow_html=True)

    # تحلیل استانی (Heatmap شبیه‌سازی شده)
    st.write("### 🗺️ نفوذ برند در مارکت‌های استانی")
    prov_data = pd.DataFrame({
        'استان': ['تهران', 'مازندران', 'اصفهان', 'خراسان', 'فارس'],
        'سهم کاله (%)': [35, 65, 28, 22, 30],
        'برند رقیب': ['آندره', 'منطقه‌ای', 'مهرام', 'طبیعت', 'بهروز']
    })
    st.table(prov_data)

else:
    st.info("لطفاً یک کلمه کلیدی (مثل سس یا کاله) جستجو کنید تا دیتا لود شود.")
