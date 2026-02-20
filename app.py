import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# تنظیمات مدیریتی سولیکو
st.set_page_config(page_title="Solico Strategic Dashboard", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Tahoma', sans-serif; font-size: 12px; background-color: #0b0b0b; color: #eee; }
    .header { background: linear-gradient(90deg, #b11e22, #000); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
    .stTextInput>div>div>input { text-align: right; direction: rtl; }
    .kpi-box { background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; text-align: center; }
    </style>
    <div class="header"><h2 style="color:white; margin:0;">SOLICO GROUP INTELLIGENCE</h2></div>
    """, unsafe_allow_html=True)

def get_data(q):
    if any(x in q for x in ["سوسیس", "کالباس", "کوکتل", "نوروزی", "پنیری"]):
        return pd.DataFrame({'برند': ['سولیکو (کاله)', 'گوشتیران', '202', 'آندره'], 'قیمت_ریال': [1980000, 1820000, 2150000, 2300000], 'سهم_بازار': [46, 21, 15, 12], 'محبوبیت': [98, 75, 84, 90]})
    elif "سس" in q:
        return pd.DataFrame({'برند': ['دلپذیر', 'سولیکو (کاله)', 'بیژن', 'مهرام'], 'قیمت_ریال': [620000, 680000, 640000, 650000], 'سهم_بازار': [34, 27, 20, 10], 'محبوبیت': [92, 90, 94, 78]})
    return pd.DataFrame()

query = st.text_input("جستجوی محصول (مثلاً: کوکتل پنیری، سس کچاپ):")

if query:
    df = get_data(query)
    if not df.empty:
        st.info(f"تحلیل هوشمند: برند {df.iloc[df['سهم_بازار'].idxmax()]['برند']} لیدر فعلی بازار در بخش {query} است.")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='kpi-box'>لیدر بازار<br><h3 style='color:#00ffcc;'>{df.iloc[df['سهم_بازار'].idxmax()]['برند']}</h3></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='kpi-box'>میانگین قیمت آنلاین<br><h3 style='color:#00ffcc;'>{df['قیمت_ریال'].mean():,.0f}</h3></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='kpi-box'>محبوبیت مجازی<br><h3 style='color:#00ffcc;'>{df.iloc[df['محبوبیت'].idxmax()]['برند']}</h3></div>", unsafe_allow_html=True)
        
        fig = px.pie(df, values='سهم_بازار', names='برند', hole=0.4, title="سهم بازار برندهای داخلی", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        st.table(df)
