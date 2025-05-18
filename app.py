import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

DB_PATH = "food_waste.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

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

initialize_database()
conn = engine.connect()

st.title("🍱 Local Food Wastage Management System")

# Main menu
option = st.selectbox("Choose what to view:", [
    "All Providers",
    "All Receivers",
    "Available Food",
    "Claims Summary",
    "SQL Query Analysis"
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

elif option == "SQL Query Analysis":
    query_dict = {
        "1. Providers and Receivers per City":
        """SELECT providers.city, 
                  COUNT(DISTINCT providers.provider_id) AS num_providers,
                  COUNT(DISTINCT receivers.receiver_id) AS num_receivers
           FROM providers
           JOIN receivers ON providers.city = receivers.city
           GROUP BY providers.city""",

        "2. Top Provider Type by Food Contribution":
        """SELECT provider_type, COUNT(*) AS total_food_items
           FROM food_listings
           GROUP BY provider_type
           ORDER BY total_food_items DESC
           LIMIT 1""",

        "3. Provider Contacts in Chennai":
        """SELECT name, contact
           FROM providers
           WHERE city = 'Chennai'""",

        "4. Receivers with Most Claims":
        """SELECT receivers.name, COUNT(*) AS total_claims
           FROM claims
           JOIN receivers ON claims.receiver_id = receivers.receiver_id
           GROUP BY receivers.name
           ORDER BY total_claims DESC
           LIMIT 5""",

        "5. Total Quantity of Available Food":
        """SELECT SUM(quantity) AS total_available_quantity
           FROM food_listings""",

        "6. City with Most Food Listings":
        """SELECT location, COUNT(*) AS listings_count
           FROM food_listings
           GROUP BY location
           ORDER BY listings_count DESC
           LIMIT 1""",

        "7. Most Common Food Types":
        """SELECT food_type, COUNT(*) AS count
           FROM food_listings
           GROUP BY food_type
           ORDER BY count DESC""",

        "8. Claims Per Food Item":
        """SELECT food_id, COUNT(*) AS total_claims
           FROM claims
           GROUP BY food_id""",

        "9. Provider with Most Completed Claims":
        """SELECT providers.name, COUNT(*) AS successful_claims
           FROM claims
           JOIN food_listings ON claims.food_id = food_listings.food_id
           JOIN providers ON food_listings.provider_id = providers.provider_id
           WHERE status = 'Completed'
           GROUP BY providers.name
           ORDER BY successful_claims DESC
           LIMIT 1""",

        "10. Claim Status Percentage":
        """SELECT status,
                  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS percentage
           FROM claims
           GROUP BY status""",

        "11. Avg Quantity Claimed Per Receiver":
        """SELECT receivers.name, AVG(food_listings.quantity) AS avg_quantity
           FROM claims
           JOIN food_listings ON claims.food_id = food_listings.food_id
           JOIN receivers ON claims.receiver_id = receivers.receiver_id
           GROUP BY receivers.name""",

        "12. Most Claimed Meal Type":
        """SELECT meal_type, COUNT(*) AS total_claims
           FROM claims
           JOIN food_listings ON claims.food_id = food_listings.food_id
           GROUP BY meal_type
           ORDER BY total_claims DESC
           LIMIT 1""",

        "13. Total Quantity Donated per Provider":
        """SELECT providers.name, SUM(food_listings.quantity) AS total_quantity
           FROM providers
           JOIN food_listings ON providers.provider_id = food_listings.provider_id
           GROUP BY providers.name
           ORDER BY total_quantity DESC""",

        "14. Upcoming Expiry (next 3 days)":
        """SELECT food_name, expiry_date, quantity
           FROM food_listings
           WHERE expiry_date BETWEEN DATE('now') AND DATE('now', '+3 day')""",

        "15. Cities with Most Pending Claims":
        """SELECT providers.city, COUNT(*) AS pending_claims
           FROM claims
           JOIN food_listings ON claims.food_id = food_listings.food_id
           JOIN providers ON food_listings.provider_id = providers.provider_id
           WHERE status = 'Pending'
           GROUP BY providers.city
           ORDER BY pending_claims DESC"""
    }

    query_choice = st.selectbox("Select a query to run:", list(query_dict.keys()))
    if query_choice:
        df = pd.read_sql(query_dict[query_choice], conn)
        st.subheader(f"Result: {query_choice}")
        st.dataframe(df)

