
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# تنظیمات اصلی صفحه
st.set_page_config(page_title="Solico Super App", layout="wide")

# استایل فوق حرفه‌ای مشابه اپلیکیشن‌های موبایل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', sans-serif;
        background-color: #f0f2f5;
        direction: rtl;
    }

    /* هدر دیجی‌کالایی */
    .header-box {
        background-color: #ef394e;
        padding: 20px;
        color: white;
        text-align: center;
        border-radius: 0 0 25px 25px;
        box-shadow: 0 4px 15px rgba(239, 57, 78, 0.3);
        margin-bottom: 25px;
    }
    .user-tag { font-size: 10px; opacity: 0.8; font-weight: 100; letter-spacing: 0.5px; margin-top: 5px; display: block; }

    /* کارت‌های دیتای پایین صفحه - خوانایی بالا */
    .info-card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .label-text { color: #7a7a7a; font-size: 13px; font-weight: 400; display: block; margin-bottom: 2px; }
    .value-text { color: #1a1c22; font-size: 16px; font-weight: 700; display: block; margin-bottom: 12px; }
    
    /* استایل آیکون‌های دسته‌بندی دایره‌ای */
    .cat-container { display: flex; justify-content: space-around; margin-bottom: 25px; background: white; padding: 15px; border-radius: 15px; }
    .cat-circle {
        width: 55px; height: 55px;
        background: #fff; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        border: 2px solid #ef394e; font-size: 22px; margin: 0 auto;
    }
    </style>

    <div class="header-box">
        <div style="font-size: 22px; font-weight: 700;">SOLICO INTELLIGENCE APP</div>
        <span class="user-tag">behr.khosravi@solico-group.ir</span>
    </div>
    """, unsafe_allow_html=True)

# دیتابیس لوگوها
LOGOS = {
    "کاله": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Kalleh_Logo.svg/1200px-Kalleh_Logo.svg.png",
    "مهرام": "https://mahramco.com/wp-content/uploads/2021/05/logo-mahram.png",
    "دلپذیر": "https://delpazir.com/wp-content/themes/delpazir/assets/images/logo.png",
    "آندره": "https://andrefood.com/wp-content/uploads/2021/03/Andre-Logo-1.png",
    "بیژن": "https://bijanfoods.com/wp-content/uploads/2022/07/logo.png",
    "طبیعت": "https://tabiat.ir/wp-content/uploads/2020/06/logo.png"
}

def get_market_intelligence(query):
    q = query.strip()
    # تحلیل هوشمند محصولات
    if any(x in q for x in ["سس", "مایونز", "کچاپ"]):
        data = [
            {'Brand': 'دلپذیر', 'Share': 35, 'City': 'سراسری', 'B2B': 'قوی (رستوران)', 'B2W': 'بنکداری برتر', 'Target': 'بازار انبوه'},
            {'Brand': 'مهرام', 'Share': 30, 'City': 'تهران', 'B2B': 'بسیار فعال', 'B2W': 'مویرگی', 'Target': 'خرده‌فروشی'},
            {'Brand': 'کاله', 'Share': 18, 'City': 'شمال', 'B2B': 'تخصصی کترینگ', 'B2W': 'سیستمی', 'Target': 'پرایم'}
        ]
        msg = "💡 پیشنهاد مدیریت: تمرکز بر سس‌های ساشه برای لاین B2B هتل‌ها."
    elif any(x in q for x in ["سوسیس", "کالباس", "سوجوک", "کوکتل"]):
        data = [
            {'Brand': 'کاله', 'Share': 42, 'City': 'ایران', 'B2B': 'لیدر بازار', 'B2W': 'هوشمند', 'Target': 'کل بازار'},
            {'Brand': 'آندره', 'Share': 22, 'City': 'تهران', 'B2B': 'لوکس/HoReCa', 'B2W': 'محدود', 'Target': 'پروتئینی‌ها'}
        ]
        msg = "💡 پیشنهاد مدیریت: تقویت لاین سوجوک در بازارهای محلی غرب کشور."
    elif any(x in q for x in ["تن", "ماهی", "زیتون"]):
        data = [
            {'Brand': 'طبیعت', 'Share': 40, 'City': 'کشوری', 'B2B': 'سازمانی', 'B2W': 'بسیار قوی', 'Target': 'هایپرمارکت'},
            {'Brand': 'تحفه', 'Share': 28, 'City': 'جنوب', 'B2B': 'صادراتی', 'B2W': 'فعال', 'Target': 'آنلاین'}
        ]
        msg = "💡 پیشنهاد مدیریت: تنوع در طعم‌های فلفلی و رژیمی برای جذب نسل جوان."
    else: return None, None
    return pd.DataFrame(data), msg

# ردیف آیکون‌ها (Category Menu)
st.markdown('<div class="cat-container">', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.markdown('<div class="cat-circle">🥫</div><p style="text-align:center; font-size:12px; font-weight:bold;">سس</p>', unsafe_allow_html=True)
with c2: st.markdown('<div class="cat-circle">🥩</div><p style="text-align:center; font-size:12px; font-weight:bold;">گوشتی</p>', unsafe_allow_html=True)
with c3: st.markdown('<div class="cat-circle">🐟</div><p style="text-align:center; font-size:12px; font-weight:bold;">کنسرو</p>', unsafe_allow_html=True)
with c4: st.markdown('<div class="cat-circle">🫒</div><p style="text-align:center; font-size:12px; font-weight:bold;">زیتون</p>', unsafe_allow_html=True)
with c5: st.markdown('<div class="cat-circle">🥛</div><p style="text-align:center; font-size:12px; font-weight:bold;">لبنیات</p>', unsafe_allow_html=True)

# کادر جستجو
search_val = st.text_input("", placeholder="نام محصول را وارد کنید (مثلاً: سس مایونز یا کوکتل)")

if search_val:
    df, strategy_msg = get_market_intelligence(search_val)
    if df is not None:
