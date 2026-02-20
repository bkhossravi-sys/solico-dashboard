import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# تنظیمات اصلی داشبورد
st.set_page_config(page_title="Strategic Marketing Monitoring", layout="wide")

# CSS حرفه‌ای برای طراحی مدرن و فونت‌های ریز
st.markdown("""
    <style>
    :root { --main-red: #b11e22; --dark-card: #111111; --text-gray: #a0a0a0; }
    html, body, [class*="css"] { font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #000000; color: #ffffff; font-size: 13px; }
    
    /* هدر سایت */
    .header-container { border-bottom: 1px solid #333; padding: 10px 0; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
    .brand-title { font-size: 18px; font-weight: 700; letter-spacing: 1px; color: var(--main-red); }
    
    /* کارت‌های KPI */
    .kpi-container { background: var(--dark-card); border: 1px solid #222; padding: 15px; border-radius: 4px; text-align: center; }
    .kpi-label { font-size: 10px; color: var(--text-gray); text-transform: uppercase; margin-bottom: 5px; display: block; }
    .kpi-value { font-size: 16px; font-weight: bold; color: #fff; }
    
    /* بخش پیشنهاد مدیر فروش */
    .advice-box { background: rgba(177, 30, 34, 0.05); border-right: 3px solid var(--main-red); padding: 12px; font-size: 12px; line-height: 1.6; direction: rtl; margin-bottom: 20px; }
    
    /* استایل اینستاگرام */
    .insta-chip { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: bold; }
    
    /* ورودی متن */
    .stTextInput>div>div>input { background-color: #000 !important; color: #fff !important; border: 1px solid #333 !important; font-size: 13px !important; border-radius: 2px !important; }
    
    /* مخفی کردن منوهای اضافی Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    
    <div class="header-container">
        <div class="brand-title">STRATEGIC MARKETING MONITORING</div>
        <div style="font-size: 10px; color: #666;">v2.1 | LIVE INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

# دیتابیس هوشمند با قیمت‌های دقیق اعلام شده
def fetch_market_data(query):
    q = query.strip()
    # تحلیل سس ساشه (کارتن 300 عددی)
    if "ساشه" in q:
        return pd.DataFrame({
            'Product': ['فرانسوی 300ct', 'مایونز 300ct', 'کچاپ 300ct', 'خردل 300ct'],
            'Brand': ['مهرام', 'کاله (سولیکو)', 'بیژن', 'دلپذیر'],
            'Price_IRR': [17000000, 13200000, 15800000, 14500000],
            'Market_Share': [38, 32, 18, 12],
            'Social_Impact': [88, 95, 84, 75]
        })
    # تحلیل سوجوک و محصولات 300 گرمی (DigiKala & Snapp)
    elif any(x in q for x in ["سوجوک", "سلامی", "300", "اسلامی"]):
        return pd.DataFrame({
            'Product': ['سوجوک ویژه 300g', 'سلامی اسلامی 300g', 'پپرونی 300g', 'ژامبون 300g'],
            'Brand': ['کاله (سولیکو)', 'سولیکو', 'گوشتیران', '202'],
            'Price_IRR': [1850000, 2150000, 1680000, 1950000],
            'Market_Share': [52, 45, 16, 14],
            'Social_Impact': [97, 94, 71, 85]
        })
    return pd.DataFrame()

# بخش ورودی
col_input = st.columns([1, 2, 1])[1]
with col_input:
    search_q = st.text_input("", placeholder="Search products (e.g., ساشه, سوجوک)...")

if search_q:
    df = fetch_market_data(search_q)
    if not df.empty:
        # پیشنهاد استراتژیک مدیر فروش
        st.markdown(f"""
        <div class="advice-box">
            <b>💼 پیشنهاد استراتژیک فروش:</b> با توجه به دیتای استخراج شده، برند <b>{df.iloc[df['Market_Share'].idxmax()]['Brand']}</b> لیدر است. 
            برای محصول <b>{search_q}</b>، پیشنهاد می‌شود روی "باندلینگ" در اسنپ‌مارکت تمرکز کنید تا سهم بازار در شبکه توزیع مویرگی تقویت شود.
        </div>
        """, unsafe_allow_html=True)

        # کارت‌های KPI ریز و شیک
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(f"<div class='kpi-container'><span class='kpi-label'>Leader</span><span class='kpi-value'>{df.iloc[df['Market_Share'].idxmax()]['Brand']}</span></div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='kpi-container'><span class='kpi-label'>Avg Price (IRR)</span><span class='kpi-value'>{df.iloc[:, 2].mean():,.0f}</span></div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='kpi-container'><span class='kpi-label'>Social King</span><span class='insta-chip'>{df.iloc[df['Social_Impact'].idxmax()]['Brand']}</span></div>", unsafe_allow_html=True)
        with k4: st.markdown(f"<div class='kpi-container'><span class='kpi-label'>Data Source</span><span class='kpi-value' style='color:#666;'>SNAPP / DIGI</span></div>", unsafe_allow_html=True)

        st.write("---")
        
        # نمودارها در یک ردیف
        c_left, c_right = st.columns(2)
        
        with c_left:
            # نمودار سهم بازار با استایل مینیمال
            fig_m = px.bar(df, x='Brand', y='Market_Share', color='Brand',
                           title="Market Share Analysis (%)",
                           color_discrete_sequence=['#b11e22', '#333', '#555', '#777'])
            fig_m.update_layout(showlegend=False, height=250, margin=dict(t=30, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=10))
            st.plotly_chart(fig_m, use_container_width=True)
            
        with c_right:
            # تاثیر اینستاگرام (نمودار خطی مدرن)
            fig_s = go.Figure(go.Scatter(x=df['Brand'], y=df['Social_Impact'], mode='lines+markers', 
                                        line=dict(color='#E1306C', width=2), marker=dict(size=8)))
            fig_s.update_layout(title="Instagram Engagement Index", height=250, margin=dict(t=30, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=10))
            st.plotly_chart(fig_s, use_container_width=True)

        # جدول داده‌ها با استایل فشرده
        st.markdown("<p style='font-size:11px; color:#555;'>DETAILED RAW DATA</p>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data found. Try 'ساشه' or 'سوجوک'.")
