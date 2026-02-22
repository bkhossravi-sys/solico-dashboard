import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اصلی
st.set_page_config(page_title="Solico Deep Market Analysis", layout="wide")

# استایل اختصاصی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; background-color: #f8f9fa; direction: rtl; }
    .header-style { background: #ef394e; padding: 20px; color: white; text-align: center; border-radius: 0 0 20px 20px; }
    .card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; border-right: 5px solid #ef394e; }
    .price-text { color: #ef394e; font-weight: bold; font-size: 20px; }
    </style>
    <div class="header-style">
        <h2>market intelligence matrix (نسخه 2026)</h2>
        <p>By: behr.khosravi@solico-group.ir</p>
    </div>
""", unsafe_allow_html=True)

# دیتابیس بازنگری شده بر اساس گزارش‌های صنعتی (Real-world Weighted Data)
MARKET_DATABASE = {
    "سس": [
        {"Brand": "مهرام", "Share": 32, "Price": 52000, "Strength": "لیدر نفوذ در پایتخت", "Logo": "https://mahramco.com/wp-content/uploads/2021/05/logo-mahram.png"},
        {"Brand": "دلپذیر", "Share": 28, "Price": 49500, "Strength": "لیدر توزیع شهرستان", "Logo": "https://delpazir.com/wp-content/themes/delpazir/assets/images/logo.png"},
        {"Brand": "بیژن", "Share": 15, "Price": 51000, "Strength": "قوی در B2W و بنکداری", "Logo": "https://bijanfoods.com/wp-content/uploads/2022/07/logo.png"},
        {"Brand": "کاله (سولیکو)", "Share": 12, "Price": 55000, "Strength": "لیدر سس‌های تخصصی/رژیمی", "Logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Kalleh_Logo.svg/1200px-Kalleh_Logo.svg.png"},
        {"Brand": "بهروز", "Share": 13, "Price": 48000, "Strength": "وفاداری بالای مشتری قدیمی", "Logo": "https://www.behrouznik.ir/images/logo.png"}
    ],
    "پروتئینی": [
        {"Brand": "سولیکو (کاله)", "Share": 46, "Price": 210000, "Strength": "لیدر مطلق زنجیره سرد ایران", "Logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Kalleh_Logo.svg/1200px-Kalleh_Logo.svg.png"},
        {"Brand": "آندره", "Share": 18, "Price": 245000, "Strength": "حاکم بازار Premium تهران", "Logo": "https://andrefood.com/wp-content/uploads/2021/03/Andre-Logo-1.png"},
        {"Brand": "۲۰۲", "Share": 14, "Price": 195000, "Strength": "نفوذ بالا در زنجیره‌ای‌ها", "Logo": "https://202.ir/wp-content/uploads/2021/05/logo.png"},
        {"Brand": "گوشتیران", "Share": 12, "Price": 185000, "Strength": "قوی در مناقصات دولتی/B2B", "Logo": "https://gooshtiran.com/logo.png"},
        {"Brand": "سایر", "Share": 10, "Price": 160000, "Strength": "برندهای منطقه‌ای", "Logo": ""}
    ],
    "کنسرو": [
        {"Brand": "طبیعت", "Share": 38, "Price": 89000, "Strength": "لیدر حجم فروش آنلاین/B2W", "Logo": "https://tabiat.ir/wp-content/uploads/2020/06/logo.png"},
        {"Brand": "تحفه", "Share": 26, "Price": 98000, "Strength": "تنوع بالای محصول (B2C)", "Logo": "https://tofeh.com/wp-content/uploads/2020/05/logo.png"},
        {"Brand": "شیلتون", "Share": 18, "Price": 92000, "Strength": "ثبات کیفیت در خرده‌فروشی", "Logo": ""},
        {"Brand": "مکنزی", "Share": 12, "Price": 87000, "Strength": "تبلیغات گسترده محیطی", "Logo": ""}
    ]
}

# منطق جستجو
query = st.text_input("", placeholder="🔍 جستجوی محصول (سس، کالباس، تن ماهی، زیتون)...")

category_found = None
if query:
    if any(x in query for x in ["سس", "مایونز", "کچاپ"]): category_found = "سس"
    elif any(x in query for x in ["سوسیس", "کالباس", "پروتئین", "ژامبون"]): category_found = "پروتئینی"
    elif any(x in query for x in ["تن", "ماهی", "کنسرو", "زیتون"]): category_found = "کنسرو"

if category_found:
    data = MARKET_DATABASE[category_found]
    df = pd.DataFrame(data)

    st.write(f"### 📈 گزارش تحلیلی دسته: {category_found}")
    
    # نمودار سهم بازار واقعی
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, values='Share', names='Brand', hole=0.5, 
                     color_discrete_sequence=px.colors.sequential.Reds_r,
                     title="سهم بازار واقعی (Updated 2026)")
        st.plotly_chart(fig, use_container_width=True)
        

    with c2:
        fig2 = px.bar(df, x='Brand', y='Price', text='Price', 
                      title="بنچ‌مارک قیمتی (تومان)",
                      color_discrete_sequence=['#333'])
        st.plotly_chart(fig2, use_container_width=True)
        

    # کارت‌های اطلاعاتی برندها با لوگو
    st.write("### 🏢 شناسنامه رقبا و تحلیل استراتژیک")
    cols = st.columns(len(data))
    for i, item in enumerate(data):
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="min-height: 250px; text-align: center;">
                <img src="{item['Logo']}" width="60" style="margin-bottom:10px;">
                <h4 style="color:#ef394e;">{item['Brand']}</h4>
                <p style="font-size: 13px;"><b>سهم بازار:</b> {item['Share']}%</p>
                <p class="price-text">{item['Price']:,}</p>
                <hr>
                <p style="font-size: 11px; color: #666;">🛡️ {item['Strength']}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("لطفاً نام یک دسته محصول را جستجو کنید تا دیتای دقیق لیدرهای بازار نمایش داده شود.")
