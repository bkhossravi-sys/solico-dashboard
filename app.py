import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai
from thefuzz import process

# --- تنظیمات ظاهر اپلیکیشن (Mobile-First) ---
st.set_page_config(page_title="Market Analyzer Pro", layout="centered")

# استایل CSS برای شبیه‌سازی اپلیکیشن‌های مدرن (مانند عکس‌های ارسالی شما)
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stTextInput > div > div > input { border-radius: 25px; border: 2px solid #E0E0E0; padding: 10px 20px; }
    .card { background-color: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #EEE; }
    .metric-box { text-align: center; padding: 10px; background: #F0F2F6; border-radius: 12px; }
    .status-up { color: #28A745; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- بارگذاری داده‌های لیست قیمت (بر اساس فایل ارسالی شما) ---
# [span_0](start_span)[span_1](start_span)[span_2](start_span)من در اینجا داده‌های کلیدی فایل شما را به صورت دیکشنری وارد کرده‌ام[span_0](end_span)[span_1](end_span)[span_2](end_span)
raw_data = [
    {"ID": "30004266", "Product": "مرغ آمل ریز ۱۱۰", "Price": 8450000, "Category": "کالای فله"},
    {"ID": "30003814", "Product": "جونه ریز ۱۱۰", "Price": 13270000, "Category": "کالای فله"},
    {"ID": "30010530", "Product": "ژامبون مخلوط دار فرش", "Price": 552000, "Category": "دار فرش"},
    {"ID": "20011912", "Product": "هات داگ روسی فله توری", "Price": 7790000, "Category": "سوسیس فله"},
    {"ID": "30008846", "Product": "کوکتل مخصوص", "Price": 14970000, "Category": "سوسیس فله"},
    {"ID": "20008830", "Product": "آلمانی B", "Price": 4550000, "Category": "سوسیس فله"},
    {"ID": "30002707", "Product": "مایونز پرچرب دبه", "Price": 10158000, "Category": "سس دبه"},
    {"ID": "30008397", "Product": "پنیر چدار نارنجی", "Price": 735000, "Category": "پنیر"},
    {"ID": "30014985", "Product": "زیتون شور باهسته معمولی", "Price": 19000000, "Category": "زیتون"},
]
df_master = pd.DataFrame(raw_data)

# --- تنظیمات هوش مصنوعی جمینای ---
genai.configure(api_key="YOUR_GEMINI_API_KEY") # کلید خود را اینجا بگذارید
ai_model = genai.GenerativeModel('gemini-1.5-flash')

# --- بخش جستجوی هوشمند ---
st.markdown("## 🔍 آنالیز هوشمند کالا")
search_query = st.text_input("", placeholder="نام کالا را وارد کنید (مثلاً: کوکتل یا مایونز)...")

if search_query:
    # الگوریتم Fuzzy Search برای پیدا کردن نزدیک‌ترین نام کالا
    choices = df_master['Product'].tolist()
    best_match, score = process.extractOne(search_query, choices)

    if score > 50:
        selected_item = df_master[df_master['Product'] == best_match].iloc[0]
        
        # نمایش کارت محصول
        st.markdown(f"""
        <div class="card">
            <p style="color: grey; font-size: 0.8rem;">کد کالا: {selected_item['ID']}</p>
            <h3>{selected_item['Product']}</h3>
            <h2 style="color: #D32F2F;">{selected_item['Price']:,} <span style="font-size: 1rem;">ریال</span></h2>
            <p>دسته بندی: <b>{selected_item['Category']}</b></p>
        </div>
        """, unsafe_allow_html=True)

        # --- بخش تحلیل AI حرفه‌ای ---
        with st.spinner('در حال دریافت تحلیل زنده بازار از Gemini...'):
            try:
                prompt = f"""
                شما یک تحلیلگر ارشد بازار مواد غذایی در ایران هستید. 
                محصول: {selected_item['Product']}
                قیمت فعلی سولیکو: {selected_item['Price']} ریال
                
                تحلیل کن:
                1. لیدر بازار ایران (Market Leader) در این محصول کیست؟ (مثلاً کاله، مهرام، بیژن یا ...)
                2. محبوبیت در اینستاگرام و شبکه های اجتماعی برای این محصول چطور است؟
                3. قیمت رقبای آنلاین (دیجی کالا/اسنپ مارکت) در چه محدوده ای است؟
                4. قدرت برند در کدام شهرهای ایران بیشتر است؟
                
                پاسخ را به صورت حرفه‌ای، فارسی و در قالب Bullet Points کوتاه بده.
                """
                ai_response = ai_model.generate_content(prompt)
                
                st.markdown("### 🧠 تحلیل استراتژیک هوش مصنوعی")
                st.write(ai_response.text)
                
            except Exception as e:
                st.error("خطا در اتصال به هوش مصنوعی.")

        # --- بخش ویژوال (شبیه عکس‌های ارسالی) ---
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            # نمودار گیج (Gauge Chart) برای سهم بازار فرضی
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 65, # سهم بازار فرضی
                title = {'text': "سهم بازار (فرضی)"},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
            ))
            fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-box">
                <p>محبوبیت اجتماعی</p>
                <h3 class="status-up">▲ 12%</h3>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("کالایی با این نام در لیست قیمت ۲۰۲۶ پیدا نشد.")

else:
    st.info("نام محصول را در کادر بالا بنویسید تا آنالیز کامل ظاهر شود.")
