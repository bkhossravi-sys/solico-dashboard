import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات پیشرفته صفحه برای حالت موبایل
st.set_page_config(page_title="Solico Intelligence Hub", layout="centered")

# استایل CSS برای ظاهر فوق حرفه‌ای (Dark & Premium)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; background-color: #0e1117; color: white; }
    .stTextInput > div > div > input { background-color: #262730; color: white; border-radius: 10px; border: 1px solid #ef394e; }
    .metric-card { background: #1f2129; padding: 15px; border-radius: 15px; border-top: 4px solid #ef394e; text-align: center; margin: 10px 0; }
    .leader-badge { background: #ffd700; color: black; padding: 2px 10px; border-radius: 20px; font-weight: bold; font-size: 12px; }
    .social-score { color: #1da1f2; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# هدر اپلیکیشن
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #ef394e; margin-bottom: 0;">Solico Super App v2.0</h2>
        <p style="font-size: 0.8em; color: #808495;">By: behr.khosravi@solico-group.ir</p>
    </div>
""", unsafe_allow_html=True)

# دیتابیس استخراج شده از فایل Book2.pdf و تحلیل بازار
# [span_0](start_span)قیمت‌ها بر اساس ریال موجود در فایل[span_0](end_span)
market_data = [
    {"Product": "سس مایونز ۹۰۰ گرمی کاله (شیشه‌ای)", "Price": 1041000, "Category": "سس", "Social_Popularity": 85, "Market_Share": 12},
    {"Product": "سس مایونز پرچرب ۹۰۰ گرمی کاله (پت جار)", "Price": 4650000, "Category": "سس", "Social_Popularity": 70, "Market_Share": 5},
    {"Product": "سس کچاپ ۸۰۰ گرمی کاله", "Price": 1750000, "Category": "سس", "Social_Popularity": 92, "Market_Share": 30},
    {"Product": "سس مایونز دبه ۸ کیلویی کوچین", "Price": 8482000, "Category": "سس", "Social_Popularity": 40, "Market_Share": 15},
]

# اطلاعات رقبا (Snapshot بازار آنلاین)
competitors = {
    "سس": {"Leader": "مهرام", "Leader_Share": 32, "Social_Star": "بیژن", "Avg_Discount": "18%"},
    "پروتئینی": {"Leader": "سولیکو (کاله)", "Leader_Share": 46, "Social_Star": "سولیکو", "Avg_Discount": "10%"}
}

# بخش جستجوی هوشمند
search_input = st.text_input("", placeholder="مثلاً: مایونز ۹۰۰ یا کچاپ ۸۰۰...")

if search_input:
    # منطق جستجوی بخشی از کلمات
    keywords = search_input.split()
    results = [item for item in market_data if all(key in item["Product"] for key in keywords)]

    if results:
        for res in results:
            with st.container():
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #ef394e;">{res['Product']}</h3>
                    <div style="display: flex; justify-content: space-around; margin-top: 10px;">
                        <div><p style="margin:0;">قیمت سولیکو</p><strong>{res['Price']:,} ریال</strong></div>
                        <div><p style="margin:0;">سهم بازار</p><strong>{res['Market_Share']}%</strong></div>
                        <div><p style="margin:0;">محبوبیت اجتماعی</p><strong class="social-score">{res['Social_Popularity']}%</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # تحلیل لیدر بازار برای دسته مورد جستجو
        st.write("---")
        cat = results[0]["Category"]
        info = competitors.get(cat)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"🏆 **لیدر بازار {cat}:** {info['Leader']}")
            st.write(f"📊 **سهم لیدر:** {info['Leader_Share']}%")
        with col2:
            st.write(f"🌟 **محبوب‌ترین در شبکه اجتماعی:** {info['Social_Star']}")
            st.write(f"🔴 **میانگین تخفیف رقبا:** {info['Avg_Discount']}")

        # نمودار سهم بازار برندها
        fig = px.bar(pd.DataFrame([{"Brand": info['Leader'], "Share": info['Leader_Share']}, 
                                  {"Brand": "سولیکو", "Share": results[0]['Market_Share']}]),
                     x='Brand', y='Share', color='Brand', 
                     template="plotly_dark", title="مقایسه سهم بازار")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("محصولی با این مشخصات یافت نشد.")
else:
    st.info("💡 نام یا وزن محصول را وارد کنید تا تحلیل لحظه‌ای بازار نمایش داده شود.")
