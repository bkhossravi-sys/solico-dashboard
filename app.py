import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# تنظیمات صفحه
st.set_page_config(page_title="Market Intelligence Dashboard", layout="wide")

# استایل اختصاصی مشابه گرافیک دیجی‌کالا (قرمز، سفید، خاکستری روشن)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; background-color: #f8f8f8; color: #444; }
    .stTextInput>div>div>input { border-radius: 12px !important; border: 1px solid #ef394e !important; height: 45px; font-size: 16px; text-align: center; }
    .dk-header { background-color: #fff; padding: 10px; border-bottom: 1px solid #e0e0e0; display: flex; justify-content: center; margin-bottom: 20px; }
    .dk-logo { color: #ef394e; font-size: 24px; font-weight: bold; }
    .category-circle { background: #fff; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin: 0 auto 8px; border: 1px solid #f0f0f0; }
    .strategy-card { background: #fff; border-radius: 15px; border-right: 6px solid #ef394e; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); direction: rtl; margin-bottom: 25px; }
    .market-tag { background: #f0f0f0; padding: 4px 12px; border-radius: 20px; font-size: 10px; color: #666; margin-left: 5px; }
    .leader-tag { background: #fff0f1; color: #ef394e; padding: 2px 10px; border-radius: 5px; font-weight: bold; font-size: 11px; }
    </style>
    <div class="dk-header"><span class="dk-logo">MARKET INTELLIGENCE</span></div>
    """, unsafe_allow_html=True)

# سیستم استعلام هوشمند (شبیه‌ساز هوش مصنوعی برای تحلیل بازار)
def get_ai_market_intelligence(query):
    q = query.strip()
    
    # دیتابیس منطقی بر اساس تحلیل زنجیره تأمین ایران
    if any(x in q for x in ["سس", "مایونز", "کچاپ"]):
        data = [
            {'Brand': 'مهرام', 'Share': 32, 'Lead_Province': 'تهران/البرز', 'Market': 'B2C/Supermarket', 'B2B': 'High', 'B2W': 'Active'},
            {'Brand': 'دلپذیر', 'Share': 30, 'Region': 'سراسری', 'Market': 'B2C/Hypermarket', 'B2B': 'Medium', 'B2W': 'Strong'},
            {'Brand': 'کاله', 'Share': 15, 'Region': 'شمال/تهران', 'Market': 'B2C/Chain Stores', 'B2B': 'Strong', 'B2W': 'Active'},
            {'Brand': 'بیژن', 'Share': 13, 'Region': 'غرب کشور', 'Market': 'B2C/Retail', 'B2B': 'Low', 'B2W': 'Medium'}
        ]
        strategy = "تمرکز بر کمپین‌های 'خرید ترکیبی' با نان‌های صنعتی و افزایش حضور در پلتفرم‌های آنلاین (B2C) برای بازپس‌گیری سهم بازار از لیدرهای سنتی."
    
    elif any(x in q for x in ["سوسیس", "کالباس", "آندره", "گوشتی", "سوجوک"]):
        data = [
            {'Brand': 'سولیکو (کاله)', 'Share': 36, 'Lead_Province': 'سراسری', 'Market': 'Supermarket/B2C', 'B2B': 'Strong', 'B2W': 'High'},
            {'Brand': 'آندره', 'Share': 22, 'Lead_Province': 'تهران', 'Market': 'پروتئینی لوکس/HoReCa', 'B2B': 'Active', 'B2W': 'Medium'},
            {'Brand': '۲۰۲', 'Share': 18, 'Lead_Province': 'البرز/مرکز', 'Market': 'Chain Stores', 'B2B': 'Medium', 'B2W': 'Strong'},
            {'Brand': 'گوشتیران', 'Share': 14, 'Lead_Province': 'جنوب/مرکز', 'Market': 'B2B/Wholesale', 'B2B': 'Strong', 'B2W': 'Low'}
        ]
        strategy = f"تقویت کانال HoReCa (هتل‌ها و رستوران‌ها) برای برند {q} و استفاده از مدل توزیع Direct-to-Store جهت کاهش هزینه‌های واسطه‌گری."
    
    else:
        data = [{'Brand': 'نامشخص', 'Share': 100, 'Lead_Province': 'سراسری', 'Market': 'B2C', 'B2B': 'Active', 'B2W': 'Active'}]
        strategy = "برای این محصول دیتای کافی موجود نیست؛ تحلیل بر اساس میانگین بازار خرده‌فروشی انجام شد."

    return pd.DataFrame(data), strategy

# بخش آیکون‌های دایره‌ای مشابه دیجی‌کالا
st.write("### دسته‌بندی‌های بازار")
cols_cat = st.columns(6)
categories = [("سس", "🥫"), ("گوشتی", "🥩"), ("لبنیات", "🥛"), ("نوشیدنی", "🥤"), ("تن‌ماهی", "🐟"), ("روغن", "🌻")]
for i, (name, icon) in enumerate(categories):
    with cols_cat[i]:
        st.markdown(f'<div class="category-circle">{icon}</div><p style="text-align:center; font-size:11px;">{name}</p>', unsafe_allow_html=True)

# فیلد جستجوی هوشمند
search_input = st.text_input("", placeholder="🔍 نام محصول را برای استعلام از جمینای وارد کنید...")

if search_input:
    df, ai_strategy = get_ai_market_intelligence(search_input)
    
    # نمایش جمله کلیدی استراتژیک
    st.markdown(f"""
    <div class="strategy-card">
        <h4 style="color:#ef394e; margin-top:0;">💡 تحلیل هوشمند جمینای برای {search_input}:</h4>
        <p style="font-size:14px;">{ai_strategy}</p>
    </div>
    """, unsafe_allow_html=True)

    # بخش نمودارها در یک ردیف
    st.write("### 📊 ماتریس پایش بازار")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        # سهم بازار کشوری
        fig1 = px.pie(df, values='Share', names='Brand', hole=0.7, color_discrete_sequence=['#ef394e', '#333', '#888', '#ccc'])
        fig1.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("<p style='text-align:center;'>سهم بازار (%)</p>", unsafe_allow_html=True)
        
    with m2:
        # لیدرهای استانی
        fig2 = px.bar(df, x='Share', y='Brand', orientation='h', color_discrete_sequence=['#ef394e'])
        fig2.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("<p style='text-align:center;'>قدرت برندها</p>", unsafe_allow_html=True)
        
    with m3:
        # نمودار رادار برای نفوذ کانال‌ها
        fig3 = go.Figure(go.Scatterpolar(r=[80, 60, 90, 70], theta=['B2B', 'B2W', 'Retail', 'Online'], fill='toself', line_color='#ef394e'))
        fig3.update_layout(polar=dict(radialaxis=dict(visible=False)), height=200, margin=dict(t=30, b=20, l=30, r=30))
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("<p style='text-align:center;'>تحلیل کانال‌های فروش</p>", unsafe_allow_html=True)
        
    with m4:
        # نفوذ منطقه‌ای
        fig4 = px.scatter(df, x="Brand", y="Share", size="Share", color="Brand", title="")
        fig4.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)
        st.caption("<p style='text-align:center;'>پراکندگی رقبا</p>", unsafe_allow_html=True)
        
    # کارت‌های تفکیک بازار (B2B, B2W, Region)
    st.write("---")
    st.write("### 🏢 جزئیات عملیاتی رقبای اصلی")
    
    cols = st.columns(len(df))
    for i, row in df.iterrows():
        with cols[i]:
            st.markdown(f"""
            <div style="background:#fff; padding:15px; border-radius:12px; box-shadow:0 2px 10px rgba(0,0,0,0.05); text-align:center; border:1px solid #eee;">
                <span class="leader-tag">{row['Brand']}</span><br><br>
                <p style="font-size:10px; color:#888;">📍 لیدر در: <b>{row.get('Lead_Province', row.get('Region', 'سراسری'))}</b></p>
                <div style="margin-top:10px;">
                    <span class="market-tag">B2B: {row.get('B2B', 'Active')}</span>
                    <span class="market-tag">B2W: {row.get('B2W', 'Active')}</span>
                </div>
                <p style="font-size:10px; margin-top:10px; color:#ef394e;">کانال: {row['Market']}</p>
            </div>
            """, unsafe_allow_html=True)

    # جدول نهایی مشابه لیست کالاهای دیجی‌کالا
    st.write(" ")
    st.table(df[['Brand', 'Share', 'Market', 'B2B']])
