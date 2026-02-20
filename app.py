import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# تنظیمات اصلی صفحه
st.set_page_config(page_title="Solico Super App", layout="wide")

# استایل اختصاصی ترکیبی دیجی‌کالا و پاور بی‌آی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', sans-serif;
        background-color: #f8f8f8;
        direction: rtl;
    }

    /* هدر قرمز دیجی کالا */
    .dk-header {
        background-color: #ef394e;
        padding: 15px;
        color: white;
        text-align: center;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .user-mail { font-size: 11px; opacity: 0.9; font-weight: 100; letter-spacing: 1px; }

    /* کارت‌های شاخص‌های کلیدی (Metrics) */
    .metric-container {
        background: white;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #e0e0e0;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* استایل فونت‌های پایین صفحه - خوانایی حداکثری */
    .brand-title { color: #ef394e; font-weight: 700; font-size: 18px; margin-bottom: 10px; }
    .info-label { color: #5a5a5a; font-size: 14px; font-weight: 400; }
    .info-value { color: #1a1a1a; font-size: 15px; font-weight: 700; display: block; margin-bottom: 8px; border-bottom: 1px solid #f0f0f0; padding-bottom: 4px;}

    /* دسته‌بندی دایره‌ای */
    .cat-item { text-align: center; margin-bottom: 20px; }
    .cat-circle {
        width: 60px; height: 60px; 
        background: white; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        font-size: 25px; border: 2px solid #ef394e;
    }
    </style>

    <div class="dk-header">
        <div style="font-size: 20px; font-weight: 700;">SOLICO GROUP INTELLIGENCE</div>
        <div class="user-email">By: behr.khosravi@solico-group.ir</div>
        <div style="margin-top:10px; font-size:12px;">📍 انتخاب منطقه: سراسر ایران</div>
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
    "طبیعت": "https://tabiat.ir/wp-content/uploads/2020/06/logo.png"
}

def get_data(query):
    q = query.strip()
    if any(x in q for x in ["سس", "مایونز", "کچاپ"]):
        data = [
            {'Brand': 'مهرام', 'Share': 34, 'City': 'تهران', 'B2B': 'بسیار فعال', 'B2W': 'توزیع مویرگی', 'Target': 'رستوران‌ها'},
            {'Brand': 'دلپذیر', 'Share': 31, 'City': 'مشهد', 'B2B': 'متوسط', 'B2W': 'بنکداری قوی', 'Target': 'هایپرمارکت'},
            {'Brand': 'کاله', 'Share': 20, 'City': 'آمل/شمال', 'B2B': 'تخصصی', 'B2W': 'سیستمی', 'Target': 'خرده‌فروشی'}
        ]
        strat = "تمرکز بر سس‌های تک‌نفره برای بخش B2B (فست‌فودها)."
    elif any(x in q for x in ["سوسیس", "کالباس", "سوجوک", "پروتئین"]):
        data = [
            {'Brand': 'سولیکو (کاله)', 'Share': 45, 'City': 'کشوری', 'B2B': 'حاکم بازار', 'B2W': 'هوشمند', 'Target': 'همه کانال‌ها'},
            {'Brand': 'آندره', 'Share': 25, 'City': 'تهران', 'B2B': 'لوکس/هتل', 'B2W': 'محدود', 'Target': 'پروتئینی‌ها'},
            {'Brand': '۲۰۲', 'Share': 15, 'City': 'کرج', 'B2B': 'فعال', 'B2W': 'قوی', 'Target': 'فروشگاهی'}
        ]
        strat = "توسعه سوجوک و محصولات تخصصی برای تمایز در بازار B2B."
    elif any(x in q for x in ["تن", "ماهی", "زیتون"]):
        data = [
            {'Brand': 'طبیعت', 'Share': 38, 'City': 'سراسری', 'B2B': 'سازمانی', 'B2W': 'بسیار قوی', 'Target': 'عمده فروشی'},
            {'Brand': 'تحفه', 'Share': 30, 'City': 'جنوب', 'B2B': 'صادراتی', 'B2W': 'فعال', 'Target': 'فروشگاه زنجیره‌ای'}
        ]
        strat = "افزایش تنوع در بسته‌بندی‌های زیتون برای لاین کترینگ و هتل‌ها."
    else: return None, None
    return pd.DataFrame(data), strat

# ردیف آیکون‌های دسته‌بندی (دقیقاً مثل اپ دیجی‌کالا)
cols_cat = st.columns(5)
categories = [("سس", "🥫"), ("گوشتی", "🥩"), ("کنسرو", "🐟"), ("زیتون", "🫒"), ("لبنیات", "🥛")]
for i, (name, icon) in enumerate(categories):
    with cols_cat[i]:
        st.markdown(f'<div class="cat-item"><div class="cat-circle">{icon}</div><div style="font-size:12px;margin-top:5px;font-weight:bold;color:#444;">{name}</div></div>', unsafe_allow_html=True)

# جستجو با استایل گرد
search_q = st.text_input("", placeholder="🔍 جستجو در تمامی محصولات سولیکو و رقبا...")

if search_q:
    df, strategy = get_data(search_q)
    if df is not None:
        # کارت شگفت‌انگیز (لیدر بازار)
        st.markdown(f"""
        <div style="background:#ef394e; color:white; padding:15px; border-radius:15px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:18px; font-weight:bold;">🏆 لیدر فعلی بازار: {df.iloc[0]['Brand']}</span><br>
                <span style="font-size:12px;">{strategy}</span>
            </div>
            <img src="{BRAND_LOGOS.get(df.iloc[0]['Brand'])}" width="60" style="background:white; border-radius:10px; padding:5px;">
        </div>
        """, unsafe_allow_html=True)

        # بخش نمودارها (Power BI Style)
        st.write("### 📊 تحلیل دیتامحور (Data Analytics)")
        c1, c2 = st.columns([1, 1])
        with c1:
            fig = px.pie(df, values='Share', names='Brand', hole=0.6, color_discrete_sequence=['#ef394e', '#333', '#888'])
            fig.update_layout(showlegend=False, height=250, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
                    with c2:
            fig2 = px.bar(df, x='Brand', y='Share', color='Brand', color_discrete_sequence=['#ef394e'])
            fig2.update_layout(showlegend=False, height=250, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)
            
        # بخش اطلاعات تفصیلی (خوانایی اصلاح شده)
        st.write("---")
        st.write("### 🏢 جزئیات عملیاتی و کانال‌های فروش")
        
        # نمایش کارت‌ها
        card_cols = st.columns(len(df))
        for i, row in df.iterrows():
            with card_cols[i]:
                logo_url = BRAND_LOGOS.get(row['Brand'], "https://via.placeholder.com/100")
                st.markdown(f"""
                <div style="background:white; border-radius:15px; padding:20px; border:1px solid #eee; min-height:350px;">
                    <div style="text-align:center;">
                        <img src="{logo_url}" width="70" style="margin-bottom:10px;">
                        <div class="brand-title">{row['Brand']}</div>
                    </div>
                    <div style="margin-top:15px;">
                        <span class="info-label">📍 شهر لیدر:</span>
                        <span class="info-value">{row['City']}</span>
                        
                        <span class="info-label">🏢 وضعیت B2B:</span>
                        <span class="info-value">{row['B2B']}</span>
                        
                        <span class="info-label">🚚 وضعیت B2W:</span>
                        <span class="info-value">{row['B2W']}</span>
                        
                        <span class="info-label">🎯 تمرکز بازار:</span>
                        <span class="info-value">{row['Target']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.error("محصولی یافت نشد. (سس، سوسیس، تن ماهی یا زیتون را امتحان کنید)")

