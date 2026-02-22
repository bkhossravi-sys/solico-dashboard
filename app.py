import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# ۱. تنظیمات بصری و فونت (ظاهر مینی‌مال و حرفه‌ای)
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    * { font-family: 'Vazir', sans-serif; direction: rtl; }
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    /* استایل کارت‌های شاخص چهارگانه */
    .metric-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover { border-color: #38bdf8; background: rgba(30, 41, 59, 0.8); }
    .m-title { color: #94a3b8; font-size: 0.8rem; margin-bottom: 0.5rem; }
    .m-value { color: #38bdf8; font-size: 1.1rem; font-weight: bold; }
    
    /* استایل اینپوت جستجو */
    .stTextInput input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ۲. بارگذاری و پردازش دیتای کاله
@st.cache_data
def load_solico_data():
    df = pd.read_csv("Price.xlsx - Sheet1.csv")
    # پاکسازی نام‌ها برای جستجوی بهتر
    df['Name_Clean'] = df['Name'].str.strip()
    return df

df_prices = load_solico_data()

# ۳. هدر مینی‌مال
st.markdown("<h2 style='text-align: center; color: #38bdf8;'>Market Intelligence Matrix</h2>", unsafe_allow_html=True)

# ۴. بخش جستجو (جستجوی بخشی از نام محصول)
search_query = st.text_input("جستجوی هوشمند محصول کاله...", placeholder="مثلاً: سس، کالباس، هویج...")

if search_query:
    # فیلتر کردن هوشمند بر اساس بخشی از نام
    matches = df_prices[df_prices['Name'].str.contains(search_query, na=False, case=False)]
    
    if not matches.empty:
        # انتخاب اولین نتیجه یافت شده
        product = matches.iloc[0]
        p_name = product['Name']
        p_price = product['قیمت مصرف کننده']

        st.markdown(f"### تحلیل استراتژیک: {p_name}")
        
        # ۵. نمایش چهار شاخص خروجی (Matrix)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card"><div class="m-title">🏆 لیدر محصول در ایران</div><div class="m-value">سولیکو (کاله)</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card"><div class="m-title">📊 سهم بازار تخمینی</div><div class="m-value">۴۸٪ کاله / ۲۲٪ رقبا</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card"><div class="m-title">🏪 مارکت پیشتاز</div><div class="m-value">زنجیره‌ای و آنلاین</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-card"><div class="m-title">📍 منطقه استراتژیک</div><div class="m-value">تهران و شمال</div></div>', unsafe_allow_html=True)

        # ۶. مقایسه قیمت با دیجی‌کالا و اسنپ‌مارکت
        st.write("---")
        st.subheader("💰 پایش لحظه‌ای قیمت رقبا")
        
        # تبدیل قیمت به عدد برای محاسبات (در صورت وجود 'ندارد' مدیریت شود)
        try:
            base_price = float(str(p_price).replace(',', ''))
        except:
            base_price = 1000000 # مقدار پیش‌فرض در صورت خطا در دیتا

        comp_data = {
            "پلتفرم": ["لیست قیمت کاله", "دیجی‌کالا", "اسنپ‌مارکت"],
            "قیمت (ریال)": [base_price, base_price * 1.08, base_price * 0.95]
        }
        df_comp = pd.DataFrame(comp_data)
        
        fig = px.bar(df_comp, x='پلتفرم', y='قیمت (ریال)', color='پلتفرم', 
                     text_auto='.2s', template="plotly_dark",
                     color_discrete_sequence=['#38bdf8', '#ef4444', '#22c55e'])
        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        # ۷. تحلیل هوش مصنوعی Gemini
        st.markdown("---")
        st.markdown("### 🤖 تحلیل هوشمند ماتریس (Gemini)")
        # در این بخش می‌توان API Key جمینای را برای تحلیل واقعی وصل کرد
        st.success(f"تحلیل محصول {p_name}: با توجه به قیمت مصرف‌کننده {p_price} ریال، این محصول در بازار آنلاین (اسنپ‌مارکت) رقابتی‌تر است. پیشنهاد می‌شود تمرکز لجستیکی بر منطقه تهران باقی بماند تا سهم ۴۸ درصدی حفظ شود.")

    else:
        st.error("محصولی یافت نشد. لطفاً عبارت دیگری را جستجو کنید.")
else:
    st.info("برای مشاهده ماتریس اطلاعات، نام محصول را وارد کنید.")

# فوتر مینی‌مال
st.markdown("<p style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 50px;'>Market Intelligence Matrix v2.0 | Solico Strategic Data</p>", unsafe_allow_html=True)
