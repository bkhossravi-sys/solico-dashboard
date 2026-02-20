import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اصلی
st.set_page_config(page_title="Solico Market Intelligence", layout="wide")

# استایل اختصاصی (ترکیب دیجی‌کالا و اسنپ)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; background-color: #f5f5f5; direction: rtl; }
    
    /* هدر اپلیکیشنی */
    .app-header {
        background: #ef394e; padding: 20px; color: white; text-align: center;
        border-radius: 0 0 25px 25px; box-shadow: 0 4px 12px rgba(239, 57, 78, 0.2);
    }
    
    /* کارت‌های اسنپی */
    .factory-card {
        background: white; border-radius: 15px; padding: 18px;
        border-right: 6px solid #ef394e; margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .brand-name { color: #ef394e; font-size: 20px; font-weight: 700; margin-bottom: 8px; }
    .contact-info { font-size: 13px; color: #555; line-height: 1.6; }
    .badge { background: #fceef0; color: #ef394e; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: bold; }
    
    /* آیکون‌های گرد بالای صفحه */
    .top-nav { display: flex; justify-content: space-around; padding: 15px 0; background: white; margin-bottom: 20px; border-radius: 0 0 15px 15px; }
    .nav-item { text-align: center; width: 70px; }
    .nav-icon { width: 50px; height: 50px; background
