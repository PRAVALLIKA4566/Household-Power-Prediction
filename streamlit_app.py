import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# ---------------- Page Config (MUST BE FIRST) ----------------
st.set_page_config(page_title="Household Power Prediction", layout="wide")

# ---------------- Theme Switcher ----------------
st.sidebar.header("Theme")
theme = st.sidebar.selectbox(
    "Choose Theme",
    ["Light", "Eco Green", "Dark"],
    key="theme_select"
)

if theme == "Light":
    css = """
    <style>
    .stApp { background-color: #f5f7fb; color: #1f2933; }
    h1 { color: #1f3a5f; text-align: center; font-weight: 700; }
    h2, h3 { color: #2d6cdf; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0px 2px 10px rgba(0,0,0,0.08); margin-bottom: 20px; }
    div.stButton > button { background-color: #2d6cdf; color: white; border-radius: 8px; height: 3em; width: 100%; font-size: 16px; font-weight: 600; border: none; }
    div.stButton > button:hover { background-color: #1f4fbf; color: white; }
    [data-testid="stMetricValue"] { color: #1f3a5f; font-size: 26px; font-weight: 700; }
    section[data-testid="stSidebar"] { background-color: #e9eef6; }
    </style>
    """

elif theme == "Eco Green":
    css = """
    <style>
    .stApp { background-color: #f6fbf8; color: #1f2933; }
    h1 { color: #2f855a; text-align: center; font-weight: 700; }
    h2, h3 { color: #38a169; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0px 2px 10px rgba(0,0,0,0.08); margin-bottom: 20px; }
    div.stButton > button { background-color: #38a169; color: white; border-radius: 8px; height: 3em; width: 100%; font-size: 16px; font-weight: 600; border: none; }
    div.stButton > button:hover { background-color: #2f855a; color: white; }
    [data-testid="stMetricValue"] { color: #2f855a; font-size: 26px; font-weight: 700; }
    section[data-testid="stSidebar"] { background-color: #edf7f1; }
    </style>
    """

else:  # Dark (Fixed Contrast)
    css = """
    <style>
    .stApp { background-color: #0f2027; color: #e6edf3; }
    p, span, div, label { color: #e6edf3 !important; }
    h1 { color: #00e5ff; text-align: center; font-weight: 800; }
    h2, h3 { color: #00ffb3; }
    .card { background-color: rgba(255,255,255,0.08); padding: 20px; border-radius: 15px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3); margin-bottom: 20px; }
    input, select, textarea { background-color: #1c2b36 !important; color: #e6edf3 !important; border-radius: 6px; border: 1px solid #2e4756; }
    .stSlider > div { color: #e6edf3 !important; }
    div.stButton > button { background-color: #00e5ff; color: black; border-radius: 10px; height: 3em; width: 100%; font-size: 18px; font-weight: bold; }
    div.stButton > button:hover { background-color: #00ffb3; color: black; }
    [data-testid="stMetricValue"] { color: #00ffb3; font-size: 28px; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #cfd8dc; font-size: 16px; }
    section[data-testid="stSidebar"] { background-color: #0b1e2d; }
    section[data-testid="stSidebar"] * { color: #e6edf3 !important; }
    </style>
    """

st.markdown(css, unsafe_allow_html=True)

# ---------------- Load Model ----------------
model = joblib.load("household_power_model.pkl")

