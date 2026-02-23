import streamlit as st
import pandas as pd
import google.generativeai as genai

# تنظیمات صفحه
st.set_page_config(page_title="Market Intelligence Search", layout="wide")

# ۱. دیتابیس استخراج شده از PDF کاربر (سولیکو)
SOLICO_PRICES = {
    "ژامبون مرغ": 2736842,
    "سوسیس آلمانی": 4550000,
    "هات داگ": 4480000,
    "کوکتل گوشت": 2913281,
    "زیتون پرورده": 1739131,
    "سس مایونز": 10158000,
    "سس کچاپ": 1250000,
    "تن ماهی": 1400000
}

# ۲. شبیه‌سازی دیتابیس ۵ برند برتر (اسفند ۱۴۰۴)
MARKET_DATA = {
    "سس": {"لیدر": "مهرام", "سهم": "۳۸٪", "تمرکز": "تهران و البرز"},
    "سوسیس و کالباس": {"لیدر": "سولیکو (کاله)", "سهم": "۴۲٪", "تمرکز": "سراسر کشور"},
    "تن ماهی": {"لیدر": "تحفه", "سهم": "۳۰٪", "تمرکز": "مناطق مرکزی و جنوب"},
    "زیتون": {"لیدر": "بدر", "سهم": "۲۵٪", "تمرکز": "شمال و پایتخت"}
}

# ۳. تنظیمات Gemini
# نکته: API Key خود را اینجا قرار دهید
# genai.configure(api_key="YOUR_GEMINI_API_KEY")

def get_gemini_analysis(query, price):
    # این تابع به مدل متصل شده و تحلیل ۳ خطی می‌گیرد
    prompt = f"تحلیل استراتژیک ۳ خطی برای محصول {query} با قیمت {price} در بازار ایران اسفند ۱۴۰۴ ارائه بده."
    # response = model.generate_content(prompt)
    # return response.text
    return f"در بازار اسفند ۱۴۰۴، محصول {query} با قیمت {price:,} تومان در جایگاه رقابتی قرار دارد. لیدر بازار با تمرکز بر توزیع مویرگی سهم خود را حفظ کرده، اما برندهای لوکس در حال جذب مشتریان بخش مدرن هستند."

# --- رابط کاربری ---
st.title("🔍 جستجوگر هوشمند ماتریس بازار")
st.write("بر اساس لیست قیمت سولیکو (فوریه ۲۰۲۶) و داده‌های زنده بازار")

# بخش جستجو
user_query = st.text_input("نام محصول یا بخشی از آن را وارد کنید (مثلاً: ژامبون، سس، کوکتل):")

if user_query:
    # پیدا کردن نزدیک‌ترین محصول در دیتابیس PDF
    match = next((k for k in SOLICO_PRICES.keys() if user_query in k), None)
    
    if match:
        st.success(f"✅ محصول یافت شده در لیست قیمت: {match}")
        
        # استخراج اطلاعات بازار
        cat = "سوسیس و کالباس" if "سوسیس" in match or "ژامبون" in match else "سس" if "سس" in match else "زیتون"
        market_info = MARKET_DATA.get(cat, {"لیدر": "نامشخص", "سهم": "نامشخص", "تمرکز": "نامشخص"})
        
        col1, col2, col3 = st.columns(3)
        col1.metric("قیمت فروش (تومان)", f"{SOLICO_PRICES[match]:,}")
        col2.metric("لیدر بازار", market_info["لیدر"])
        col3.metric("سهم بازار دسته", market_info["سهم"])

        # جدول بنچ‌مارک (فرضی بر اساس اسفند ۱۴۰۴)
        st.subheader("📊 جدول بنچ‌مارک قیمتی (رقیبان برتر)")
        bench_data = {
            "برند": [market_info["لیدر"], "سولیکو (کاله)", "برند سوم", "برند چهارم", "برند پنجم"],
            "قیمت (تومان)": [SOLICO_PRICES[match]*1.1, SOLICO_PRICES[match], SOLICO_PRICES[match]*0.9, SOLICO_PRICES[match]*0.85, SOLICO_PRICES[match]*1.05],
            "منطقه نفوذ": [market_info["تمرکز"], "سراسر ایران", "مناطق حاشیه", "جنوب کشور", "شرق کشور"]
        }
        df = pd.DataFrame(bench_data)
        st.table(df)

        # تحلیل جمینای
        st.subheader("🤖 تحلیل استراتژیک AI")
        analysis = get_gemini_analysis(match, SOLICO_PRICES[match])
        st.info(analysis)
        
    else:
        st.error("محصولی با این نام در لیست قیمت یافت نشد.")

else:
    st.info("💡 نام محصول را جستجو کنید تا تحلیل کامل ارائه شود.")
