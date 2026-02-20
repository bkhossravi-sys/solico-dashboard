import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# تنظیمات اصلی صفحه
st.set_page_config(page_title="Iran Market SuperApp", layout="wide")

# طراحی گرافیکی مشابه دیجی‌کالا (قرمز و سفید با کارت‌های سایه‌دار)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; background-color: #f0f2f5; color: #333; }
    .main-header { background-color: #fff; padding: 15px; border-bottom: 3px solid #ef394e; text-align: center; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .dk-logo { color: #ef394e; font-size: 28px; font-weight: 900; letter-spacing: -1px; }
    .stTextInput>div>div>input { border-radius: 25px !important; border: 2px solid #ef394e !important; padding: 20px; font-size: 16px; text-align: right; }
    .card { background: white; border-radius: 15px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 20px; direction: rtl; }
    .strategy-text { border-right: 5px solid #ef394e; padding-right: 15px; font-size: 15px; line-height: 1.8; color: #444; }
    .brand-badge { display: inline-block; background: #fff0f1; color: #ef394e; padding: 5px 15px; border-radius: 8px; font-weight: bold; margin-bottom: 10px; }
    .market-tag { background: #f4f4f4; padding: 3px 10px; border-radius: 5px; font-size: 11px; margin-left: 5px; border: 1px solid #ddd; }
    </style>
    <div class="main-header"><span class="dk-logo">MARKET INTELLIGENCE SUPER-APP</span></div>
    """, unsafe_allow_html=True)

# دیتابیس جامع و هوشمند برندها و لوگوها
BRAND_LOGOS = {
    "کاله": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Kalleh_Logo.svg/1200px-Kalleh_Logo.svg.png",
    "سولیکو (کاله)": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Kalleh_Logo.svg/1200px-Kalleh_Logo.svg.png",
    "مهرام": "https://mahramco.com/wp-content/uploads/2021/05/logo-mahram.png",
    "دلپذیر": "https://delpazir.com/wp-content/themes/delpazir/assets/images/logo.png",
    "آندره": "https://andrefood.com/wp-content/uploads/2021/03/Andre-Logo-1.png",
    "۲۰۲": "https://202.ir/wp-content/uploads/2021/05/logo.png",
    "بیژن": "https://bijanfoods.com/wp-content/uploads/2022/07/logo.png",
    "طبیعت": "https://tabiat.ir/wp-content/uploads/2020/06/logo.png",
    "تحفه": "https://tofeh.com/wp-content/uploads/2020/05/logo.png"
}

def get_market_analysis(query):
    q = query.strip()
    # دسته سس‌ها
    if any(x in q for x in ["سس", "مایونز", "کچاپ"]):
        data = [
            {'Brand': 'مهرام', 'Share': 33, 'Lead_City': 'تهران/اصفهان', 'B2B': 'بسیار فعال (رستوران‌ها)', 'B2W': 'قوی', 'Channel': 'سوپرمارکتی'},
            {'Brand': 'دلپذیر', 'Share': 30, 'Lead_City': 'سراسری/جنوب', 'B2B': 'متوسط', 'B2W': 'بسیار قوی (بنکداری)', 'Channel': 'هایپرمارکتی'},
            {'Brand': 'بیژن', 'Share': 15, 'Lead_City': 'غرب کشور', 'B2B': 'فعال', 'B2W': 'متوسط', 'Channel': 'خرده‌فروشی'},
            {'Brand': 'کاله', 'Share': 12, 'Lead_City': 'شمال ایران', 'B2B': 'تخصصی', 'B2W': 'فعال', 'Channel': 'زنجیره‌ای'}
        ]
        strategy = "تمرکز بر توزیع مویرگی در شهرهای گروه B و استفاده از بسته‌بندی‌های گالنی برای تقویت بخش B2B (فست‌فودها)."
    
    # دسته گوشتی
    elif any(x in q for x in ["سوسیس", "کالباس", "سوجوک", "کوکتل", "آندره"]):
        data = [
            {'Brand': 'سولیکو (کاله)', 'Share': 38, 'Lead_City': 'سراسری', 'B2B': 'بسیار قوی', 'B2W': 'سیستمی', 'Channel': 'سوپرمارکتی'},
            {'Brand': 'آندره', 'Share': 20, 'Lead_City': 'تهران (لوکس)', 'B2B': 'هتل‌ها/رستوران‌ها', 'B2W': 'متوسط', 'Channel': 'پروتئینی تخصصی'},
            {'Brand': '۲۰۲', 'Share': 17, 'Lead_City': 'کرج/تهران', 'B2B': 'فعال', 'B2W': 'قوی', 'Channel': 'فروشگاه زنجیره‌ای'},
            {'Brand': 'بشارت', 'Share': 10, 'Lead_City': 'تبریز/شمال‌غرب', 'B2B': 'منطقه‌ای', 'B2W': 'سنتی', 'Channel': 'بازار محلی'}
        ]
        strategy = "ارتقای حاشیه سود با تمرکز بر محصولات سلامت‌محور (درصد گوشت بالا) و ایجاد نمایندگی‌های انحصاری در مراکز استان‌های پرجمعیت."

    # دسته تن‌ماهی و زیتون
    elif any(x in q for x in ["تن", "ماهی", "زیتون"]):
        data = [
            {'Brand': 'طبیعت', 'Share': 35, 'Lead_City': 'سراسری', 'B2B': 'دولتی/سازمانی', 'B2W': 'بسیار قوی', 'Channel': 'هایپرمارکتی'},
            {'Brand': 'تحفه', 'Share': 28, 'Lead_City': 'تهران/جنوب', 'B2B': 'تخصصی', 'B2W': 'قوی', 'Channel': 'آنلاین/زنجیره‌ای'},
            {'Brand': 'مکنزی', 'Share': 15, 'Lead_City': 'مرکز ایران', 'B2B': 'متوسط', 'B2W': 'فعال', 'Channel': 'سوپرمارکتی'}
        ]
        strategy = "بهینه‌سازی زنجیره تأمین مواد اولیه و استفاده از تخفیفات حجمی (Quantity Discount) در کانال B2W برای تسلط بر شلف سوپرمارکت‌ها."
    
    else:
        return None, "محصول یافت نشد. لطفاً دسته‌بندی درستی (سس، سوسیس، تن ماهی و...) وارد کنید."

    return pd.DataFrame(data), strategy

# رابط کاربری
st.write("### 🛍️ جستجوی استراتژیک کالا")
search_input = st.text_input("", placeholder="🔍 نام محصول (مثلاً: سس خردل، سوجوک، تن ماهی یا زیتون) ...")

if search_input:
    df, strategy = get_market_analysis(search_input)
    
    if df is not None:
        # کارت تحلیل مدیریتی
        st.markdown(f"""
        <div class="card">
            <h4 style="color:#ef394e;">📋 گزارش استراتژیک مدیریت بازار:</h4>
            <p class="strategy-text">{strategy}</p>
        </div>
        """, unsafe_allow_html=True)

        # ردیف اول: تحلیل بصری
        st.write("### 📊 ماتریکس پایش سهم بازار")
        c1, c2, c3 = st.columns([2, 1, 1])
        
        with c1:
            fig1 = px.bar(df, x='Brand', y='Share', color='Brand', text='Share', 
                          title="سهم بازار برندهای لیدر (%)", color_discrete_sequence=px.colors.sequential.Reds_r)
            fig1.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
            
        with c2:
            fig2 = px.pie(df, values='Share', names='Brand', hole=0.6, color_discrete_sequence=['#ef394e', '#333', '#666', '#999'])
            fig2.update_layout(height=350, showlegend=False, title="توزیع کل بازار")
            st.plotly_chart(fig2, use_container_width=True)
            
        with c3:
            # شاخص نفوذ استانی (فرضی)
            fig3 = go.Figure(go.Scatterpolar(r=[90, 70, 80, 60], theta=['B2B', 'B2W', 'Retail', 'Online'], fill='toself', line_color='#ef394e'))
            fig3.update_layout(polar=dict(radialaxis=dict(visible=False)), height=350, title="قدرت کانال‌های فروش")
            st.plotly_chart(fig3, use_container_width=True)
            
        # ردیف دوم: کارت‌های برند با لوگو و تفکیک بازار
        st.write("---")
        st.write("### 🏢 شناسنامه عملیاتی برندها")
        
        brand_cols = st.columns(len(df))
        for i, row in df.iterrows():
            with brand_cols[i]:
                logo_url = BRAND_LOGOS.get(row['Brand'], "https://via.placeholder.com/100")
                st.markdown(f"""
                <div style="background:white; border-radius:12px; padding:15px; text-align:center; box-shadow:0 2px 10px rgba(0,0,0,0.05); min-height:280px;">
                    <img src="{logo_url}" width="80" style="margin-bottom:10px;">
                    <div class="brand-badge">{row['Brand']}</div>
                    <p style="font-size:12px;">📍 شهر لیدر: <b>{row['Lead_City']}</b></p>
                    <hr style="margin:10px 0; opacity:0.2;">
                    <div style="text-align:right;">
                        <span class="market-tag">B2B: {row['B2B']}</span><br>
                        <span class="market-tag">B2W: {row['B2W']}</span><br>
                        <span class="market-tag">کانال: {row['Channel']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # جدول داده‌های خام مدیریتی
        st.write(" ")
        st.write("### 📄 جدول مقایسه‌ای عملکرد")
        st.dataframe(df, use_container_width=True)
    else:
        st.error(strategy)

