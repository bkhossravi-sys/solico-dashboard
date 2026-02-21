import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from thefuzz import process
import google.generativeai as genai

# تنظیمات ظاهری داشبورد مدیریتی
st.set_page_config(page_title="Solico Plus Dashboard", layout="centered")

# استایل‌دهی برای شبیه‌سازی اپلیکیشن موبایل Power BI
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f0f2f5; }
    .kpi-card { 
        background-color: white; padding: 20px; border-radius: 15px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center; 
    }
    .price-value { color: #d32f2f; font-size: 32px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# [span_2](start_span)[span_3](start_span)[span_4](start_span)[span_5](start_span)[span_6](start_span)دیتابیس محصولات استخراج شده از لیست قیمت شما[span_2](end_span)[span_3](end_span)[span_4](end_span)[span_5](end_span)[span_6](end_span)
data = [
    {"نام": "مرغ آمل ریز ۱۱۰", "قیمت": 8450000, "دسته": "کالای فله"},
    {"نام": "جونه ریز ۱۱۰", "قیمت": 13270000, "دسته": "کالای فله"},
    {"نام": "خونه درشت ۱۳۵", "قیمت": 10550000, "دسته": "کالای فله"},
    {"نام": "کوکتل مخصوص", "قیمت": 14970000, "دسته": "سوسیس فله"},
    {"نام": "هات داگ روسی فله توری", "قیمت": 7790000, "دسته": "سوسیس فله"},
    {"نام": "ژامبون مخلوط دار فرش", "قیمت": 552000, "دسته": "دار فرش"},
    {"نام": "بیکن ایرلندی دار فرش", "قیمت": 4410200, "دسته": "دار فرش"},
    {"نام": "سس کچاپ ۸۰۰ گرمی", "قیمت": 1250000, "دسته": "سس"},
    {"نام": "مایونز پرچرب دبه", "قیمت": 10158000, "دسته": "سس دبه"},
    {"نام": "زیتون شور باهسته معمولی", "قیمت": 19000000, "دسته": "زیتون"}
]
df = pd.DataFrame(data)

st.title("📊 سیستم آنالیز هوشمند سولیکو")

# بخش جستجوگر هوشمند
search_query = st.text_input("", placeholder="نام کالا را وارد کنید (مثلاً: کوکتل مخصوص)...")

if search_query:
    # [span_7](start_span)[span_8](start_span)[span_9](start_span)جستجوی فازی برای پیدا کردن نزدیک‌ترین نام[span_7](end_span)[span_8](end_span)[span_9](end_span)
    match, score = process.extractOne(search_query, df["نام"].tolist())
    
    if score > 50:
        item = df[df["نام"] == match].iloc[0]
        
        # نمایش کارت شاخص قیمت (مشابه عکس‌های Power BI)
        st.markdown(f"""
        <div class="kpi-card">
            <p style="color: #555;">محصول انتخاب شده:</p>
            <h2 style="margin:0;">{item['نام']}</h2>
            <hr>
            <p style="color: #555;">قیمت فروش (ریال):</p>
            <p class="price-value">{item['قیمت']:,}</p>
            <p style="color: #888;">دسته: {item['دسته']}</p>
        </div>
        """, unsafe_allow_html=True)

        # نمایش نمودار عقربه‌ای (Gauge) برای تحلیل بصری سهم یا موقعیت قیمتی
        #         fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = (item['قیمت'] / 20000000) * 100, # نمایش فرضی نسبت به سقف قیمت لیست
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "شاخص نفوذ بازار (فرضی)"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#00ced1"},
                'steps': [
                    {'range': [0, 50], 'color': "#e8f8f8"},
                    {'range': [50, 100], 'color': "#b2ebf2"}]
            }
        ))
        fig.update_layout(height=280, margin=dict(l=30, r=30, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

        # تحلیل هوش مصنوعی با اتصال به جمینای
        st.subheader("🤖 تحلیل استراتژیک AI")
        if "GOOGLE_API_KEY" in st.secrets:
            try:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                analysis_prompt = f"تحلیل بازار ایران برای محصول {item['نام']} با قیمت {item['قیمت']} ریال. رقبای اصلی کیستند؟"
                response = model.generate_content(analysis_prompt)
                st.info(response.text)
            except:
                st.error("خطا در ارتباط با هوش مصنوعی. لطفاً API Key را چک کنید.")
        else:
            st.warning("کلید امنیتی (Secrets) در Streamlit تنظیم نشده است.")
    else:
        st.error("کالا در لیست قیمت پیدا نشد!")

else:
    st.info("لطفاً بخشی از نام محصول را تایپ کنید تا آنالیز آغاز شود.")
