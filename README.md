# Assignment_1
A Streamlit-based web app to reduce food waste by connecting food providers with NGOs, shelters, and individuals. Includes registration, food listing, claiming system, and real-time analytics using SQLite and Pandas.
# 🍽️ Local Food Waste Management System 🌍

A community-centric platform that bridges the gap between **food donors** (restaurants, homes, supermarkets) and **receivers** (NGOs, shelters, individuals in need) — helping reduce food waste and feed the hungry.

---

## 🔍 Overview

Every day, huge quantities of edible food are discarded while many go hungry. This system provides a digital platform for **registering, listing, claiming**, and **tracking surplus food donations** in a local community.

Built using **Python + Streamlit**, with **SQLite** for data management and **Pandas/Seaborn** for analytics.

---

## ✅ Features

- 🔐 **User Registration**: Providers & Receivers can register and manage profiles.
- 🍱 **Food Listings**: Providers list surplus food with details like quantity, expiry, meal type.
- 📥 **Claiming System**: Receivers can browse and claim available food items.
- 📊 **Real-time Claim Status**: Track food claims (Pending / Completed / Cancelled).
- 📈 **Dashboard & Insights**: Visual queries and charts on donations, claims, and trends.
- 📂 **CSV + DB Integration**: Automatically syncs with CSV for backups and reporting.

---

## 🛠️ Tech Stack

| Component       | Technology              |
|----------------|--------------------------|
| Frontend       | Streamlit (Python)       |
| Backend        | SQLite3                  |
| Data Analysis  | Pandas, Matplotlib, Seaborn |
| File Handling  | CSV                      |
| Deployment     | Localhost / Streamlit Cloud |

---

## 📦 Project Structure

```
├── homepage.py           # Main dashboard and table views
├── Providers.py          # Provider registration & management
├── Receivers.py          # Receiver registration & management
├── Food_listing_datas.py # Food listings - add/edit/delete
├── claim_status.py       # Food claiming logic and status update
├── Queries.py            # Analytics and data visualization
├── About.py              # Info & benefits section
├── food_waste_management.py  # Page navigation control
├── Dataset/              # CSVs: claims_data.csv, providers_data.csv, etc.
├── Local_food_WM.db      # SQLite database file
├── Image.jpeg            # Welcome screen banner
```

---

## 📈 Sample Queries

- Top food donors by quantity
- Meal types most in demand
- Cities with highest food wastage
- Unclaimed and expired food data
- Donation trends over time

---

## 🌟 Benefits

- ♻️ Reduces food waste at the source
- 🤝 Builds local community networks
- 🌱 Promotes sustainability and social responsibility
- 🍛 Helps combat hunger at the grassroots

---

## 🚀 Future Scope

- Mobile App Integration (React Native / Flutter)
- Real-time maps & location-based food pickup
- SMS / WhatsApp alerts for claims
- Admin-level reporting and approval flows

---
