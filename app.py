import streamlit as st

# تنظیمات اصلی
st.set_page_config(page_title="MIM Professional", layout="wide")

# استایل اختصاصی برای خوانایی حداکثری در موبایل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; background-color: #f0f2f5; color: #1a1a1a; }
    
    .header-card { background: #ffffff; padding: 20px; border-radius: 15px; border-bottom: 5px solid #ef394e; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; text-align: center; }
    
    .result-card { background: #ffffff; padding: 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #d1d5db; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    
    .brand-title { color: #111827; font-size: 20px; font-weight: bold; }
    .price-text { color: #d32f2f; font-size: 24px; font-weight: 800; display: block; margin-top: 5px; }
    .city-label { background: #e5e7eb; color: #374151; padding: 4px 12px; border-radius: 8px; font-size: 13px; font-weight: bold; }
    
    .gemini-analysis { background: #fff4f4; border-right: 6px solid #ef394e; padding: 15px; border-radius: 10px; margin-top: 20px; }
    .badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 12px; margin-bottom: 10px; font-weight: bold; }
    .badge-popular { background: #ffd700; color: #000; }
    .badge-design { background: #e1bee7; color: #4a148c; }
    </style>
""", unsafe_allow_html=True)

# هدر اپلیکیشن
st.markdown("""
    <div class="header-card">
        <span style="color: #ef394e; font-weight: bold; font-size: 12px; letter-spacing: 1px;">MARKET INTELLIGENCE MATRIX</span>
        <h2 style="margin: 5px 0; color: #1a1a1a;">سامانه پایش هوشمند بازار</h2>
    </div>
""", unsafe_allow_html=True)

# دیتابیس هوشمند (آپدیت اسفند ۱۴۰۴ بر اساس اسکرین‌شات‌ها)
DATABASE = {
    "سس": {
        "items": [
            {"name": "مهرام (۹۷۰ گرم)", "price": 520000, "city": "تهران", "share": 35, "popular": True, "design": False},
            {"name": "کاله (سولیکو)", "price": 485000, "city": "آمل / سراسری", "share": 13, "popular": False, "design": True},
            {"name": "دلپذیر", "price": 490000, "city": "مشهد", "share": 28, "popular": False, "design": False},
            {"name": "بیژن", "price": 510000, "city": "شیراز", "share": 15, "popular": False, "design": False}
        ],
        "gemini_insight": "برند مهرام با وجود قیمت بالاتر، به دلیل قدرت برندینگ (Popularity) همچنان سهم اول بازار را دارد، اما کاله با بسته‌بندی‌های مدرن (Best Design) در حال جذب نسل جوان است."
    }
}

# باکس جستجوی تمیز
query = st.text_input("🔍 نام محصول را وارد کنید:", placeholder="مثلاً: سس")

if query:
    target = None
    if "سس" in query: target = DATABASE["سس"]
    
    if target:
        st.markdown("### 🏆 نتایج تحلیل زنده")
        
        # نمایش کارت‌های محصول
        for item in target["items"]:
            pop_tag = '<span class="badge badge-popular">🌟 محبوب‌ترین برند بازار</span>' if item['popular'] else ''
            des_tag = '<span class="badge badge-design">🎨 زیباترین بسته‌بندی</span>' if item['design'] else ''
            
            st.markdown(f"""
                <div class="result-card">
                    {pop_tag} {des_tag}
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="brand-title">{item['name']}</span>
                        <span class="city-label">📍 {item['city']}</span>
                    </div>
                    <span class="price-text">{item['price']:,} تومان</span>
                    <div style="margin-top: 10px; font-size: 14px; color: #666;">
                        سهم بازار: <b>{item['share']}%</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        # بخش تحلیل کیفی جمینای
        st.markdown(f"""
            <div class="gemini-analysis">
                <b style="color: #ef394e;">💡 تحلیل استراتژیک جمینای:</b><br>
                <p style="margin-top: 8px; font-size: 15px; color: #333; line-height: 1.6;">{target['gemini_insight']}</p>
            </div>
        """, unsafe_allow_html=True)
        
    else:
        st.warning("داده‌ای برای این محصول یافت نشد. (فعلاً 'سس' را جستجو کنید)")
else:
    st.info("👆 لطفاً نام محصول را در کادر بالا بنویسید تا تحلیل بازار استخراج شود.")

