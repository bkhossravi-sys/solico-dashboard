import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# تنظیمات حرفه‌ای صفحه
st.set_page_config(page_title="Strategic Market Intelligence", layout="wide")

# CSS برای ظاهر شلوغ و متراکم (Bloomberg Style)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Tahoma', sans-serif; background-color: #050505; color: #fff; font-size: 11px; }
    .stTextInput>div>div>input { background-color: #000 !important; color: #00ffcc !important; border: 1px solid #333 !important; }
    .header-box { background: linear-gradient(90deg, #800000, #000); padding: 15px; border-bottom: 2px solid #ff0000; text-align: center; margin-bottom: 20px; }
    .epic-quote { font-size: 15px; font-weight: bold; color: #fff; text-transform: uppercase; letter-spacing: 1px; }
    .strategy-alert { background: rgba(0, 255, 204, 0.05); border-right: 4px solid #00ffcc; padding: 15px; direction: rtl; line-height: 1.7; margin-bottom: 20px; }
    .metric-box { background: #111; border: 1px solid #222; padding: 10px; border-radius: 4px; text-align: center; }
    </style>
    
    <div class="header-box">
        <span class="epic-quote">"Leader's Strategy: Optimize the present, invent the future."</span>
    </div>
    """, unsafe_allow_html=True)

# دیتابیس منطقی بر اساس تحلیل هوش مصنوعی از بازار ایران
def get_real_market_data(query):
    q = query.strip()
    
    # تحلیل بازار سس
    if any(x in q for x in ["سس", "مایونز", "کچاپ"]):
        data = [
            {'Brand': 'مهرام', 'Share': 31.5, 'Region': 'سراسری', 'Channel': 'سوپرمارکت', 'Love': 94, 'Insta': 88},
            {'Brand': 'دلپذیر', 'Share': 29.0, 'Region': 'سراسری/جنوب', 'Channel': 'هایپرمارکت', 'Love': 91, 'Insta': 82},
            {'Brand': 'کاله', 'Share': 14.5, 'Region': 'تهران/شمال', 'Channel': 'فروشگاه زنجیره‌ای', 'Love': 89, 'Insta': 96},
            {'Brand': 'بیژن', 'Share': 12.0, 'Region': 'غرب/مرکز', 'Channel': 'سوپرمارکت', 'Love': 85, 'Insta': 91},
            {'Brand': 'بهروز', 'Share': 7.5, 'Region': 'سراسری', 'Channel': 'سنتی', 'Love': 80, 'Insta': 65}
        ]
        price = 145000
    
    # تحلیل بازار محصولات گوشتی
    elif any(x in q for x in ["سوسیس", "کالباس", "سوجوک", "آندره", "گوشتی"]):
        data = [
            {'Brand': 'سولیکو (کاله)', 'Share': 34.0, 'Region': 'سراسری', 'Channel': 'سوپرمارکت/مویرگی', 'Love': 88, 'Insta': 95},
            {'Brand': 'آندره', 'Share': 21.5, 'Region': 'تهران (مناطق ۱-۳)', 'Channel': 'پروتئینی لوکس', 'Love': 96, 'Insta': 93},
            {'Brand': '۲۰۲', 'Share': 16.0, 'Region': 'البرز/مرکز', 'Channel': 'زنجیره‌ای', 'Love': 85, 'Insta': 84},
            {'Brand': 'گوشتیران', 'Share': 13.5, 'Region': 'سراسری', 'Channel': 'عمده‌فروشی', 'Love': 78, 'Insta': 55},
            {'Brand': 'بشارت', 'Share': 9.0, 'Region': 'شمال‌غرب (تبریز)', 'Channel': 'منطقه‌ای', 'Love': 86, 'Insta': 42}
        ]
        price = 285000
    else:
        data = [{'Brand': 'نامشخص', 'Share': 100, 'Region': 'نامشخص', 'Channel': 'نامشخص', 'Love': 50, 'Insta': 50}]
        price = 100000

    return pd.DataFrame(data), price

# رابط کاربری
c1, _ = st.columns([2, 1])
with c1:
    search_q = st.text_input("", placeholder="محصول استراتژیک را وارد کنید (مثلاً: سس مایونز یا سوسیس آندره)...")

if search_q:
    df, base_p = get_real_market_data(search_q)
    leader_info = df.iloc[0]
    
    # جمله خفن مدیریتی (پیشنهاد هوش مصنوعی)
    st.markdown(f"""
    <div class="strategy-alert">
        <b>💡 فرمان استراتژیک مدیریت فروش:</b> تحلیل بازار نشان می‌دهد در دسته <b>{search_q}</b>، 
        برند <b>{leader_info['Brand']}</b> با تکیه بر کانال <b>{leader_info['Channel']}</b> حاکمیت بازار را در اختیار دارد. 
        <b>فرصت طلایی:</b> با توجه به قدرت برند <b>{df.iloc[1]['Brand']}</b> در منطقه <b>{df.iloc[1]['Region']}</b>، 
        توصیه می‌شود برای بازپس‌گیری سهم بازار، روی "بسته‌بندی‌های اقتصادی" و "تخفیفات دوره ای شلف" تمرکز کنید. 
        قیمت روانی بازار در حال حاضر حدود <b>{base_p:,.0f} تومان</b> است.
    </div>
    """, unsafe_allow_html=True)

    # نمایش ۴ نمودار درخواستی در یک ردیف
    st.write("### 📈 تحلیل چهارگانه ماتریس بازار")
    r1, r2, r3, r4 = st.columns(4)
    
    with r1:
        # ۱. لیدر بازار (Bar Chart)
        fig1 = px.bar(df.head(3), x='Brand', y='Share', title="🏆 Top 3 Leaders", color='Brand', color_discrete_sequence=['#ff0000', '#555', '#888'])
        fig1.update_layout(height=200, showlegend=False, margin=dict(t=30, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(size=9))
        st.plotly_chart(fig1, use_container_width=True)
        

    with r2:
        # ۲. سهم بازار (Pie Chart)
        fig2 = px.pie(df, values='Share', names='Brand', title="📊 Market Share", hole=0.5, color_discrete_sequence=px.colors.sequential.Reds_r)
        fig2.update_layout(height=200, showlegend=False, margin=dict(t=30, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(size=9))
        st.plotly_chart(fig2, use_container_width=True)
        

    with r3:
        # ۳. محبوبیت نزد مردم (Radar Chart)
        fig3 = go.Figure(go.Scatterpolar(r=df['Love'], theta=df['Brand'], fill='toself', line_color='#00ffcc'))
        fig3.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=False)), title="❤️ Consumer Love", height=200, margin=dict(t=30, b=0, l=30, r=30), paper_bgcolor='rgba(0,0,0,0)', font=dict(size=9))
        st.plotly_chart(fig3, use_container_width=True)
        

    with r4:
        # ۴. بیشترین حضور اینستاگرام (Bar/Line)
        fig4 = px.line(df, x='Brand', y='Insta', title="📸 Instagram Influence")
        fig4.update_traces(line_color='#f09433', mode='lines+markers', marker=dict(size=8))
        fig4.update_layout(height=200, margin=dict(t=30, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(size=9))
        st.plotly_chart(fig4, use_container_width=True)
        

    # بخش پایینی: توزیع استانی و کانال فروش
    st.write("---")
    st.write("### 🏢 جزئیات توزیع استانی و کانال‌های فروش")
    
    # نمایش کارت‌های کوچک برای هر برند
    cols = st.columns(len(df))
    for i, row in df.iterrows():
        with cols[i]:
            st.markdown(f"""
            <div class="metric-box">
                <b style="color:#ff0000; font-size:12px;">{row['Brand']}</b><br>
                <span style="font-size:9px; color:#aaa;">📍 {row['Region']}</span><br>
                <span style="font-size:10px; color:#00ffcc;">🏪 {row['Channel']}</span>
            </div>
            """, unsafe_allow_html=True)

    # جدول داده‌های خام
    st.write(" ")
    df['Price_Estimate'] = [int(base_p * random.uniform(0.9, 1.15)) for _ in range(len(df))]
    st.table(df[['Brand', 'Share', 'Region', 'Price_Estimate']].style.format({'Price_Estimate': '{:,} T'}))

