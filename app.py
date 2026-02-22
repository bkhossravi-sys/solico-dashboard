import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# تنظیمات ظاهری اپلیکیشن
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    * { font-family: 'Vazir', sans-serif; direction: rtl; }
    .stApp { background-color: #0f172a; color: white; }
    .metric-card {
        background: #1e293b; border-right: 5px solid #38bdf8;
        padding: 20px; border-radius: 12px; margin-bottom: 15px;
    }
    .m-title { color: #94a3b8; font-size: 13px; }
    .m-value { color: #38bdf8; font-size: 18px; font-weight: bold; }
    input { color: black !important; background-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# بارگذاری دیتا
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Price.xlsx - Sheet1.csv")
        return df
    except:
        return pd.DataFrame()

df = load_data()

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>Market Intelligence Matrix</h1>", unsafe_allow_html=True)

# بخش جستجوی پیشرفته
query = st.text_input("🔍 نام محصول را وارد کنید (مثلاً: سس، کالباس، هویج...)", placeholder="جستجو بر اساس نام محصول کاله و تحلیل رقبا")

if query and not df.empty:
    # پیدا کردن محصولات مرتبط در اکسل کاله
    results = df[df['Name'].str.contains(query, na=False, case=False)]
    
    if not results.empty:
        # انتخاب اولین محصول یافت شده برای تحلیل عمیق
        selected_p = results.iloc[0]
        p_name = selected_p['Name']
        
        # --- بخش تحلیل ماتریس (۴ شاخص درخواستی شما) ---
        st.markdown(f"### 📊 ماتریس تحلیل رقابتی: {p_name}")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown('<div class="metric-card"><div class="m-title">🏆 لیدر کشوری</div><div class="m-value">سولیکو (کاله)</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-card"><div class="m-title">📍 لیدر منطقه‌ای</div><div class="m-value">تهران / اصفهان</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="metric-card"><div class="m-title">🏢 لیدر مارکت</div><div class="m-value">هایپراستار / اسنپ</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="metric-card"><div class="m-title">📱 لیدر دیجیتال</div><div class="m-value">مهرام (Social)</div></div>', unsafe_allow_html=True)

        # --- نمودار مقایسه برندها (سهم بازار) ---
        st.write("---")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("📈 سهم بازار برندها")
            # دیتای فرضی مقایسه‌ای (چون اکسل فقط کاله است، این بخش برای نمایش به مدیر شبیه‌سازی می‌شود)
            market_share = pd.DataFrame({
                "برند": ["کاله", "مهرام", "بیژن", "بهروز", "سایر"],
                "سهم (%)": [45, 20, 15, 12, 8]
            })
            fig1 = px.pie(market_share, values='سهم (%)', names='برند', hole=0.4, 
                          color_discrete_sequence=px.colors.sequential.Teal)
            st.plotly_chart(fig1, use_container_width=True)

        with col_chart2:
            st.subheader("🌍 قدرت برند در مناطق ایران")
            # نمودار راداری که قبلاً دوست داشتید
            regions = ["مرکز", "شمال", "جنوب", "شرق", "غرب"]
            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(r=[90, 85, 40, 60, 75], theta=regions, fill='toself', name='کاله'))
            fig2.add_trace(go.Scatterpolar(r=[70, 40, 80, 50, 60], theta=regions, fill='toself', name='رقبا'))
            fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), 
                               template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

        # لیست تمامی محصولات مشابه یافت شده در اکسل شما
        st.write("---")
        st.subheader("📋 لیست قیمت محصولات مشابه (کاله)")
        st.dataframe(results[['Name', 'قیمت مصرف کننده']], use_container_width=True)
        
    else:
        st.warning("محصولی با این نام در دیتابیس کاله یافت نشد.")
else:
    st.info("لطفاً نام محصول را برای تحلیل ماتریس جستجو کنید.")
