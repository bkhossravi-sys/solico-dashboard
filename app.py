import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# تنظیمات اصلی
st.set_page_config(page_title="Strategic Marketing Monitoring", layout="wide")

# استایل فوق حرفه‌ای، فونت‌های ریز و طراحی فشرده
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Tahoma', sans-serif; background-color: #000; color: #eee; font-size: 12px; }
    .main-title { font-size: 16px; font-weight: bold; color: #b11e22; border-bottom: 1px solid #333; padding-bottom: 5px; margin-bottom: 15px; }
    .stTextInput>div>div>input { background-color: #111 !important; color: #00ffcc !important; border: 1px solid #333 !important; font-size: 13px !important; }
    .kpi-box { background: #111; border: 1px solid #222; padding: 10px; border-radius: 4px; text-align: center; }
    .kpi-val { font-size: 15px; font-weight: bold; color: #fff; display: block; }
    .kpi-lab { font-size: 9px; color: #777; text-transform: uppercase; }
    .advice-card { background: rgba(177,30,34,0.1); border-right: 3px solid #b11e22; padding: 10px; font-size: 11px; direction: rtl; margin-bottom: 15px; }
    .insta-tag { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743); padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    [data-testid="stMetricValue"] { font-size: 16px !important; }
    </style>
    <div class="main-title">STRATEGIC MARKETING MONITORING | AI-POWERED ENGINE</div>
    """, unsafe_allow_html=True)

# موتور هوشمند تولید دیتا (شبیه‌ساز جستجوی Gemini در بازار ایران)
def ai_market_analyzer(query):
    # محصولات سولیکو (کاله) معمولاً لیدر هستند
    brands = ['کاله (سولیکو)', 'مهرام', 'دلپذیر', 'بیژن', 'گوشتیران', '۲۰۲', 'تحفه', 'طبیعت']
    
    # منطق قیمت‌گذاری هوشمند بر اساس نوع محصول
    base_price = 150000
    if any(x in query for x in ["ساشه", "کارتن"]): base_price = 1400000
    if any(x in query for x in ["تن", "ماهی"]): base_price = 85000
    if any(x in query for x in ["سوجوک", "سلامی", "پنیر"]): base_price = 195000
    
    data = []
    # تولید ۵ رقیب اصلی به صورت داینامیک برای هر محصول
    selected_brands = random.sample(brands, 5)
    if 'کاله (سولیکو)' not in selected_brands: selected_brands[0] = 'کاله (سولیکو)'
    
    for brand in selected_brands:
        price_variation = random.uniform(0.8, 1.2)
        market_share = random.randint(10, 45) if brand == 'کاله (سولیکو)' else random.randint(5, 25)
        data.append({
            'برند': brand,
            'محصول': f"{query} - اختصاصی",
            'قیمت_تومان': int(base_price * price_variation),
            'سهم_بازار_%': market_share,
            'نفوذ_اینستاگرام': random.randint(60, 98),
            'رضایت_مشتری': random.randint(70, 95)
        })
    return pd.DataFrame(data).sort_values(by='سهم_بازار_%', ascending=False)

# فیلد جستجوی آزاد
search_term = st.text_input("", placeholder="نام هر محصولی را وارد کنید (مثلاً: تن ماهی، سس گاردین، سس هزارجزیره، سوجوک...)")

if search_term:
    df = ai_market_analyzer(search_term)
    
    # ۱. بخش پیشنهاد استراتژیک هوشمند
    leader_brand = df.iloc[0]['برند']
    st.markdown(f"""
    <div class="advice-card">
        <b>💡 تحلیل هوشمند مدیر فروش:</b> در دسته <b>{search_term}</b>، برند <b>{leader_brand}</b> در حال حاضر فضای رقابتی را کنترل می‌کند. 
        با توجه به نرخ تعامل در اینستاگرام، پیشنهاد می‌شود برای افزایش فروش، کمپین "تست طعم" در شعب منتخب اسنپ‌مارکت فعال شود. 
        قیمت بهینه برای نفوذ در بازار حدود <b>{int(df['قیمت_تومان'].mean()):,.0f} تومان</b> ارزیابی می‌شود.
    </div>
    """, unsafe_allow_html=True)

    # ۲. ردیف شاخص‌های کلیدی (Compact KPIs)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='kpi-box'><span class='kpi-lab'>Leader</span><span class='kpi-val'>{leader_brand}</span></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='kpi-box'><span class='kpi-lab'>Avg Price</span><span class='kpi-val'>{int(df['قیمت_تومان'].mean()):,.0f}</span></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='kpi-box'><span class='kpi-lab'>Social King</span><span class='insta-tag'>{df.iloc[df['نفوذ_اینستاگرام'].idxmax()]['برند']}</span></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='kpi-box'><span class='kpi-lab'>Status</span><span class='kpi-val' style='color:#00ffcc;'>High Demand</span></div>", unsafe_allow_html=True)

    # ۳. نمودارهای تحلیل بازار ایران
    st.write("---")
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        fig_market = px.pie(df, values='سهم_بازار_%', names='برند', hole=0.6, 
                           title=f"سهم بازار ایران: {search_term}",
                           color_discrete_sequence=px.colors.sequential.Reds_r)
        fig_market.update_layout(height=250, margin=dict(t=30, b=0, l=0, r=0), showlegend=False)
        st.plotly_chart(fig_market, use_container_width=True)
        

    with col_r:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=df['برند'], y=df['نفوذ_اینستاگرام'], name='Instagram Impact', line=dict(color='#E1306C', width=2)))
