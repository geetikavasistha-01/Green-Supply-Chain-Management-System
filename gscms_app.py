import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB Connection
client = MongoClient("mongodb+srv://geetikavasistha13:01gWVJgQKvq0gUes@gscms.ph6se0s.mongodb.net/")
db = client["gscms"]  # Replace with your actual DB name

# Load data from collections
def load_data(collection_name):
    collection = db[collection_name]
    data = list(collection.find())
    for item in data:
        item["_id"] = str(item["_id"])  # Convert ObjectId to string
    return pd.DataFrame(data)

# Streamlit UI Setup
st.set_page_config(page_title="Green Supply Chain Management System", layout="wide")
st.title("🌿 Green Supply Chain Management System (GSCMS)")

tabs = st.tabs(["Suppliers", "Manufacturers", "Products", "Transportation", "Audits", "Regulations"])

collections = {
    "Suppliers": "suppliers",
    "Manufacturers": "manufacturers",
    "Products": "products",
    "Transportation": "transportations",
    "Audits": "audits",
    "Regulations": "regulations"
}

for tab, collection in zip(tabs, collections.values()):
    with tab:
        df = load_data(collection)
        st.subheader(f"{collection.capitalize()} Records")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning(f"No data found in {collection} collection.")
