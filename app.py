# app.py
import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))
from tracker import get_all_prices

from utils import send_email

st.set_page_config(page_title="🍭 Price Tracker", layout="wide")
st.title("🍭 Amazon Price Tracker (1000+ Products)")
st.caption("Monitor multiple product prices and get alerts!")

try:
    products_df = pd.read_csv("products.csv")
    st.write("✅ Loaded products:", products_df.shape)

    if products_df.empty:
        st.warning("The product list is empty. Please check your CSV.")
    else:
        url_list = products_df["url"].tolist()

        st.info("🔄 Fetching current prices... Please wait.")
        results = get_all_prices(url_list)

        data = []
        for i, product in enumerate(results):
            target_price = products_df.iloc[i]["target_price"]
            alert = product["price"] and product["price"] <= target_price
            data.append({
                "Product": product["title"],
                "Current Price": product["price"],
                "Target Price": target_price,
                "Buy Link": product["url"],
                "Alert": "✅ YES" if alert else "❌ NO"
            })

        df = pd.DataFrame(data)
        st.dataframe(df)

        st.subheader("📬 Get Price Drop Alerts")
        email_input = st.text_input("Your Email Address")

        if st.button("Send Alerts"):
            alert_rows = df[df["Alert"] == "✅ YES"]
            if not alert_rows.empty:
                for row in alert_rows.itertuples():
                    send_email(
                        subject=f"Price Drop Alert: {row.Product}",
                        body=f"{row.Product} is now ₹{row._2}\nBuy here: {row._4}",
                        to_email=email_input
                    )
                st.success("📩 Alerts sent successfully!")
            else:
                st.info("😕 No products currently below target price.")
except Exception as e:
    st.error(f"An error occurred: {e}")
