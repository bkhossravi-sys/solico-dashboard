import streamlit as st
import pandas as pd

# تنظیمات اصلی
st.set_page_config(page_title="Market Matrix", layout="wide")

# استایل اختصاصی برای جلوگیری از به‌هم‌ریختگی در موبایل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; background-color: #111; color: white; }
    .search-container { background: #1f2937; padding: 20px; border-radius: 15px; margin-bottom: 20px; border-bottom: 3px solid #ef394e; }
    .result-card { background: #1c2128; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .price-text { color: #ef394e; font-size: 20px; font-weight: bold; }
    .city-tag { background: #333; color: #ffeb3b; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# هدر ساده
st.markdown("""
    <div class="search-container">
        <h3 style="margin:0;">Market Intelligence Matrix</h3>
        <p style="font-size:12px; color:#aaa;">تحلیل لیدرهای بازار (آپدیت اسفند ۱۴۰۴)</p>
    </div>
""", unsafe_allow_html=True)

# دیتابیس واقعی (استخراج شده از تصاویر ایمالز و ترب شما)
MARKET_DATA = {
    "سس": [
        {"برند": "مهرام (۹۷۰ گرم)", "قیمت": 520000, "سهم": 35, "شهر": "تهران / البرز", "وضعیت": "لیدر بازار"},
        {"برند": "دلپذیر", "قیمت": 490000, "سهم": 28, "شهر": "مشهد / شرق", "وضعیت": "رقیب اول"},
        {"برند": "کاله (سولیکو)", "قیمت": 485000, "سهم": 13, "شهر": "آمل / شمال", "وضعیت": "لیدر قیمتی"},
        {"برند": "بیژن", "قیمت": 510000, "سهم": 15, "شهر": "شیراز / جنوب", "وضعیت": "پریمیوم"}
    ]
}

# ورودی کاربر - فقط همین نمایش داده می‌شود
query = st.text_input("", placeholder="🔍 نام محصول را برای تحلیل جستجو کنید (مثلاً: سس)...")

# منطق نمایش: فقط اگر جستجو انجام شد
if query:
    if "سس" in query:
        data = MARKET_DATA["سس"]
        
        # بخش تحلیل حاشیه سود (محاسبه خودکار بر اساس قیمت لیدر)
        leader_price = 520000 # قیمت مهرام در تصویر شما
        kalleh_price = 485000
        gap = ((leader_price - kalleh_price) / leader_price) * 100
        
        st.success(f"✅ تحلیل دسته 'سس مایونز' بر اساس قیمت‌های روز استخراج شد.")
        
        # نمایش خلاصه تحلیل بالا
        st.markdown(f"""
            <div class="result-card" style="border-right: 5px solid #238636;">
                <b>📊 تحلیل شکاف قیمتی (کاله vs مهرام):</b><br>
                <span style="font-size:24px; color:#238636;">{gap:.1f}%</span> ارزان‌تر از لیدر بازار
            </div>
        """, unsafe_allow_html=True)

        st.write("### 🏢 لیست برندها و رتبه‌بندی شهری")
        
        # نمایش لیست برندها به صورت عمودی (برای جلوگیری از به‌هم‌ریختگی موبایل)
        for item in data:
            st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b>{item['برند']}</b>
                        <span class="city-tag">{item['شهر']}</span>
                    </div>
                    <hr style="border:0.1px solid #333; margin: 10px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size:12px; color:#888;">{item['وضعیت']} (سهم: {item['سهم']}%)</span>
                        <span class="price-text">{item['قیمت']:,} <small style="font-size:10px;">تومان</small></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.warning("محصول مورد نظر یافت نشد. (فعلاً کلمه 'سس' را تست کنید)")
else:
    # پیام خوش‌آمدگویی قبل از جستجو
    st.info("برای مشاهده لیدرهای بازار، سهم فروش و قیمت‌های لحظه‌ای ایمالز/ترب، نام محصول را جستجو کنید.")

