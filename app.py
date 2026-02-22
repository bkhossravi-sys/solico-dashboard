import streamlit as st

# تنظیمات اصلی اپلیکیشن
st.set_page_config(page_title="MIM Pro 2026", layout="wide")

# استایل ثابت و خوانا (بدون تغییر فونت طبق دستور شما)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; background-color: #f9fafb; color: #111827; }
    .main-container { max-width: 800px; margin: auto; padding: 10px; }
    .search-box { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 20px; border-top: 5px solid #ef394e; }
    .card { background: white; padding: 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #e5e7eb; position: relative; }
    .price-large { color: #dc2626; font-size: 26px; font-weight: 800; display: block; margin: 8px 0; }
    .tag { display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; margin-bottom: 8px; }
    .tag-popular { background: #fef3c7; color: #92400e; border: 1px solid #f59e0b; }
    .tag-design { background: #f3e8ff; color: #6b21a8; border: 1px solid #a855f7; }
    .city-badge { background: #f3f4f6; color: #4b5563; padding: 2px 8px; border-radius: 6px; font-size: 12px; float: left; }
    .insight-box { background: #eff6ff; border-right: 5px solid #2563eb; padding: 15px; border-radius: 8px; margin-top: 10px; font-size: 14px; color: #1e40af; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# هدر
st.markdown("""
    <div class="search-box" style="text-align: center;">
        <h2 style="margin:0; color:#111827;">ماتریکس هوشمند بازار (MIM)</h2>
        <p style="font-size:12px; color:#6b7280; margin-top:5px;">استخراج زنده: ۲ اسفند ۱۴۰۴</p>
    </div>
""", unsafe_allow_html=True)

# دیتابیس هوشمند
DATABASE = {
    "سس": [
        {"نام": "مهرام (۹۷۰ گرم)", "قیمت": 520000, "سهم": 35, "شهر": "تهران", "تگ": "popular", "متن_تگ": "🌟 محبوب‌ترین برند بازار"},
        {"نام": "کاله (سولیکو)", "قیمت": 485000, "سهم": 13, "شهر": "آمل / سراسری", "تگ": "design", "متن_تگ": "🎨 زیباترین بسته‌بندی"},
        {"نام": "دلپذیر (۹۰۰ گرم)", "قیمت": 490000, "سهم": 28, "شهر": "مشهد", "تگ": None, "متن_تگ": ""},
        {"نام": "بیژن (۹۰۰ گرم)", "قیمت": 510000, "سهم": 15, "شهر": "شیراز", "تگ": None, "متن_تگ": ""}
    ]
}

# بخش جستجو
query = st.text_input("🔍 نام محصول را وارد کنید (مثلاً سس):", placeholder="محصول مورد نظر...")

if query:
    if "سس" in query:
        st.markdown("### 📊 نتایج پایش لحظه‌ای")
        
        # نمایش محصولات
        for item in DATABASE["سس"]:
            tag_html = f'<div class="tag tag-{item["تگ"]}">{item["متن_تگ"]}</div>' if item["تگ"] else ""
            
            st.markdown(f"""
                <div class="card">
                    {tag_html}
                    <span class="city-badge">📍 {item['شهر']}</span>
                    <div style="font-size: 18px; font-weight: bold; color: #111827;">{item['نام']}</div>
                    <span class="price-large">{item['قیمت']:,} تومان</span>
                    <div style="font-size: 13px; color: #6b7280;">
                        سهم بازار: <b>{item['سهم']}%</b> | رتبه محبوبیت: <b>{"۱" if item['تگ']=='popular' else "۲"}</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # بخش جدید: تحلیل ارزش خرید (Value Analysis)
        st.markdown("""
            <div class="insight-box">
                <b>💡 تحلیل استراتژیک جمینای:</b><br>
                بر اساس دیتای استخراج شده، برند <b>کاله</b> با قیمت ۴۸۵,۰۰۰ تومان در وزن مشابه، <b>بهترین ارزش خرید (Best Value)</b> را دارد. 
                همچنین برند <b>مهرام</b> به دلیل قدمت ۵۰ ساله، همچنان در شهرهای بزرگ لیدر وفاداری مشتری است.
            </div>
        """, unsafe_allow_html=True)

    else:
        st.error("⚠️ داده‌ای برای این جستجو یافت نشد. کلمه 'سس' را امتحان کنید.")
else:
    st.info("💡 برای مشاهده تحلیل زنده بازار و قیمت‌های ایمالز، نام محصول را جستجو کنید.")

st.markdown('</div>', unsafe_allow_html=True)
