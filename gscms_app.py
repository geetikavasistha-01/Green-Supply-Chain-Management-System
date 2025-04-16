import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# ---- MONGODB CONNECTION ----
client = MongoClient("mongodb://localhost:27017/")
db = client["gscms"]
suppliers_col = db["suppliers"]

# ---- STREAMLIT SETTINGS ----
st.set_page_config(page_title="GSCMS", layout="wide")
st.markdown("<h1 style='text-align: center; color: lightgreen;'>🌿 Green Supply Chain Management System (GSCMS)</h1>", unsafe_allow_html=True)

# ---- SIDEBAR NAVIGATION ----
tabs = ["Dashboard", "Suppliers", "Manufacturers", "Products", "Transportation", "Audits", "Regulations"]
selected_tab = st.sidebar.radio("Select Section", tabs)

# ---- DASHBOARD TAB ----
if selected_tab == "Dashboard":
    st.subheader("📊 Sustainability Dashboard")

    # Sample Data
    eco_data = {
        "Supplier": ["EcoTex", "GreenPlast", "BioLogix", "SunRenew"],
        "Carbon Emission (kg CO2)": [120, 80, 40, 20],
        "Recyclable Material (%)": [60, 70, 90, 85],
        "Renewable Energy Usage (%)": [50, 65, 80, 95],
    }
    df_eco = pd.DataFrame(eco_data)

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(df_eco, x="Supplier", y="Carbon Emission (kg CO2)", color="Supplier", title="Carbon Emissions by Supplier")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(df_eco, names="Supplier", values="Recyclable Material (%)", title="Recyclable Material Share")
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.line(df_eco, x="Supplier", y="Renewable Energy Usage (%)", title="Renewable Energy Usage")
    st.plotly_chart(fig3, use_container_width=True)

# ---- SUPPLIERS TAB ----
elif selected_tab == "Suppliers":
    st.subheader("🏭 Manage Suppliers")

    with st.expander("➕ Add New Supplier"):
        name = st.text_input("Supplier Name")
        location = st.text_input("Location")
        compliance = st.slider("Green Compliance (%)", 0, 100, 70)
        if st.button("Save Supplier"):
            if name and location:
                suppliers_col.insert_one({"name": name, "location": location, "compliance": compliance})
                st.success(f"Supplier '{name}' added successfully!")
            else:
                st.warning("Please fill all fields.")

    with st.expander("📄 View All Suppliers"):
        data = list(suppliers_col.find({}, {"_id": 0}))
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info("No supplier data found.")

# ---- OTHER TABS ----
else:
    st.subheader(f"{selected_tab} - Section under construction 🚧")



