import streamlit as st 
import requests 
from datetime import datetime

==============================

PAGE CONFIG

==============================

st.set_page_config( page_title="Smart GreenHouse Interface", page_icon="🌿", layout="wide" )

==============================

BACKGROUND IMAGE

==============================

image_url = "https://tse2.mm.bing.net/th/id/OIP.mR7CJ6OBkrJnjcLs8eVRzwHaHa?rs=1&pid=ImgDetMain&o=7&rm=3"

st.markdown(f"""

<style>

/* GLOBAL TEXT */
html, body, [class*="css"]  {{
    font-family: 'Segoe UI', sans-serif;
}}

/* BACKGROUND */
.stApp {{
    background:
    linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.35)),
    url("{image_url}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
}}

/* MAIN CONTAINER */
.block-container {{
    backdrop-filter: blur(12px);
    background-color: rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 2.5rem;
    border: 1px solid rgba(255,255,255,0.15);
}}

/* CARD STYLE */
div[data-testid="stMetric"] {{
    background: rgba(255,255,255,0.12);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}}

/* TITLE */
h1, h2, h3 {{
    text-align: center;
    letter-spacing: 1px;
}}

/* REFRESH BUTTON */
div.stButton > button {{
    border-radius: 10px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    background: rgba(255,255,255,0.15);
    color: white;
    border: 1px solid rgba(255,255,255,0.25);
}}

</style>""", unsafe_allow_html=True)

==============================

HEADER

==============================

st.title("🌱 Smart GreenHouse Dashboard") st.caption("Real-time environmental monitoring system")

==============================

REFRESH CONTROL

==============================

col_left, col_center, col_right = st.columns([1,2,1]) with col_center: if st.button("🔄 Refresh Data"): st.rerun()

==============================

API ENDPOINTS

==============================

SENSOR_URL = "https://sufficient-puma-humiya-344b268d.koyeb.app/api/v1/sensors/latest" PREDICTION_URL = "https://sufficient-puma-humiya-344b268d.koyeb.app/api/v1/predictions/latest"

==============================

DATA FETCH FUNCTION

==============================

def fetch_data(): try: with st.spinner("Fetching real-time data..."): sensor_response = requests.get(SENSOR_URL, timeout=10) prediction_response = requests.get(PREDICTION_URL, timeout=10)

sensor_response.raise_for_status()
        prediction_response.raise_for_status()

        sensors = sensor_response.json()
        prediction = prediction_response.json()

        return sensors, prediction, None

except Exception as e:
    return None, None, str(e)

==============================

LOAD DATA

==============================

sensors, prediction, error = fetch_data()

==============================

ERROR HANDLING

==============================

if error: st.error("Unable to retrieve greenhouse data") st.caption(error) st.stop()

==============================

METRICS DISPLAY

==============================

col1, col2, col3, col4 = st.columns(4, gap="large")

with col1: st.metric( label="🌡 Temperature", value=f"{sensors['temperature']} °C" )

with col2: st.metric( label="💧 Humidity", value=f"{sensors['humidity']} %" )

with col3: st.metric( label="☀ Light Intensity", value=f"{sensors['light']} lux" )

with col4: st.metric( label="🔮 Temperature Prediction (1h)", value=f"{prediction['temperature_1h']} °C" )

==============================

FOOTER

==============================

st.divider() st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") st.caption("System status: Online ✅")

