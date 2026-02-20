import streamlit as st
import pandas as pd
import plotly.express as px

# 1. تنظیمات اولیه صفحه
st.set_page_config(page_title="Solico Super App", layout="wide")

# 2. استایل بصری (دیجی کالا + پاور بی‌آی)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; background-color: #f4f4f4; direction: rtl; }
    
    /* هدر قرمز دیجی‌کالا */
    .main-header {
        background: linear-gradient(90deg, #ef394e 0%, #c1121f 100%);
        padding: 25px; color: white; text-align: center;
        border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .email-tag { font-size: 12px; opacity: 0.8; font-weight: 100; margin-top: 5px; display: block; }
    
    /* کارت‌های شناسنامه برند - بسیار خوانا */
    .brand-card {
        background: white; border-radius: 20px; padding: 20px;
        border: 1px solid #eee; margin-bottom: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .info-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f9f9f9; }
    .label { color: #666; font-size: 14px; }
    .value { color: #000; font-weight: 700; font-size: 16px; }
    
    /* آیکون‌های گرد دسته‌بندی */
    .cat-circle {
        width: 65px; height: 65px; background: white; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto; border: 2px solid #ef394e; font-size: 28px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    
    <div class="main-header">
        <div style="font-size: 24px; font-weight: 700;">هوش تجاری گروه سولیکو</div>
        <span class="email-tag">By: behr.khosravi@solico-group.ir</span>
    </div>
""", unsafe_allow_html=True)

# 3. دیتابیس لوگوها
LOGOS = {
    "کاله": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Kalleh_Logo.svg/1200px-Kalleh_Logo.svg.png",
    "مهرام": "https://mahramco.com/wp-content/uploads/2021/05/logo-mahram.png",
    "دلپذیر": "https://delpazir.com/wp-content/themes/delpazir/assets/images/logo.png",
    "آندره": "https://andrefood.com/wp-content/uploads/2021/03/Andre-Logo-1.png",
    "طبیعت": "https://tabiat.ir/wp-content/uploads/2020/06/logo.png"
}

# 4. تابع دریافت دیتا (بدون خطا)
def get_data(search_term):
    s = search_term.strip()
    if any(x in s for x in ["سس", "مایونز", "کچاپ"]):
        return pd.DataFrame([
            {'Brand': 'مهرام', 'Share': 35, 'City': 'تهران', 'B2B': 'بسیار فعال', 'B2W': 'مویرگی'},
            {'Brand': 'دلپذیر', 'Share': 32, 'City': 'سراسری', 'B2B': 'متوسط', 'B2W': 'بنکداری'},
            {'Brand': 'کاله', 'Share': 18, 'City': 'آمل', 'B2B': 'تخصصی کترینگ', 'B2W': 'سیستمی'}
        ]), "💡 استراتژی: تمرکز بر سس‌های تک‌نفره برای بخش رستورانی."
    elif any(x in s for x in ["سوسیس", "کالباس", "کوکتل"]):
        return pd.DataFrame([
            {'Brand': 'کاله', 'Share': 45, 'City': 'کشوری', 'B2B': 'لیدر اصلی', 'B2W': 'هوشمند'},
            {'Brand': 'آندره', 'Share': 25, 'City': 'تهران', 'B2B': 'لوکس', 'B2W': 'محدود'}
        ]), "💡 استراتژی: توسعه محصولات سوجوک در مناطق غرب تهران."
    return None, None

# 5. بخش آیکون‌های گرد (Categories)
st.write(" ")
c1, c2, c3, c4 = st.columns(4)
items = [("سس", "🥫"), ("گوشتی", "🥩"), ("کنسرو", "🐟"), ("لبنیات", "🥛")]
cols = [c1, c2, c3, c4]
for i, (name, icon) in enumerate(items):
    with cols[i]:
        st.markdown(f'<div class="cat-circle">{icon}</div><p style="text-align:center; font-weight:bold; margin-top:8px;">{name}</p>', unsafe_allow_html=True)

# 6. کادر جستجو
query = st.text_input("", placeholder="🔍 نام محصول را اینجا بنویسید (مثلاً: سس یا کوکتل)")

if query:
    df, strategy = get_data(query)
    if df is not None:
        # نمایش استراتژی
        st.success(strategy)
        
        # نمودار دایره‌ای (Power BI Style)
        st.write("### 📊 سهم بازار")
        fig = px.pie(df, values='Share', names='Brand', hole=0.5, color_discrete_sequence=['#ef394e', '#333', '#777'])
        fig.update_layout(showlegend=True, height=350)
        st.plotly_chart(fig, use_container_width=True)
                
        # شناسنامه برندها (بسیار خوانا)
        st.write("### 🏢 جزئیات عملیاتی برندها")
        for _, row in df.iterrows():
            logo = LOGOS.get(row['Brand'], "https://via.placeholder.com/100")
            st.markdown(f"""
            <div class="brand-card">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <img src="{logo}" width="60">
                    <h2 style="margin-right:15px; color:#ef394e;">{row['Brand']}</h2>
                </div>
                <div class="info-row"><span class="label">📍 شهر لیدر:</span><span class="value">{row['City']}</span></div>
                <div class="info-row"><span class="label">🏢 وضعیت B2B:</span><span class="value">{row['B2B']}</span></div>
                <div class="info-row"><span class="label">🚚 وضعیت B2W:</span><span class="value">{row['B2W']}</span></div>
                <div class="info-row"><span class="label">📈 سهم بازار:</span><span class="value">{row['Share']}%</span></div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("محصول مورد نظر یافت نشد. کلماتی مثل 'سس' یا 'کوکتل' را امتحان کنید.")
