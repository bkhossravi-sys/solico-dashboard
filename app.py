import streamlit as st
import google.generativeai as genai
import pandas as pd
import requests

# تنظیمات صفحه برای حالت موبایل
st.set_page_config(page_title="Solico Market Analyzer", layout="centered")

# اتصال به جمینای
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

# استایل‌دهی CSS برای شبیه‌سازی اپلیکیشن
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTextInput > div > div > input { border-radius: 20px; }
    .report-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

## --- بخش هدر و جستجو ---
st.title("📊 آنالیزور هوشمند بازار")
product_name = st.text_input("نام کالا را وارد کنید (مثلاً: مایونز ۹۰۰ یا تون ماهی)", placeholder="جستجو در بازار...")

if product_name:
    with st.spinner('در حال استخراج داده‌های زنده و تحلیل هوشمند...'):
        
        # ۱. شبیه‌سازی دریافت داده از اسکرپر (دیجی‌کالا/اسنپ مارکت)
        # در پروژه واقعی اینجا توابع Scrapy یا Selenium فراخوانی می‌شوند
        market_data = {
            "برندها": ["مهرام", "بیژن", "کاله (سولیکو)", "تبرک"],
            "قیمت_میانگین": [95000, 92000, 98000, 89000],
            "سهم_شبکه‌های_اجتماعی": ["۲۵٪", "۱۵٪", "۴۰٪", "۲۰٪"],
            "شهر_اصلی": ["تهران", "مشهد", "اصفهان", "تبریز"]
        }
        
        df = pd.DataFrame(market_data)

        # ۲. ارسال داده به جمینای برای تحلیل حرفه‌ای
        prompt = f"""
        به عنوان یک تحلیلگر خبره بازار ایران، محصول "{product_name}" را بر اساس داده‌های زیر تحلیل کن:
        {df.to_string()}
        
        خروجی را در این قالب بده:
        ۱. لیدر فعلی بازار کیست؟
        ۲. محبوبیت در شبکه‌های اجتماعی (اینستاگرام و تلگرام).
        ۳. تحلیل قیمت رقبا نسبت به برند سولیکو.
        ۴. پیشنهاد استراتژیک برای تصاحب سهم بازار در شهرهای ضعیف‌تر.
        تحلیل باید بسیار حرفه‌ای و خلاصه باشد.
        """
        
        response = model.generate_content(prompt)

        ## --- نمایش خروجی به سبک داشبورد عکس‌های ارسالی ---
        
        # کارت لیدر بازار
        st.markdown(f"""<div class="report-card">
            <h3>🏆 لیدر بازار: {market_data['برندها'][2]}</h3>
            <p>{response.text[:200]}...</p>
        </div>""", unsafe_allow_html=True)

        # نمایش نمودار مقایسه قیمت (شبیه عکس دوم)
        st.subheader("📊 مقایسه قیمت و سهم اجتماعی")
        st.bar_chart(df.set_index('برندها')['قیمت_میانگین'])

        # تحلیل کامل جمینای
        with st.expander("👁 مشاهده تحلیل عمیق AI"):
            st.write(response.text)

        # دیتای شهرهای برتر
        st.info(f"📍 تمرکز اصلی برند برتر در شهر: {market_data['شهر_اصلی'][2]}")

else:
    st.info("لطفاً نام یک محصول را برای تحلیل وارد کنید.")