# ---------------- Header ----------------
st.markdown("""
<h1>⚡ Household Power Consumption Dashboard</h1>
<p style='text-align:center; font-size:18px;'>
ML-powered energy forecasting & billing system
</p>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.header("Tariff Settings")
rate = st.sidebar.number_input(
    "Electricity Rate (₹ per kWh)",
    value=6.0,
    min_value=0.0,
    key="rate_input"
)
use_slabs = st.sidebar.checkbox("Use Slab-Based Tariff (India)", key="slab_checkbox")

st.sidebar.header("Presets")
preset = st.sidebar.selectbox(
    "Select Usage Preset",
    ["Custom", "All OFF", "Night Load", "Day Load", "Heavy Load"],
    key="preset_select"
)

# ---------------- Defaults ----------------
Global_reactive_power = 0.0
Voltage = 230.0
Global_intensity = 0.0
Sub_metering_1 = 0.0
Sub_metering_2 = 0.0
Sub_metering_3 = 0.0
hour = 12
day = 15
month = 6
weekday = 3

# ---------------- Apply Presets ----------------
if preset == "Night Load":
    Global_intensity = 0.8
    Sub_metering_3 = 0.5
elif preset == "Day Load":
    Global_intensity = 2.5
    Sub_metering_1 = 0.5
    Sub_metering_2 = 0.8
elif preset == "Heavy Load":
    Global_intensity = 6.0
    Sub_metering_3 = 2.5
    Sub_metering_1 = 1.0

# ---------------- Input Section ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.header("🔧 Input Features")

col1, col2, col3 = st.columns(3)

with col1:
    Global_reactive_power = st.number_input(
        "Global Reactive Power (kW)",
        value=Global_reactive_power,
        key="grp_input"
    )
    Voltage = st.number_input(
        "Voltage (V)",
        value=Voltage,
        key="voltage_input"
    )
    Global_intensity = st.number_input(
        "Global Intensity (A)",
        value=Global_intensity,
        key="gi_input"
    )

with col2:
    Sub_metering_1 = st.number_input(
        "Sub Metering 1 (Kitchen)",
        value=Sub_metering_1,
        key="sm1_input"
    )
    Sub_metering_2 = st.number_input(
        "Sub Metering 2 (Laundry)",
        value=Sub_metering_2,
        key="sm2_input"
    )
    Sub_metering_3 = st.number_input(
        "Sub Metering 3 (Climate)",
        value=Sub_metering_3,
        key="sm3_input"
    )

with col3:
    hour = st.slider("Hour of Day", 0, 23, hour, key="hour_slider")
    day = st.slider("Day of Month", 1, 31, day, key="day_slider")
    month = st.slider("Month", 1, 12, month, key="month_slider")
    weekday = st.slider("Weekday (0=Mon, 6=Sun)", 0, 6, weekday, key="weekday_slider")

# Validation warning
if Global_intensity > 0 and Sub_metering_1 == 0 and Sub_metering_2 == 0 and Sub_metering_3 == 0:
    st.markdown("""
    <div class='card' style='border-left:5px solid #ff9800;'>
    ⚠ Sub-meters are zero but current is non-zero. This implies unmetered loads.
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Input Data ----------------
input_data = pd.DataFrame({
    "Global_reactive_power": [Global_reactive_power],
    "Voltage": [Voltage],
    "Global_intensity": [Global_intensity],
    "Sub_metering_1": [Sub_metering_1],
    "Sub_metering_2": [Sub_metering_2],
    "Sub_metering_3": [Sub_metering_3],
    "hour": [hour],
    "day": [day],
    "month": [month],
    "weekday": [weekday]
})

# ---------------- Slab Tariff Function ----------------
def slab_bill(units):
    bill = 0
    slabs = [(100, 3), (200, 5), (float('inf'), 8)]
    remaining = units
    for limit, price in slabs:
        use = min(remaining, limit)
        bill += use * price
        remaining -= use
        if remaining <= 0:
            break
    return bill

# ---------------- Prediction ----------------
if st.button("Predict", key="predict_button"):
    prediction = model.predict(input_data)[0]

    BASE_LOAD_KW = 0.05
    if (Sub_metering_1 == 0 and Sub_metering_2 == 0 and Sub_metering_3 == 0 and
        Global_intensity == 0 and Global_reactive_power == 0):
        prediction = BASE_LOAD_KW

    per_day = prediction * 24
    per_week = prediction * 24 * 7
    per_month = prediction * 24 * 30

    if use_slabs:
        bill_month = slab_bill(per_month)
    else:
        bill_month = per_month * rate

    bill_day = bill_month / 30
    bill_week = bill_month / 4.345

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Results")
    st.success(f"Predicted Global Active Power: {prediction:.3f} kW")

    colA, colB, colC = st.columns(3)
    colA.metric("⚡ Daily Energy", f"{per_day:.2f} kWh")
    colB.metric("📅 Weekly Energy", f"{per_week:.2f} kWh")
    colC.metric("📆 Monthly Energy", f"{per_month:.2f} kWh")

    colD, colE, colF = st.columns(3)
    colD.metric("💸 Daily Bill", f"₹{bill_day:.2f}")
    colE.metric("💰 Weekly Bill", f"₹{bill_week:.2f}")
    colF.metric("🏦 Monthly Bill", f"₹{bill_month:.2f}")

    if prediction > 2.5:
        st.error("⚠ High continuous load detected. Monthly bill may be unrealistic for normal households.")

    # Graph
    st.subheader("Energy Trend")
    labels = ["Day", "Week", "Month"]
    values = [per_day, per_week, per_month]
    plt.figure()
    plt.plot(labels, values, marker="o")
    plt.ylabel("Energy (kWh)")
    plt.title("Estimated Energy Consumption")
    st.pyplot(plt)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Enhanced Streamlit App | Random Forest Model | ML-based Energy Forecasting")