import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# تنظیمات اصلی صفحه برای حالت موبایل و دسکتاپ
st.set_page_config(page_title="Solico Market Intelligence", layout="wide")

# استایل فوق حرفه‌ای ترکیبی از Power BI و Digikala
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; background-color: #0d1117; color: #e6edf3; }
    
    /* هدر سایت با ایمیل کاربر */
    .top-bar { background: #161b22; padding: 10px; border-bottom: 2px solid #ef394e; text-align: center; margin-bottom: 20px; }
    .user-email { color: #8b949e; font-size: 12px; letter-spacing: 1px; }
    
    /* کارت‌های مشابه Power BI */
    .metric-card { background: #1c2128; border-radius: 12px; padding: 20px; border: 1px solid #30363d; box-shadow: 0 4px 15px rgba(0,0,0,0.3); text-align: center; }
    .strategy-box { background: rgba(239, 57, 78, 0.1); border-right: 5px solid #ef394e; padding: 20px; border-radius: 8px; direction: rtl; margin-bottom: 25px; line-height: 1.8; }
    
    /* استایل اینپوت جستجو */
    .stTextInput>div>div>input { border-radius: 30px !important; border: 1px solid #ef394e !important; background: #0d1117 !important; color: #fff !important; text-align: center; height: 50px; }
    
    /* دایره‌های دسته‌بندی دیجی‌کالا */
    .cat-circle { background: #fff; border-radius: 50%; width: 55px; height: 55px; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 24px; border: 2px solid #ef394e; }
    </style>
    
    <div class="top-bar">
        <span style="color:#ef394e; font-weight:bold; font-size:18px;">SOLICO MARKET INTELLIGENCE</span><br>
        <span class="user-email">By: behr.khosravi@solico-group.ir</span>
    </div>
    """, unsafe_allow_html=True)

# دیتابیس لوگوها
BRAND_LOGOS = {
    "سولیکو (کاله)": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Kalleh_Logo.svg/1200px-Kalleh_Logo.svg.png",
    "کاله": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Kalleh_Logo.svg/1200px-Kalleh_Logo.svg.png",
    "مهرام": "https://mahramco.com/wp-content/uploads/2021/05/logo-mahram.png",
    "دلپذیر": "https://delpazir.com/wp-content/themes/delpazir/assets/images/logo.png",
    "آندره": "https://andrefood.com/wp-content/uploads/2021/03/Andre-Logo-1.png",
    "۲۰۲": "https://202.ir/wp-content/uploads/2021/05/logo.png",
    "طبیعت": "https://tabiat.ir/wp-content/uploads/2020/06/logo.png",
    "تحفه": "https://tofeh.com/wp-content/uploads/2020/05/logo.png"
}

def fetch_market_data(query):
    q = query.strip()
    # تحلیل سس‌ها
    if any(x in q for x in ["سس", "مایونز", "کچاپ", "خردل"]):
        data = [
            {'Brand': 'مهرام', 'Share': 34, 'Lead': 'تهران', 'B2B': 'بسیار قوی', 'B2W': 'فعال', 'Type': 'Retail/HoReCa'},
            {'Brand': 'دلپذیر', 'Share': 31, 'Lead': 'سراسری', 'B2B': 'متوسط', 'B2W': 'بسیار قوی', 'Type': 'Mass Market'},
            {'Brand': 'بیژن', 'Share': 18, 'Lead': 'غرب', 'B2B': 'فعال', 'B2W': 'متوسط', 'Type': 'Retail'},
            {'Brand': 'سولیکو (کاله)', 'Share': 17, 'Lead': 'شمال', 'B2B': 'قوی', 'B2W': 'فعال', 'Type': 'Premium'}
        ]
        strat = "تقویت زنجیره تأمین در بخش B2W (بنکداری) شهرهای مشهد و تبریز جهت کاهش سهم رقبای سنتی."
    
    # تحلیل پروتئینی (سوسیس و کالباس)
    elif any(x in q for x in ["سوسیس", "کالباس", "سوجوک", "ژامبون", "آندره", "گوشت"]):
        data = [
            {'Brand': 'سولیکو (کاله)', 'Share': 42, 'Lead': 'سراسری', 'B2B': 'بسیار قوی', 'B2W': 'سیستمی', 'Type': 'Supermarket'},
            {'Brand': 'آندره', 'Share': 24, 'Lead': 'تهران (مرکز)', 'B2B': 'HoReCa', 'B2W': 'متوسط', 'Type': 'Delicatessen'},
            {'Brand': '۲۰۲', 'Share': 19, 'Lead': 'البرز', 'B2B': 'فعال', 'B2W': 'قوی', 'Type': 'Chain Stores'},
            {'Brand': 'گوشتیران', 'Share': 15, 'Lead': 'مرکز', 'B2B': 'سازمانی', 'B2W': 'قوی', 'Type': 'Wholesale'}
        ]
        strat = "توسعه خط تولید سوجوک و محصولات تخصصی برای تسلط بر بخش B2B رستوران‌های کژوال تهران."
    
    # تحلیل تن ماهی و زیتون
    elif any(x in q for x in ["تن", "ماهی", "زیتون"]):
        data = [
            {'Brand': 'طبیعت', 'Share': 36, 'Lead': 'سراسری', 'B2B': 'سازمانی', 'B2W': 'بسیار قوی', 'Type': 'Hypermarket'},
            {'Brand': 'تحفه', 'Share': 29, 'Lead': 'جنوب/تهران', 'B2B': 'تخصصی', 'B2W': 'قوی', 'Type': 'Health Focus'},
            {'Brand': 'شیلتون', 'Share': 20, 'Lead': 'مرکز', 'B2B': 'متوسط', 'B2W': 'فعال', 'Type': 'Retail'}
        ]
        strat = "استفاده از مدل فروش B2B برای قراردادهای تأمین غذای ارگان‌ها و بهبود توزیع در فروشگاه‌های زنجیره‌ای."
    else:
        return None, None
    return pd.DataFrame(data), strat

# ردیف آیکون‌های دسته‌بندی (Style Digikala)
st.write(" ")
c_cat = st.columns(5)
cats = [("سس", "🥫"), ("گوشتی", "🥩"), ("کنسرو", "🐟"), ("زیتون", "🫒"), ("لبنیات", "🥛")]
for i, (n, ico) in enumerate(cats):
    with c_cat[i]:
        st.markdown(f'<div class="cat-circle">{ico}</div><p style="text-align:center;font-size:10px;margin-top:5px;">{n}</p>', unsafe_allow_html=True)

# فیلد جستجو
search = st.text_input("", placeholder="نام محصول را برای تحلیل هوشمند وارد کنید...")

if search:
    df, strategy_text = fetch_market_data(search)
    
    if df is not None:
        # کارت استراتژی (Hero Section)
        st.markdown(f"""
        <div class="strategy-box">
            <h4 style="color:#ef394e; margin-bottom:10px;">💡 استراتژی افزایش سهم بازار {search}:</h4>
            {strategy_text}
        </div>
        """, unsafe_allow_html=True)

        # ردیف نمودارهای Power BI
        st.write("### 📊 Metrics Dashboard")
        m1, m2, m3 = st.columns([2, 1, 1])
        
        with m1:
            fig1 = px.bar(df, x='Brand', y='Share', color='Share', text='Share', 
                          color_continuous_scale=['#444', '#ef394e'], title="سهم بازار (%)")
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#fff", height=300)
            st.plotly_chart(fig1, use_container_width=True)
            
        with m2:
            fig2 = px.pie(df, values='Share', names='Brand', hole=0.7, color_discrete_sequence=['#ef394e', '#555', '#888', '#aaa'])
            fig2.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=300)
            st.plotly_chart(fig2, use_container_width=True)
            
        with m3:
            fig3 = go.Figure(go.Scatterpolar(r=[80, 70, 90, 60], theta=['B2B', 'B2W', 'Retail', 'Online'], fill='toself', fillcolor='rgba(239, 57, 78, 0.3)', line_color='#ef394e'))
            fig3.update_layout(polar=dict(bgcolor='#161b22', radialaxis=dict(visible=False)), height=300, margin=dict(t=40, b=20), title="Channel Strength")
            st.plotly_chart(fig3, use_container_width=True)
            
        # کارت‌های شناسنامه برند با لوگو
        st.write("---")
        st.write("### 🏢 Brand Operational ID")
        cols = st.columns(len(df))
        for i, row in df.iterrows():
            with cols[i]:
                logo = BRAND_LOGOS.get(row['Brand'], "https://via.placeholder.com/100")
                st.markdown(f"""
                <div class="metric-card">
                    <img src="{logo}" width="60" style="margin-bottom:10px;">
                    <h5 style="color:#ef394e;">{row['Brand']}</h5>
                    <p style="font-size:11px; color:#8b949e;">📍 لیدر: {row['Lead']}</p>
                    <div style="text-align:right; font-size:10px;">
                        <b>B2B:</b> {row['B2B']}<br>
                        <b>B2W:</b> {row['B2W']}<br>
                        <b>Focus:</b> {row['Type']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("داده‌ای یافت نشد. لطفاً از دسته‌های سس، سوسیس، کالباس، تن ماهی یا زیتون استفاده کنید.")
