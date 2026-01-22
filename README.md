# ⚡ Household Power Consumption Prediction

A machine learning–powered Streamlit web application to predict household power consumption, estimate energy usage, and calculate electricity bills.

---

##  Project Overview

This project uses a trained Random Forest regression model to forecast household **Global Active Power (kW)** based on:

- Electrical measurements  
- Sub-metering values  
- Time-based features  

The application then computes:

- Daily, weekly, monthly energy usage  
- Electricity bills (flat rate or slab-based tariff)  

---

##  Features

-  ML-based power prediction  
-  Energy usage estimation (day/week/month)  
-  Electricity bill calculation  
- Indian slab tariff support  
-  Theme switcher (Light / Eco Green / Dark)  
- Validation warnings  
-  Energy trend visualization  
-  Styled dashboard UI  

---

##  Tech Stack

- Python  
- Streamlit  
- Scikit-learn  
- Pandas  
- Matplotlib  

---

##  Project Structure

HouseholdPowerApp/
├── streamlit_app.py
├── household_power_model.pkl
├── requirements.txt
├── README.md
└── data/
└── household_power_consumption.csv

