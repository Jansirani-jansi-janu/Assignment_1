import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.title("🍲 Local Food Wastage Management System")

engine = create_engine('sqlite:///food_waste.db')
conn = engine.connect()

option = st.selectbox("Choose what to view:", [
    "All Providers", "All Receivers", "Available Food", "Claims Summary"
])

if option == "All Providers":
    st.subheader("Food Providers")
    df = pd.read_sql("SELECT * FROM providers", conn)
    st.dataframe(df)

elif option == "All Receivers":
    st.subheader("Food Receivers")
    df = pd.read_sql("SELECT * FROM receivers", conn)
    st.dataframe(df)

elif option == "Available Food":
    st.subheader("Food Listings")
    city = st.text_input("Filter by City")
    query = "SELECT * FROM food_listings"
    if city:
        query += f" WHERE location LIKE '%{city}%'"
    df = pd.read_sql(query, conn)
    st.dataframe(df)

elif option == "Claims Summary":
    st.subheader("Food Claims Overview")
    query = """
    SELECT food_id, COUNT(*) as total_claims,
           SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) as completed
    FROM claims
    GROUP BY food_id
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)
