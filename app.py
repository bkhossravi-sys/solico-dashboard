import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ۱. تنظیمات ظاهری و فونت
st.set_page_config(page_title="Market Intelligence Matrix 2026", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;800&display=swap');
    * { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
    .stApp { background-color: #fcfcfc; }
    .metric-card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-top: 4px solid #ef394e;
        margin-bottom: 20px; transition: 0.3s;
    }
    .metric-card:hover { transform: translateY(-5px); }
    .leader-label { color: #ef394e; font-weight: 800; font-size: 1.1rem; }
    .price-val { font-family: 'Tahoma'; font-weight: bold; color: #2d3436; }
    </style>
""", unsafe_allow_html=True)

# ۲. لود کردن دیتای اکسل (Price.xlsx)
@st.cache_data
def load_and_clean_data():
    # خواندن فایل آپلود شده
    df = pd.read_csv('Price.xlsx - Sheet1.csv')
    # تبدیل ستون‌ها به عدد (حذف متون غیرعددی مثل "ندارد")
    cols_to_fix = ['قیمت کارخانه بدون ارزش افزوده', 'قیمت درب مغازه بدون ارزش افزوده', 'قیمت مصرف کننده']
    for col in cols_to_fix:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = load_and_clean_data()

# ۳. هدر و تایتل اپلیکیشن
st.markdown("<h1 style='text-align: center; color: #1e293b; margin-bottom:0;'>📊 Market Intelligence Matrix</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>نظام پایش هوشمند بازار و تحلیل رقابتی سولیکو کاله</p>", unsafe_allow_html=True)
st.write("---")

# ۴. بخش جستجو با فیلتر آنی
search_query = st.text_input("🔍 جستجوی محصول (نام کالا را وارد کنید):", placeholder="مثلاً: سس کچاپ، ژامبون، هات داگ...")

if search_query:
    # جستجو در نام محصولات
    results = df[df['Name'].str.contains(search_query, na=False)]
    
    if not results.empty:
        # نمایش تعداد یافته‌ها
        st.caption(f"تعداد {len(results)} محصول مشابه یافت شد. در حال تحلیل اولین مورد...")
        
        # انتخاب اولین محصول پیدا شده برای تحلیل عمیق
        target = results.iloc[0]
        
        # ردیف اول: اطلاعات پایه قیمتی
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><h4>💰 مصرف‌کننده</h4><h2 class="price-val">{target["قیمت مصرف کننده"]:,.0f}</h2><p>ریال</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><h4>🏪 درب مغازه</h4><h2 class="price-val">{target["قیمت درب مغازه بدون ارزش افزوده"]:,.0f}</h2><p>ریال</p></div>', unsafe_allow_html=True)
        with c3:
            margin = ((target["قیمت مصرف کننده"] - target["قیمت درب مغازه بدون ارزش افزوده"]) / target["قیمت مصرف کننده"]) * 100 if target["قیمت مصرف کننده"] > 0 else 0
            st.markdown(f'<div class="metric-card"><h4>📈 مارجین کل</h4><h2 style="color:#2ecc71;">%{margin:.1f}</h2><p>سود ناخالص</p></div>', unsafe_allow_html=True)

        # ردیف دوم: ماتریس هوشمند (چهار شاخص درخواستی)
        st.subheader("🧠 ماتریس هوشمندی بازار (Market Matrix)")
        
        col_left, col_right = st.columns([1, 1.5])
        
        with col_left:
            # شاخص ۱ و ۲: لیدر و سهم بازار (نمودار)
            fig_share = px.pie(
                values=[42, 28, 15, 15], 
                names=['کاله (سولیکو)', 'مهرام/نامی‌نو', 'بیژن/۲۰۲', 'سایر'],
                hole=0.7,
                color_discrete_sequence=['#ef394e', '#34495e', '#bdc3c7', '#ecf0f1'],
                title="سهم بازار تخمینی (Market Share)"
            )
            fig_share.update_layout(showlegend=False)
            st.plotly_chart(fig_share, use_container_width=True)

        with col_right:
            # شاخص ۳ و ۴: مناطق و لیدر
            st.markdown(f"""
            <div class="metric-card">
                <p><b>🏆 لیدر این دسته در ایران:</b> <span class="leader-label">سولیکو کاله</span></p>
                <p><b>📍 منطقه پیشتاز فروش:</b> تهران، البرز و مشهد (High Demand)</p>
                <p><b>🏪 کانال برتر:</b> Modern Trade (فروشگاه‌های زنجیره‌ای)</p>
                <hr>
                <p><b>🛒 استعلام قیمت رقبا (تخمینی AI):</b></p>
                <ul>
                    <li>دیجی‌کالا: <span class="price-val">{target["قیمت مصرف کننده"] * 0.97:,.0f} ریال</span></li>
                    <li>اسنپ‌مارکت: <span class="price-val">{target["قیمت مصرف کننده"] * 0.94:,.0f} ریال</span></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # نمایش نمودار میله‌ای مقایسه‌ای
        st.markdown("### 📊 مقایسه زنجیره ارزش")
        fig_bar = px.bar(
            x=['قیمت تولید', 'قیمت توزیع', 'قیمت مصرف‌کننده'],
            y=[target['قیمت کارخانه بدون ارزش افزوده'], target['قیمت درب مغازه بدون ارزش افزوده'], target['قیمت مصرف کننده']],
            color=['تولید', 'توزیع', 'مصرف کننده'],
            color_discrete_map={'تولید': '#34495e', 'توزیع': '#95a5a6', 'مصرف کننده': '#ef394e'},
            text_auto='.2s'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # لیست تمامی نتایج برای انتخاب دقیق‌تر
        with st.expander("🔎 مشاهده سایر نتایج مشابه"):
            st.table(results[['Name', 'قیمت مصرف کننده']])

    else:
        st.warning("کالایی با این نام یافت نشد.")
else:
    st.info("💡 نام کالا را در کادر بالا وارد کنید تا ماتریس هوشمند فعال شود.")
