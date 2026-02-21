import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from thefuzz import process
import google.generativeai as genai

# --- تنظیمات ظاهر داشبورد مدیریتی ---
st.set_page_config(page_title="Solico Market Intelligence", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f0f2f5; }
    .main-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center; }
    .price-text { color: #d32f2f; font-size: 35px; font-weight: bold; margin: 0; }
    .stTextInput > div > div > input { border-radius: 25px; border: 2px solid #0078d4; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- دیتابیس محصولات (بر اساس لیست قیمت فوریه ۲۰۲۶) ---
# [span_4](start_span)[span_5](start_span)[span_6](start_span)[span_7](start_span)[span_8](start_span)استخراج شده از منابع ارسالی شما[span_4](end_span)[span_5](end_span)[span_6](end_span)[span_7](end_span)[span_8](end_span)
data = [
    {"نام": "کوکتل مخصوص", "قیمت": 14970000, "دسته": "سوسیس فله"},
    {"نام": "مرغ آمل ریز ۱۱۰", "قیمت": 8450000, "دسته": "کالای فله"},
    {"نام": "جونه ریز ۱۱۰", "قیمت": 13270000, "دسته": "کالای فله"},
    {"نام": "خونه درشت ۱۳۵", "قیمت": 10550000, "دسته": "کالای فله"},
    {"نام": "هات داگ روسی فله توری", "قیمت": 7790000, "دسته": "سوسیس فله"},
    {"نام": "ژامبون مخلوط دار فرش", "قیمت": 552000, "دسته": "محصولات دار فرش"},
    {"نام": "بیکن ایرلندی دار فرش", "قیمت": 4410200, "دسته": "محصولات دار فرش"},
    {"نام": "سس کچاپ بطری ۸۰۰ گرمی", "قیمت": 1250000, "دسته": "سس"},
    {"نام": "مایونز پرچرب دبه", "قیمت": 10158000, "دسته": "سس دبه"},
    {"نام": "زیتون شور باهسته (معمولی)", "قیمت": 19000000, "دسته": "زیتون"},
    {"نام": "پنیر چدار نارنجی", "قیمت": 735000, "دسته": "پنیر"}
]
df = pd.DataFrame(data)

# --- هدر برنامه ---
st.markdown("<h2 style='text-align: center;'>📊 سیستم تحلیل هوشمند کالا</h2>", unsafe_allow_html=True)
query = st.text_input("", placeholder="نام کالا را وارد کنید (مثلاً: کوکتل مخصوص)")

if query:
    # جستجوی فازی برای پیدا کردن نزدیک‌ترین کالا
    match, score = process.extractOne(query, df["نام"].tolist())
    
    if score > 55:
        item = df[df["نام"] == match].iloc[0]
        
        # ۱. کارت شاخص قیمت (Power BI Style)
        st.markdown(f"""
        <div class="main-card">
            <h3 style="margin-bottom:5px;">{item['نام']}</h3>
            <p style="color:gray;">قیمت فروش (ریال)</p>
            <p class="price-text">{item['قیمت']:,}</p>
            <p style="margin-top:10px;">دسته: <b>{item['دسته']}</b></p>
        </div>
        """, unsafe_allow_html=True)

        # ۲. نمودار عقربه‌ای Gauge (مشابه اسکرین‌شات Power BI ارسالی)
        #         fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = (item['قیمت'] / 20000000) * 100, 
            title = {'text': "شاخص رقابت در بازار", 'font': {'size': 18}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "#00ced1"},
                'steps': [
                    {'range': [0, 50], 'color': "#f0f2f6"},
                    {'range': [50, 100], 'color': "#e1e4e8"}]
            }
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

        # ۳. تحلیل هوش مصنوعی Gemini
        st.markdown("---")
        st.subheader("🤖 تحلیل استراتژیک هوش مصنوعی")
        
        # دریافت کلید امنیتی از تنظیمات استریم‌لیت
        api_key = st.secrets.get("GOOGLE_API_KEY")
        
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"به عنوان تحلیلگر بازار مواد غذایی ایران، محصول {item['نام']} با قیمت {item['قیمت']} ریال را تحلیل کن. لیدر بازار کیست و رقبای آنلاین چه قیمتی دارند؟"
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception:
                st.error("خطا در برقراری ارتباط با مدل هوش مصنوعی.")
        else:
            st.warning("لطفاً GOOGLE_API_KEY را در بخش Secrets استریم‌لیت وارد کنید.")

    else:
        st.error("کالای مورد نظر در لیست یافت نشد.")
else:
    st.info("برای مشاهده آنالیز، نام کالا را جستجو کنید.")
