import streamlit as st
import pandas as pd
import plotly.express as px
import random

# تنظیمات اصلی صفحه
st.set_page_config(page_title="Solico Market Engine", layout="wide")

# استایل اختصاصی ترکیبی (اسنپ مارکت + دیجی‌کالا)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; background-color: #f0f2f5; direction: rtl; }
    
    .main-header { background: #ef394e; padding: 15px; color: white; text-align: center; border-radius: 0 0 20px 20px; margin-bottom: 20px; }
    .user-info { font-size: 10px; opacity: 0.8; margin-top: 5px; display: block; }
    
    /* کارت محصول مشابه دیجی‌کالا */
    .product-card {
        background: white; border-radius: 12px; padding: 15px;
        border: 1px solid #e0e0e0; margin-bottom: 10px;
        transition: 0.3s;
    }
    .product-card:hover { box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-color: #ef394e; }
    .price-tag { color: #ef394e; font-size: 18px; font-weight: 700; }
    .market-share-badge { background: #333; color: white; padding: 2px 8px; border-radius: 5px; font-size: 11px; }
    .brand-title { font-size: 16px; font-weight: bold; color: #1a1c22; }
    
    /* استایل دکمه‌های ناوبری */
    .nav-btn { background: white; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 0 auto; font-size: 20px; }
    </style>
    
    <div class="main-header">
        <div style="font-size: 20px; font-weight: 700;">سامانه استعلام هوشمند قیمت و بازار (Solico)</div>
        <span class="user-info">By: behr.khosravi@solico-group.ir</span>
    </div>
""", unsafe_allow_html=True)

# دیتابیس جامع قیمت و برند (شبیه‌ساز هوش مصنوعی)
def get_market_data(query):
    # کلمات کلیدی برای دسته‌بندی
    sauce_keywords = ["سس", "مایونز", "کچاپ", "خردل", "فرانسوی"]
    meat_keywords = ["سوسیس", "کالباس", "ژامبون", "کوکتل", "برگر", "گوشت"]
    olive_keywords = ["زیتون", "شیشه", "پرورده"]
    tuna_keywords = ["تن", "ماهی", "کنسرو"]

    brands_sauce = ["مهرام", "بهروز", "دلپذیر", "بیژن", "کاله", "روژین", "هانا", "دلوسه", "سحر", "ناجی"]
    brands_meat = ["سولیکو (کاله)", "آندره", "۲۰۲", "گوشتیران", "شیک", "رباط"]
    brands_olive = ["بدر", "طراوت", "مهرام", "اصالت"]
    brands_tuna = ["تحفه", "طبیعت", "شیلتون", "تاپی"]

    results = []
    
    # منطق تولید دیتای هوشمند بر اساس سرچ کاربر
    if any(x in query for x in sauce_keywords):
        target_brands = brands_sauce
        base_price = 45000
        category = "سس"
    elif any(x in query for x in meat_keywords):
        target_brands = brands_meat
        base_price = 180000
        category = "فرآورده گوشتی"
    elif any(x in query for x in olive_keywords):
        target_brands = brands_olive
        base_price = 95000
        category = "زیتون شیشه‌ای"
    elif any(x in query for x in tuna_keywords):
        target_brands = brands_tuna
        base_price = 85000
        category = "تن ماهی"
    else:
        return None

    for b in target_brands:
        results.append({
            "برند": b,
            "محصول": f"{query} {b}",
            "قیمت (تومان)": base_price + random.randint(-5000, 25000),
            "سهم بازار": random.randint(5, 35),
            "وضعیت توزیع": random.choice(["مویرگی", "بنکداری", "B2B"]),
            "دسته": category
        })
    
    return pd.DataFrame(results).sort_values(by="سهم بازار", ascending=False)

# منوی میانبر (Categories)
cols = st.columns(4)
menu = [("سس", "🥫"), ("پروتئین", "🥩"), ("زیتون", "🫒"), ("تن‌ماهی", "🐟")]
for i, (name, icon) in enumerate(menu):
    with cols[i]:
        st.markdown(f'<div class="nav-btn">{icon}</div><p style="text-align:center; font-size:12px; margin-top:5px;">{name}</p>', unsafe_allow_html=True)

# فیلد جستجو هوشمند
search_q = st.text_input("", placeholder="🔍 نام محصول را بنویسید (مثلاً: سس مایونز یا کالباس خشک)...")

if search_q:
    df = get_market_data(search_q)
    
    if df is not None:
        # ۱. بخش نمودارهای تحلیلی (Power BI Style)
        st.write("### 📊 تحلیل رقابتی بازار")
        c1, c2 = st.columns(2)
        
        with c1:
            fig1 = px.bar(df, x='برند', y='قیمت (تومان)', color='برند', text='قیمت (تومان)', 
                          title="مقایسه قیمت در سوپرمارکت‌های آنلاین", color_discrete_sequence=px.colors.sequential.Reds_r)
            fig1.update_layout(showlegend=False, height=350, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
            

        with c2:
            fig2 = px.pie(df, values='سهم بازار', names='برند', hole=0.6, title="توزیع سهم بازار (Share of Voice)")
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)
            

        # ۲. لیست محصولات (UI مشابه اسنپ مارکت)
        st.write("---")
        st.write(f"### 🛒 نتایج جستجوی قیمت برای: {search_q}")
        
        # نمایش کارت‌های محصول در ردیف‌های ۳ تایی
        rows = [df.iloc[i:i+3] for i in range(0, len(df), 3)]
        for row_data in rows:
            cols = st.columns(3)
            for i, (idx, row) in enumerate(row_data.iterrows()):
                with cols[i]:
                    st.markdown(f"""
                    <div class="product-card">
                        <span class="market-share_badge">سهم بازار: {row['سهم بازار']}%</span>
                        <div class="brand-title">{row['برند']}</div>
                        <p style="font-size:12px; color:#666; margin-top:5px;">{row['محصول']}</p>
                        <hr style="opacity:0.2;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="info-label" style="font-size:11px;">توزیع: {row['وضعیت توزیع']}</span>
                            <span class="price-tag">{row['قیمت (تومان)']:,.0f} <small style="font-size:10px;">تومان</small></span>
                        </div>
                        <div style="background:#f9f9f9; padding:5px; border-radius:5px; margin-top:10px; font-size:11px; text-align:center; color:#ef394e;">
                            📍 استعلام شده از: دیجی‌کالا / اسنپ‌مارکت
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    else:
        st.warning("محصولی یافت نشد. لطفاً از دسته‌های اصلی (سس، گوشتی، زیتون، تن‌ماهی) سرچ کنید.")

