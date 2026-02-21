import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اصلی صفحه
st.set_page_config(page_title="Solico Plus Analysis 2026", layout="wide")

# استایل اختصاصی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #ffffff; }
    .product-box { border: 2px solid #ef394e; border-radius: 15px; padding: 20px; background: #fffcfc; margin-bottom: 20px; }
    .brand-analysis { background: #f0f2f5; padding: 15px; border-radius: 10px; border-right: 5px solid #333; }
    .price-tag { color: #ef394e; font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ۱. استخراج دیتای واقعی از فایل ارسالی (Solico Plus Feb 2026)
# این دیتا مستقیماً از متن فایل استخراج شده است
RAW_DATA = [
    # سس‌ها
    {"کد": "30019555", "نام": "سس کچاپ بطری 800 گرمی", "فروش": 1850000, "خرید": 1622807, "سود": 14, "برند": "سولیکو (سس)"},
    {"کد": "30019558", "نام": "مایونز پرچرب پت جار 900 گرمی", "فروش": 4650000, "خرید": 4078947, "سود": 14, "برند": "سولیکو (سس)"},
    {"کد": "30003089", "نام": "مایونز کم‌چرب پت 250", "فروش": 2850000, "خرید": 2500000, "سود": 14, "برند": "سولیکو (سس)"},
    {"کد": "30002707", "نام": "مایونز پرچرب دبه", "فروش": 10158000, "خرید": 8910526, "سود": 14, "برند": "فله / رستورانی"},
    
    # پروتئینی (دار فرش و توری)
    {"کد": "30012185", "نام": "بیکن ایرلندی دار فرش", "فروش": 5622807, "خرید": 4950000, "سود": 12, "برند": "دار فرش (Premium)"},
    {"کد": "30013946", "نام": "مارشن دار فرش", "فروش": 5271929, "خرید": 4624500, "سود": 14, "برند": "دار فرش (Premium)"},
    {"کد": "20011844", "نام": "هات داگ پنیری توری", "فروش": 6570176, "خرید": 5763312, "سود": 12, "برند": "کاله (توری)"},
    {"کد": "30005468", "نام": "هات داگ 170 توری", "فروش": 9230000, "خرید": 8372930, "سود": 13, "برند": "کاله (توری)"},
    
    # زیتون و تن
    {"کد": "20001518", "نام": "تن ماهی 400 گرمی کاله", "فروش": 1699000, "خرید": 1461140, "سود": 14, "برند": "سولیکو (کنسرو)"},
    {"کد": "20012692", "نام": "زیتون پرورده 2000 گرمی", "فروش": 9000000, "خرید": 7824088, "سود": 13, "برند": "سولیکو (زیتون)"},
    {"کد": "30014581", "نام": "زیتون پرورده 80 گرمی", "فروش": 400000, "خرید": 347817, "سود": 12, "برند": "سولیکو (زیتون)"}
]

df_main = pd.DataFrame(RAW_DATA)

# هدر اپلیکیشن
st.markdown("<h1 style='text-align: center; color: #ef394e;'>🔍 جستجوگر عمیق محصولات سولیکو پلاس</h1>", unsafe_allow_html=True)
st.write("---")

# جستجو بر اساس نام کالا
search_query = st.text_input("📍 نام کالا یا بخشی از آن را وارد کنید (مثلاً: بیکن، مایونز، تن ماهی):", "")

# شرط: تا کالا وارد نشده هیچ خروجی نده
if search_query:
    # فیلتر کردن دیتا
    results = df_main[df_main['نام'].str.contains(search_query, na=False)]
    
    if not results.empty:
        st.success(f"تعداد {len(results)} مورد یافت شد:")
        
        for index, row in results.iterrows():
            st.markdown(f"""
            <div class="product-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 style="color: #333;">📦 {row['نام']}</h2>
                    <span style="background:#ef394e; color:white; padding:5px 15px; border-radius:20px;">کد: {row['کد']}</span>
                </div>
                <hr>
                <div style="display:flex; justify-content:space-around; text-align:center;">
                    <div><p>قیمت فروش (ریال)</p><p class="price-tag">{row['فروش']:,}</p></div>
                    <div><p>قیمت خرید (ریال)</p><p style="font-size:20px; color:#555;">{row['خرید']:,}</p></div>
                    <div><p>حاشیه سود درصد</p><p style="font-size:20px; color:green; font-weight:bold;">{row['سود']}%</p></div>
                </div>
                <div class="brand-analysis" style="margin-top:20px;">
                    <h4>🏛️ موشکافی برند و جایگاه بازار:</h4>
                    <p><b>نام برند:</b> {row['برند']}</p>
                    <p><b>وضعیت رقابتی:</b> این کالا در لیست قیمت 2026 جزو اقلام استراتژیک با حاشیه سود {row['سود']} درصد تعریف شده است.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # نمودار مقایسه‌ای کوچک برای هر کالا
            plot_data = pd.DataFrame({
                'نوع قیمت': ['خرید', 'فروش'],
                'مبلغ (ریال)': [row['خرید'], row['فروش']]
            })
            fig = px.bar(plot_data, x='نوع قیمت', y='مبلغ (ریال)', text='مبلغ (ریال)', 
                         color='نوع قیمت', color_discrete_map={'خرید': '#333', 'فروش': '#ef394e'})
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.warning("کالایی با این نام در دیتابیس ۲۰۲۶ یافت نشد.")
else:
    st.info("💡 منتظر ورود نام کالا هستیم... (لطفاً در کادر بالا تایپ کنید)")

