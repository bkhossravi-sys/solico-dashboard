import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from thefuzz import process
import google.generativeai as genai

# --- تنظیمات صفحه و استایل مشابه Power BI Mobile ---
st.set_page_config(page_title="Solico Dashboard", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTextInput > div > div > input { border-radius: 20px; text-align: right; }
    .kpi-card { background-color: white; padding: 15px; border-radius: 15px; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; margin-bottom: 10px; }
    .price-tag { color: #d32f2f; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- استخراج داده‌ها از لیست قیمت (نمونه از فایل ارسالی) ---
# [span_0](start_span)[span_1](start_span)[span_2](start_span)قیمت‌ها بر اساس ستون 'فروش' فایل PDF شما درج شده است[span_0](end_span)[span_1](end_span)[span_2](end_span)
data = [
    [span_3](start_span){"نام": "کوکتل مخصوص", "قیمت": 14970000, "دسته": "سوسیس فله"}, #[span_3](end_span)
    [span_4](start_span){"نام": "مرغ آمل ریز ۱۱۰", "قیمت": 8450000, "دسته": "کالای فله"}, #[span_4](end_span)
    [span_5](start_span){"نام": "جونه ریز ۱۱۰", "قیمت": 13270000, "دسته": "کالای فله"}, #[span_5](end_span)
    [span_6](start_span){"نام": "هات داگ روسی فله توری", "قیمت": 7790000, "دسته": "سوسیس فله"}, #[span_6](end_span)
    [span_7](start_span){"نام": "ژامبون مخلوط دار فرش", "قیمت": 552000, "دسته": "محصولات دار فرش"}, #[span_7](end_span)
    [span_8](start_span){"نام": "مایونز پرچرب دبه", "قیمت": 10158000, "دسته": "مکمل و سالادی"}, #[span_8](end_span)
    [span_9](start_span){"نام": "زیتون شور باهسته معمولی", "قیمت": 19000000, "دسته": "زیتون"} #[span_9](end_span)
]
df = pd.DataFrame(data)

# --- بخش جستجوی هوشمند ---
st.title("📊 داشبورد استراتژیک سولیکو")
query = st.text_input("", placeholder="نام محصول را جستجو کنید...")

if query:
    # پیدا کردن بهترین تطبیق با استفاده از کتابخانه thefuzz
    match, score = process.extractOne(query, df["نام"].tolist())
    
    if score > 50:
        item = df[df["نام"] == match].iloc[0]
        
        # نمایش اطلاعات کالا در کارت‌های شکیل
        st.markdown(f"""
        <div class="kpi-card">
            <h3>{item['نام']}</h3>
            <p class="price-tag">{item['قیمت']:,} <span style="font-size:14px">ریال</span></p>
            <p style="color:gray">دسته: {item['دسته']}</p>
        </div>
        """, unsafe_allow_html=True)

        # --- ویژوال‌های مشابه اسکرین‌شات‌های ارسالی ---
        #         fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = (item['قیمت'] / 20000000) * 100, # نمایش فرضی موقعیت قیمتی
            title = {'text': "شاخص رقابت‌پذیری قیمتی"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#00ced1"}}
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)

        # --- اتصال ایمن به Gemini ---
        st.markdown("### 🤖 تحلیل هوشمند بازار")
        if st.secrets.get("GOOGLE_API_KEY"):
            try:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"تحلیل لیدر بازار و رقبا برای محصول غذایی: {item['نام']}")
                st.info(response.text)
            except Exception as e:
                st.error("خطا در برقراری ارتباط با مدل هوش مصنوعی.")
        else:
            st.warning("لطفاً API Key را در تنظیمات Streamlit وارد کنید.")
    else:
        st.error("محصولی با این نام یافت نشد.")

else:
    st.info("برای شروع، بخشی از نام کالا را تایپ کنید.")
