import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اصلی
st.set_page_config(page_title="Solico Market Intelligence", layout="wide")

# استایل اختصاصی (ترکیب دیجی‌کالا و اسنپ)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; background-color: #f5f5f5; direction: rtl; }
    
    /* هدر اپلیکیشنی */
    .app-header {
        background: #ef394e; padding: 20px; color: white; text-align: center;
        border-radius: 0 0 25px 25px; box-shadow: 0 4px 12px rgba(239, 57, 78, 0.2);
    }
    
    /* کارت‌های اسنپی */
    .factory-card {
        background: white; border-radius: 15px; padding: 18px;
        border-right: 6px solid #ef394e; margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .brand-name { color: #ef394e; font-size: 20px; font-weight: 700; margin-bottom: 8px; }
    .contact-info { font-size: 13px; color: #555; line-height: 1.6; }
    .badge { background: #fceef0; color: #ef394e; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: bold; }
    
    /* آیکون‌های گرد بالای صفحه */
    .top-nav { display: flex; justify-content: space-around; padding: 15px 0; background: white; margin-bottom: 20px; border-radius: 0 0 15px 15px; }
    .nav-item { text-align: center; width: 70px; }
    .nav-icon { width: 50px; height: 50px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; border: 1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.05); font-size: 24px; }
    </style>

    <div class="app-header">
        <div style="font-size: 22px; font-weight: 700;">سولیکو - داشبورد هوشمند بازار</div>
        <div style="font-size: 11px; opacity: 0.9;">Market Intelligence Hub | 2026 Edition</div>
    </div>
""", unsafe_allow_html=True)

# دیتابیس جامع سس و فرآورده‌های گوشتی
DATA = [
    # سس‌ها (بر اساس متن ارسالی شما)
    {"Category": "سس", "Brand": "بهروز", "Share": 15, "City": "تهران (کیلومتر 8 لشگری)", "Tel": "02144536090", "Status": "تمام اتوماتیک", "Web": "behrouznik.ir"},
    {"Category": "سس", "Brand": "بیژن", "Share": 18, "City": "تهران (میدان آرژانتین)", "Tel": "02161966", "Status": "توزیع مویرگی برتر", "Web": "bijanfood.com"},
    {"Category": "سس", "Brand": "دلپذیر (کدبانو)", "Share": 32, "City": "کرج (جاده قدیم)", "Tel": "02161939802", "Status": "رهبر بازار کچاپ", "Web": "delpazirfood.com"},
    {"Category": "سس", "Brand": "مهرام", "Share": 28, "City": "تهران (خیابان مطهری)", "Tel": "02187700078", "Status": "تنوع محصول بالا", "Web": "mahramco.com"},
    {"Category": "سس", "Brand": "کاله", "Share": 12, "City": "آمل / تهران", "Tel": "02166454511", "Status": "نوآور در طعم", "Web": "kalleh.com"},
    {"Category": "سس", "Brand": "روژین", "Share": 8, "City": "تهران (پاسداران)", "Tel": "02122888890", "Status": "ارگانیک و سلامت", "Web": "rojintaak.com"},
    
    # پروتئینی (بر اساس تحلیل هوشمند بازار ۱۴۰۴/۱۴۰۵)
    {"Category": "گوشتی", "Brand": "سولیکو (کاله)", "Share": 42, "City": "سراسری", "Tel": "0216133", "Status": "رهبر مطلق بازار", "Web": "solico-group.ir"},
    {"Category": "گوشتی", "Brand": "آندره", "Share": 22, "City": "تهران (جاده مخصوص)", "Tel": "02144908249", "Status": "بخش لوکس و HoReCa", "Web": "andre.shop"},
    {"Category": "گوشتی", "Brand": "۲۰۲", "Share": 15, "City": "کرج (چهارباغ)", "Tel": "02144908249", "Status": "قوی در فروشگاه زنجیره‌ای", "Web": "202.ir"},
    {"Category": "گوشتی", "Brand": "گوشتیران", "Share": 10, "City": "تهران (جاده قدیم)", "Tel": "02166804000", "Status": "قدیمی‌ترین برند", "Web": "gooshtiran.com"}
]

df = pd.DataFrame(DATA)

# بخش آیکون‌های گرد (Top Nav)
st.markdown("""
<div class="top-nav">
    <div class="nav-item"><div class="nav-icon">🥫</div><div style="font-size:11px;">سس</div></div>
    <div class="nav-item"><div class="nav-icon">🥩</div><div style="font-size:11px;">پروتئین</div></div>
    <div class="nav-item"><div class="nav-icon">🐟</div><div style="font-size:11px;">کنسرو</div></div>
    <div class="nav-item"><div class="nav-icon">🥛</div><div style="font-size:11px;">لبنیات</div></div>
</div>
""", unsafe_allow_html=True)

# جستجو
search = st.text_input("", placeholder="🔍 نام برند یا محصول را جستجو کنید (مثلاً: کاله یا بیژن)")

# فیلتر کردن دیتا
filtered_df = df[df['Brand'].str.contains(search) | df['Category'].str.contains(search)] if search else df

if not filtered_df.empty:
    # بخش نمودار (Power BI Style)
    st.subheader("📊 سهم بازار (Market Share)")
    fig = px.bar(filtered_df, x='Brand', y='Share', color='Category', 
                 color_discrete_map={'سس': '#ef394e', 'گوشتی': '#333'},
                 text='Share')
    fig.update_layout(height=300, margin=dict(t=10, b=10), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    # بخش کارت‌های اطلاعاتی (خوانایی بالا)
    st.write("---")
    st.subheader("🏢 اطلاعات کارخانجات و تماس")
    
    for i, row in filtered_df.iterrows():
        st.markdown(f"""
        <div class="factory-card">
            <div style="display:flex; justify-content:space-between;">
                <span class="brand-name">{row['Brand']}</span>
                <span class="badge">{row['Category']}</span>
            </div>
            <div class="contact-info">
                <b>📍 آدرس:</b> {row['City']}<br>
                <b>📞 تلفن:</b> {row['Tel']}<br>
                <b>🌐 وب‌سایت:</b> {row['Web']}<br>
                <p style="color:#ef394e; font-weight:bold; margin-top:10px;">🛡️ وضعیت استراتژیک: {row['Status']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("برندی با این نام یافت نشد.")
