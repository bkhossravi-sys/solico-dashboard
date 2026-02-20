import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# تنظیمات پیشرفته صفحه
st.set_page_config(page_title="Solico Strategic Dashboard", layout="wide")

# استایل اختصاصی: فونت ریز، تم تاریک و چیدمان متراکم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tahoma', sans-serif; background-color: #000; color: #fff; font-size: 11px; }
    .stTextInput>div>div>input { background-color: #050505 !important; color: #00ffcc !important; border: 1px solid #333 !important; font-size: 12px !important; }
    .main-banner { background: linear-gradient(90deg, #b11e22 0%, #000 100%); padding: 12px; border-radius: 4px; border-bottom: 2px solid #b11e22; margin-bottom: 20px; text-align: center; }
    .quote { font-size: 14px; font-weight: bold; color: #fff; text-shadow: 2px 2px 4px #000; }
    .strategy-box { background: rgba(177, 30, 34, 0.08); border-right: 4px solid #b11e22; padding: 15px; border-radius: 4px; direction: rtl; line-height: 1.6; margin-bottom: 25px; }
    .plot-container { background: #0a0a0a; border: 1px solid #222; padding: 10px; border-radius: 5px; }
    [data-testid="stMetricValue"] { font-size: 18px !important; color: #00ffcc !important; }
    </style>
    
    <div class="main-banner">
        <span class="quote">"دیتای دقیق، سلاح برندهای پیشرو است؛ بازاری را مدیریت کنید که دیگران فقط تماشاگر آن هستند."</span>
    </div>
    """, unsafe_allow_html=True)

# سیستم هوشمند تفکیک برندهای ایرانی (بدون خطا)
def get_strategic_data(query):
    q = query.strip()
    
    # تعریف دسته‌بندی‌های دقیق
    sauce_brands = ['کاله (گاردن)', 'مهرام', 'دلپذیر', 'بیژن', 'بهروز', 'ترانه']
    meat_brands = ['کاله (سولیکو)', 'گوشتیران', '۲۰۲', 'آندره', 'شام شام', 'رباط']
    tuna_brands = ['تحفه', 'طبیعت', 'شیلتون', 'مکنزی', 'گادول']
    
    # تشخیص بازار هدف
    if any(x in q for x in ["سس", "مایونز", "کچاپ", "فرانسوی", "هزارجزیره"]):
        pool = sauce_brands
        base_price = 148000 if "ساشه" not in q else 1650000
    elif any(x in q for x in ["سوجوک", "کالباس", "سوسیس", "سلامی", "دارفرش", "کوکتل"]):
        pool = meat_brands
        base_price = 235000
    elif any(x in q for x in ["تن", "ماهی"]):
        pool = tuna_brands
        base_price = 95000
    else:
        pool = ['کاله', 'طبیعت', 'میهن', 'پاک']
        base_price = 100000

    # تولید دیتای ۵ رقیب اصلی به صورت تصادفی اما منطقی
    data = []
    selected = random.sample(pool, min(len(pool), 5))
    
    for b in selected:
        # کاله همیشه در دیتای ما جایگاه ویژه‌ای دارد
        share = random.randint(35, 48) if 'کاله' in b else random.randint(8, 22)
        love = random.randint(70, 95)
        insta = random.randint(65, 99)
        data.append({
            'Brand': b,
            'Price': int(base_price * random.uniform(0.92, 1.12)),
            'MarketShare': share,
            'ConsumerLove': love,
            'InstaPresence': insta
        })
    return pd.DataFrame(data).sort_values('MarketShare', ascending=False)

# فیلد جستجو در مرکز
c_src, _ = st.columns([2, 1])
with c_src:
    search_q = st.text_input("", placeholder="نام محصول (مثلاً: سس مایونز، سوجوک، تن ماهی)...")

if search_q:
    df = get_strategic_data(search_q)
    leader_brand = df.iloc[0]['Brand']
    
    # ۱. جمله پیشنهادی خفن به مدیر فروش
    st.markdown(f"""
    <div class="strategy-box">
        <b>🚀 تحلیل فوری مدیریت فروش:</b> در پایش لحظه‌ای بازار <b>{search_q}</b>، برند <b>{leader_brand}</b> لیدر فعلی است. 
        با توجه به نرخ نفوذ در اینستاگرام، پیشنهاد می‌شود برای حفظ سهم بازار، کمپین "تست طعم در محل فروش" (Sampling) را در شهرهای گروه A تقویت کنید. 
        قیمت بهینه برای رقابت تهاجمی در این دسته حدود <b>{int(df['Price'].mean()):,.0f} تومان</b> ارزیابی می‌شود.
    </div>
    """, unsafe_allow_html=True)

    # ۲. چهار نمودار اصلی در یک ردیف
    st.write("### 📊 Market Intelligence Matrix")
    row1 = st.columns(4)
    
    with row1[0]:
        # نمودار لیدر (Bar Chart)
        fig1 = px.bar(df.head(3), x='Brand', y='MarketShare', title="🏆 Top 3 Leaders", color='MarketShare', color_continuous_scale='Reds')
        fig1.update_layout(height=200, showlegend=False, margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(size=9))
        st.plotly_chart(fig1, use_container_width=True)
        
    with row1[1]:
        # سهم بازار (Pie Chart)
        fig2 = px.pie(df, values='MarketShare', names='Brand', title="📊 Market Share (%)", hole=0.5)
        fig2.update_layout(height=200, margin=dict(l=0,r=0,t=30,b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(size=9))
        st.plotly_chart(fig2, use_container_width=True)
        
    with row1[2]:
        # محبوبیت نزد مردم (Horizontal Bar)
        fig3 = px.bar(df.sort_values('ConsumerLove'), x='ConsumerLove', y='Brand', orientation='h', title="❤️ Consumer Love Index", color_discrete_sequence=['#00ffcc'])
        fig3.update_layout(height=200, margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(size=9))
        st.plotly_chart(fig3, use_container_width=True)
        
    with row1[3]:
        # حضور در اینستاگرام (Radar/Line Chart)
        fig4 = go.Figure(go.Scatterpolar(r=df['InstaPresence'], theta=df['Brand'], fill='toself', line_color='#f09433'))
        fig4.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=False)), title="📸 Insta Presence", height=200, margin=dict(l=20,r=20,t=30,b=10), showlegend=False, font=dict(size=9))
        st.plotly_chart(fig4, use_container_width=True)
        
    # ۳. جدول داده‌ها و شلوغ‌کاری حرفه‌ای
    st.write("---")
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        st.markdown("<p style='color:#666;'>RAW MARKET DATA FEED</p>", unsafe_allow_html=True)
        st.table(df.style.format({'Price': '{:,}'}))
    with col_t2:
        st.markdown("<p style='color:#666;'>LIVE KPIs</p>", unsafe_allow_html=True)
        st.metric("Market Volatility", "Low", "+1.2%")
        st.metric("Competitor Aggression", "Medium", "Stable")
        st.metric("Digital Reach", f"{df['InstaPresence'].mean():.1f}%", "+5%")
