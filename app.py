import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Market Intelligence Matrix", layout="wide")

# 2. CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .title-text {
        background: linear-gradient(45deg, #00d4ff, #004e92);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: 900; text-align: center;
    }
    .stTable { background-color: #161b22; border-radius: 10px; }
    </style>
    <p class="title-text">MARKET INTELLIGENCE MATRIX</p>
    """, unsafe_allow_html=True)

# 3. Data Extraction (Prices from your PDF & Screenshots)
# Prices for Kalleh/Solico are from your uploaded PDF (Feb 2026)
# Competitor prices are from your Torob/Emalls screenshots
SOLICO_DATA = {
    "sauce": {
        "leader": "مهرام",
        "analysis": "در بازار سس، مهرام لیدر توزیع مویرگی است. کاله (سولیکو) در بخش دبه و تامین B2B با قیمت‌های رقابتی نفوذ بالایی دارد.",
        "products": [
            [span_2](start_span){"name": "سس مایونز پرچرب دبه (سولیکو)", "price": 10158000, "channel": "B2B / رستوران"}, #[span_2](end_span)
            {"name": "سس مایونز ۹۷۰ گرمی (مهرام)", "price": 520000, "channel": "زنجیره‌ای / سوپرمارکت"}, # From Screenshot
            [span_3](start_span){"name": "سس کچاپ ۸۰۰ گرمی (سولیکو)", "price": 1250000, "channel": "زنجیره‌ای / B2W"}, #[span_3](end_span)
            {"name": "سس مایونز کتوئی ۲۵۰ سی‌سی", "price": 117000, "channel": "آنلاین / رژیمی"}, # From Screenshot
            [span_4](start_span){"name": "سس خردل دبه (سولیکو)", "price": 22880702, "channel": "B2B / صنعتی"} #[span_4](end_span)
        ]
    },
    "protein": {
        "leader": "سولیکو (کاله)",
        "analysis": "سولیکو لیدر حجم بازار است. آندره در کانال پروتئینی‌های لوکس و تخصصی لیدر است و قیمت‌های پریمیوم دارد.",
        "products": [
            [span_5](start_span){"name": "ژامبون مرغ دار فرش (سولیکو)", "price": 2736842, "channel": "زنجیره‌ای / سراسری"}, #[span_5](end_span)
            [span_6](start_span){"name": "ژامبون نوروزی (سولیکو)", "price": 5578947, "channel": "B2W / سازمان‌ها"}, #[span_6](end_span)
            {"name": "آندره (پروتئینی لوکس)", "price": 3150000, "channel": "پروتئینی لوکس / B2B"}, # Market Intelligence
            [span_7](start_span){"name": "سوسیس آلمانی (سولیکو)", "price": 4550000, "channel": "سوپرمارکتی / اقتصادی"}, #[span_7](end_span)
            [span_8](start_span){"name": "زیتون پرورده ۲۰۰ گرمی (کاله)", "price": 1739131, "channel": "زنجیره‌ای / سوپرمارکت"} #[span_8](end_span)
        ]
    }
}

# 4. Search & UI Logic
query = st.text_input("🔍 جستجوی محصول (مانند: مایونز، ژامبون، سس):").lower()

if query:
    # Determine Category
    category_key = "sauce" if any(x in query for x in ["سس", "مایونز", "کچاپ", "خردل"]) else "protein"
    selected_data = SOLICO_DATA[category_key]
    
    # 5. Display Analytics based on Category
    st.markdown(f"### 📊 تحلیل تخصصی بازار {('سس' if category_key == 'sauce' else 'محصولات پروتئینی')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("لیدر ایران", selected_data["leader"])
    with col2:
        st.metric("وضعیت نفوذ", "B2B & B2W Active")

    # 6. Strategic Table
    df = pd.DataFrame(selected_data["products"])
    st.table(df.rename(columns={
        "name": "نام محصول / برند", 
        "price": "قیمت (ریال/تومان)", 
        "channel": "کانال نفوذ اصلی"
    }))

    # 7. Gemini Strategic Insight (Category Specific)
    st.markdown("---")
    st.markdown("### 🤖 تحلیل استراتژیک جمینای")
    st.info(selected_data["analysis"])
    
    # Extra Insight based on your file
    if category_key == "protein":
        [span_9](start_span)st.success("💡 نکته از لیست قیمت: محصولات 'دار فرش' دارای حاشیه سود ۱۲ تا ۱۴ درصد برای عاملین فروش هستند[span_9](end_span).")
    else:
        [span_10](start_span)st.success("💡 نکته از لیست قیمت: سس‌های دبه‌ای سولیکو با حاشیه سود ۱۴ درصد، قیمت مرجع بازار B2B محسوب می‌شوند[span_10](end_span).")

else:
    st.warning("👈 نام یک محصول را وارد کنید تا ماتریکس اطلاعات لیدرها و قیمت‌ها نمایش داده شود.")
