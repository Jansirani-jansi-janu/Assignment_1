
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# Set database path
DB_PATH = "food_waste.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

# Load database from CSVs if it doesn’t exist
def initialize_database():
    if not os.path.exists(DB_PATH):
        st.info("Setting up database from CSV files...")

        providers = pd.read_csv("providers_data.csv")
        receivers = pd.read_csv("receivers_data.csv")
        food_listings = pd.read_csv("food_listings_data.csv")
        claims = pd.read_csv("claims_data.csv")

        providers.to_sql("providers", engine, index=False, if_exists="replace")
        receivers.to_sql("receivers", engine, index=False, if_exists="replace")
        food_listings.to_sql("food_listings", engine, index=False, if_exists="replace")
        claims.to_sql("claims", engine, index=False, if_exists="replace")

# Call it
initialize_database()

# Connect to database
conn = engine.connect()

st.title("🍱 Local Food Wastage Management System")

option = st.selectbox("Choose what to view:", [
    "All Providers", "All Receivers", "Available Food", "Claims Summary"
])

if option == "All Providers":
    df = pd.read_sql("SELECT * FROM providers", conn)
    st.dataframe(df)

elif option == "All Receivers":
    df = pd.read_sql("SELECT * FROM receivers", conn)
    st.dataframe(df)

elif option == "Available Food":
    city = st.text_input("Filter by City")
    query = "SELECT * FROM food_listings"
    if city:
        query += f" WHERE location LIKE '%{city}%'"
    df = pd.read_sql(query, conn)
    st.dataframe(df)

elif option == "Claims Summary":
    query = """
    SELECT food_id, COUNT(*) as total_claims,
           SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) as completed
    FROM claims
    GROUP BY food_id
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)
