import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات صفحه
st.set_page_config(page_title="Solico Competitive Intelligence", layout="wide")

# طراحی UI مشابه داشبوردهای حرفه‌ای BI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .stApp { background-color: #f8f9fa; }
    .leader-box { background: #1e1e1e; color: #ffd700; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #ffd700; }
    .price-card { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 10px; border-right: 5px solid #ef394e; }
    .city-badge { background: #e1e1e1; color: #333; padding: 2px 8px; border-radius: 15px; font-size: 11px; margin-left: 5px; }
    </style>
""", unsafe_allow_html=True)

# ۱. دیتابیس جامع محصولات (بر اساس لیست ارسالی شما)
# توجه: قیمت‌ها به ریال هستند
PRODUCTS_DATA = [
    {"id": "30003108", "name": "کچاپ 300 گرمی", "category": "سس", "price": 1050000, "leader": "مهرام", "competitors": {"مهرام": 1100000, "دلپذیر": 1080000, "بیژن": 1020000}, "top_provinces": "تهران، اصفهان"},
    {"id": "101", "name": "مایونز پرچرب 900 گرمی", "category": "سس", "price": 4650000, "leader": "کاله (گاردن)", "competitors": {"مهرام": 4800000, "بیژن": 4550000, "بهروز": 4400000}, "top_provinces": "مازندران، گیلان"},
    {"id": "202", "name": "بیکن ایرلندی دارفرش", "category": "پروتئین", "price": 9820000, "leader": "سولیکو", "competitors": {"آندره": 10500000, "۲۰۲": 9200000}, "top_provinces": "تهران، البرز"},
    {"id": "303", "name": "زیتون پرورده 2000 گرمی", "category": "زیتون", "price": 9000000, "leader": "بدر", "competitors": {"کاله": 9200000, "اصالت": 8800000}, "top_provinces": "فارس، تهران"},
    {"id": "404", "name": "تن ماهی 400 گرمی", "category": "کنسرو", "price": 1699000, "leader": "طبیعت", "competitors": {"تحفه": 1750000, "شیلتون": 1680000}, "top_provinces": "خراسان، هرمزگان"}
]

# هدر برنامه
st.title("🛡️ مرکز پایش رقابتی سولیکو")
search_input = st.text_input("🔍 جستجو بر اساس کد کالا یا نام (مثلاً: 30003108 یا مایونز)...")

if search_input:
    # فیلتر کردن محصول
    found_item = next((item for item in PRODUCTS_DATA if search_input in item["id"] or search_input in item["name"]), None)
    
    if found_item:
        st.success(f"محصول یافت شد: {found_item['name']}")
        
        # بخش ۱: وضعیت لیدری و استانی
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="leader-box">🏆 لیدر این محصول<br><h3>{found_item["leader"]}</h3></div>', unsafe_allow_html=True)
        with col2:
            st.metric("سهم در مارکت", "لیدر بازار" if found_item["leader"] == "سولیکو" or "کاله" in found_item["leader"] else "در حال رقابت")
        with col3:
            st.write("**استان‌های قدرتمند:**")
            for city in found_item["top_provinces"].split("،"):
                st.markdown(f'<span class="city-badge">📍 {city}</span>', unsafe_allow_html=True)

        # بخش ۲: مقایسه قیمت رقبا (جدول و نمودار)
        st.write("---")
        st.subheader("💰 بنچ‌مارک قیمت رقبا (ریال)")
        
        # آماده‌سازی دیتا برای نمودار
        comp_data = found_item["competitors"].copy()
        comp_data["سولیکو (ما)"] = found_item["price"]
        df_comp = pd.DataFrame(list(comp_data.items()), columns=['برند', 'قیمت']).sort_values('قیمت')

        c_left, c_right = st.columns([1, 1])
        with c_left:
            fig = px.bar(df_comp, x='برند', y='قیمت', text='قیمت', color='برند',
                         color_discrete_map={"سولیکو (ما)": "#ef394e"},
                         title=f"مقایسه قیمتی در سطح بازار")
            st.plotly_chart(fig, use_container_width=True)
            
        with c_right:
            for brand, p in comp_data.items():
                is_us = "سولیکو" in brand
                st.markdown(f"""
                <div class="price-card" style="border-right-color: {'#ef394e' if is_us else '#333'};">
                    <div style="display:flex; justify-content:space-between;">
                        <span>{brand}</span>
                        <b style="color:{'#ef394e' if is_us else '#333'};">{p:,} ریال</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.error("کد کالا یا نام محصول در دیتابیس یافت نشد.")
else:
    st.info("لطفاً کد کالا (مثلاً 30003108) را وارد کنید تا تحلیل عمیق رقبا نمایش داده شود.")
