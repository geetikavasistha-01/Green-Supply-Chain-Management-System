import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# ---- AUTHENTICATION ----
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {name}!")

    # ---- MONGODB CONNECTION ----
    client = MongoClient("mongodb+srv://geetikavasistha13:01gWVJgQKVqOgUes@gscms.ph6se0s.mongodb.net/")
    db = client["gscms"]
    suppliers_col = db["suppliers"]
    manufacturers_col = db["manufacturers"]
    products_col = db["products"]

    # ---- UI LAYOUT ----
    st.set_page_config(page_title="GSCMS", layout="wide")
    st.markdown("<h1 style='text-align: center; color: lightgreen;'>🌿 Green Supply Chain Management System (GSCMS)</h1>", unsafe_allow_html=True)
    tabs = ["Dashboard", "Suppliers", "Manufacturers", "Products"]
    selected_tab = st.sidebar.radio("📂 Navigation", tabs)

    # ---- DASHBOARD TAB ----
    if selected_tab == "Dashboard":
        st.subheader("📊 Sustainability Dashboard")

        eco_data = {
            "Supplier": ["EcoTex", "GreenPlast", "BioLogix", "SunRenew"],
            "Carbon Emission (kg CO2)": [120, 80, 40, 20],
            "Recyclable Material (%)": [60, 70, 90, 85],
            "Renewable Energy Usage (%)": [50, 65, 80, 95],
        }
        df_eco = pd.DataFrame(eco_data)

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(px.bar(df_eco, x="Supplier", y="Carbon Emission (kg CO2)", color="Supplier"))
        with col2:
            st.plotly_chart(px.pie(df_eco, names="Supplier", values="Recyclable Material (%)"))

        st.plotly_chart(px.line(df_eco, x="Supplier", y="Renewable Energy Usage (%)"))

    # ---- SUPPLIERS TAB ----
    elif selected_tab == "Suppliers":
        st.subheader("🏭 Manage Suppliers")
        with st.expander("➕ Add New Supplier"):
            name = st.text_input("Name")
            location = st.text_input("Location")
            compliance = st.slider("Green Compliance (%)", 0, 100)
            if st.button("Save Supplier"):
                suppliers_col.insert_one({"name": name, "location": location, "compliance": compliance})
                st.success("Supplier saved!")

        with st.expander("📄 View All"):
            data = list(suppliers_col.find({}, {"_id": 0}))
            st.dataframe(pd.DataFrame(data))

    # ---- MANUFACTURERS TAB ----
    elif selected_tab == "Manufacturers":
        st.subheader("🏗️ Manage Manufacturers")
        with st.expander("➕ Add Manufacturer"):
            name = st.text_input("Manufacturer Name")
            eco_rating = st.slider("Eco Rating", 1, 5)
            certs = st.text_input("Certifications")
            if st.button("Save Manufacturer"):
                manufacturers_col.insert_one({"name": name, "eco_rating": eco_rating, "certs": certs})
                st.success("Manufacturer saved!")

        with st.expander("📄 View All"):
            data = list(manufacturers_col.find({}, {"_id": 0}))
            st.dataframe(pd.DataFrame(data))

    # ---- PRODUCTS TAB ----
    elif selected_tab == "Products":
        st.subheader("📦 Manage Products")
        with st.expander("➕ Add Product"):
            pname = st.text_input("Product Name")
            eco_score = st.slider("Eco Score", 0, 100)
            origin = st.text_input("Origin Country")
            if st.button("Save Product"):
                products_col.insert_one({"name": pname, "eco_score": eco_score, "origin": origin})
                st.success("Product saved!")

        with st.expander("📄 View All"):
            data = list(products_col.find({}, {"_id": 0}))
            st.dataframe(pd.DataFrame(data))

else:
    st.error("Please login to continue.")

