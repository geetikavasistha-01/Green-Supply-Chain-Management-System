# Step 1: Basic Streamlit Setup for GSCMS Dashboard with MongoDB Integration

import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB Connection
client = MongoClient("mongodb+srv://geetikavasistha13:01gWVJgQKvq0gUes@gscms.ph6se0s.mongodb.net/")
db = client["gscms"]

# Function to fetch collection data
def load_data(collection_name):
    collection = db[collection_name]
    data = list(collection.find())
    if data:
        for item in data:
            item["_id"] = str(item["_id"])
        return pd.DataFrame(data)
    return pd.DataFrame()

# Streamlit UI
st.set_page_config(page_title="Green Supply Chain Management System", layout="wide")

st.title("🌱 Green Supply Chain Management System (GSCMS) Dashboard")

tabs = st.tabs(["Suppliers", "Manufacturers", "Products", "Transportation", "Audits", "Regulations"])

# Render collections as tables
collection_names = ["suppliers", "manufacturers", "products", "transportations", "audits", "regulations"]
tab_titles = ["Suppliers", "Manufacturers", "Products", "Transportation", "Audits", "Regulations"]

for i, tab in enumerate(tabs):
    with tab:
        st.subheader(f"{tab_titles[i]} Records")
        df = load_data(collection_names[i])
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No records found in this collection.")

client.close()




