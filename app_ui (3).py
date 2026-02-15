import streamlit as st
import requests
from datetime import datetime
import time

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="HUAWEI Smart Greenhouse",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===== API CONFIG =====
API_URL = "https://sufficient-puma-humiya-344b268d.koyeb.app/api/v1"

# ===== HUAWEI HARMONYOS INSPIRED CSS =====
st.markdown("""
<style>
    /* Import HarmonyOS Sans font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Main App Container - Huawei's signature gradient */
    .stApp {
        background: linear-gradient(145deg, #f5f7fa 0%, #e9edf2 100%);
        min-height: 100vh;
    }

    /* Main Container with comfortable padding */
    .main-container {
        max-width: 100%;
        margin: 0 auto;
        padding: 24px 20px;
    }

    /* Header Section - Huawei's clean card design */
    .header {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 32px;
        padding: 28px 24px;
        margin-bottom: 32px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.5);
        animation: slideDown 0.5s ease-out;
    }

    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    .header-title {
        font-size: 28px;
        font-weight: 600;
        color: #1a2639;
        margin-bottom: 12px;
        letter-spacing: -0.3px;
    }

    .header-subtitle {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #5a6874;
        font-size: 14px;
        font-weight: 400;
    }

    .live-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(52, 199, 89, 0.1);
        padding: 6px 14px;
        border-radius: 30px;
        color: #34c759;
        font-weight: 500;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        background: #34c759;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }

    /* Metrics Grid - Spacious and elegant */
    .metrics-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 32px;
        animation: fadeIn 0.6s ease-out 0.2s both;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Huawei's signature frosted glass cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 28px;
        padding: 24px 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.8);
        transition: all 0.3s cubic-bezier(0.2, 0, 0, 1);
    }

    .metric-card:hover {
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.04);
        transform: translateY(-2px);
    }

    .metric-card:active {
        transform: scale(0.98);
    }

    .metric-icon {
        font-size: 28px;
        margin-bottom: 16px;
        color: #1a2639;
    }

    .metric-label {
        font-size: 12px;
        font-weight: 500;
        color: #8e9aab;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }

    .metric-value-wrapper {
        display: flex;
        align-items: baseline;
        gap: 8px;
    }

    .metric-value {
        font-size: 40px;
        font-weight: 600;
        color: #1a2639;
        line-height: 1;
    }

    .metric-unit {
        font-size: 14px;
        font-weight: 400;
        color: #8e9aab;
    }

    .metric-trend {
        margin-top: 12px;
        font-size: 12px;
        color: #5a6874;
    }

    /* Prediction Section - Huawei's gradient cards */
    .prediction-section {
        background: linear-gradient(145deg, #2b3440 0%, #1e2632 100%);
        border-radius: 32px;
        padding: 28px 24px;
        margin-bottom: 32px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        animation: slideUp 0.6s ease-out 0.4s both;
    }

    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    .prediction-title {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: rgba(255, 255, 255, 0.9);
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 24px;
    }

    .prediction-badge {
        background: rgba(255, 255, 255, 0.1);
        padding: 4px 12px;
        border-radius: 30px;
        font-size: 11px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.7);
    }

    .prediction-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }

    .prediction-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 18px 16px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .prediction-item:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-2px);
    }

    .prediction-label {
        font-size: 11px;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    .prediction-value {
        font-size: 26px;
        font-weight: 600;
        color: white;
    }

    .prediction-unit {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.4);
        margin-left: 4px;
    }

    /* Status Section */
    .status-section {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 32px;
        padding: 24px;
        margin-bottom: 32px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        animation: fadeIn 0.6s ease-out 0.6s both;
    }

    .status-title {
        font-size: 14px;
        font-weight: 500;
        color: #1a2639;
        margin-bottom: 20px;
    }

    .status-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
    }

    .status-item {
        background: white;
        border-radius: 20px;
        padding: 16px 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    }

    .status-label {
        font-size: 11px;
        color: #8e9aab;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .status-value {
        font-size: 18px;
        font-weight: 600;
        color: #1a2639;
    }

    /* Refresh Button - Huawei style */
    .refresh-btn {
        background: white;
        border: none;
        border-radius: 30px;
        padding: 18px;
        font-size: 15px;
        font-weight: 500;
        color: #1a2639;
        width: 100%;
        text-align: center;
        cursor: pointer;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-out 0.8s both;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.8);
    }

    .refresh-btn:hover {
        background: #f8faff;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }

    .refresh-btn:active {
        transform: scale(0.98);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 24px 0 16px;
        color: #8e9aab;
        font-size: 11px;
        border-top: 1px solid rgba(142, 154, 171, 0.2);
        animation: fadeIn 0.6s ease-out 1s both;
    }

    /* Loading Animation */
    .loading-spinner {
        width: 44px;
        height: 44px;
        border: 3px solid rgba(26, 38, 57, 0.05);
        border-top-color: #1a2639;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 60px auto;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Responsive adjustments */
    @media (max-width: 380px) {
        .metric-value {
            font-size: 32px;
        }
        .prediction-value {
            font-size: 22px;
        }
        .status-grid {
            grid-template-columns: 1fr;
            gap: 12px;
        }
        .metrics-grid {
            gap: 16px;
        }
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)


# ===== DATA FETCHING =====
@st.cache_data(ttl=5)
def get_latest_data():
    try:
        r = requests.get(f"{API_URL}/sensors/latest", timeout=3)
        return r.json() if r.status_code == 200 else None
    except:
        return None


@st.cache_data(ttl=10)
def get_prediction():
    try:
        r = requests.get(f"{API_URL}/predictions/latest", timeout=3)
        return r.json() if r.status_code == 200 else None
    except:
        return None


@st.cache_data(ttl=60)
def get_training_status():
    try:
        r = requests.get(f"{API_URL}/training/status", timeout=3)
        return r.json() if r.status_code == 200 else None
    except:
        return None


# ===== FETCH DATA =====
data = get_latest_data()
prediction = get_prediction()
training_status = get_training_status()

# ===== MAIN CONTAINER =====
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ===== HEADER =====
st.markdown(f"""
<div class='header'>
    <div class='header-title'>🌱 Smart Greenhouse</div>
    <div class='header-subtitle'>
        <span>{datetime.now().strftime('%B %d, %Y • %I:%M %p')}</span>
        <span class='live-indicator'>
            <span class='live-dot'></span>
            Live
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== METRICS GRID (Spacious) =====
if data:
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)

    # Temperature
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>🌡️</div>
        <div class='metric-label'>TEMPERATURE</div>
        <div class='metric-value-wrapper'>
            <span class='metric-value'>{data['temperature']:.1f}</span>
            <span class='metric-unit'>°C</span>
        </div>
        <div class='metric-trend'>Normal range 20-25°C</div>
    </div>
    """, unsafe_allow_html=True)

    # Humidity
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>💧</div>
        <div class='metric-label'>HUMIDITY</div>
        <div class='metric-value-wrapper'>
            <span class='metric-value'>{data['humidity']:.1f}</span>
            <span class='metric-unit'>%</span>
        </div>
        <div class='metric-trend'>Optimal 60-70%</div>
    </div>
    """, unsafe_allow_html=True)

    # Light
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>☀️</div>
        <div class='metric-label'>LIGHT</div>
        <div class='metric-value-wrapper'>
            <span class='metric-value'>{data['light']:.0f}</span>
            <span class='metric-unit'>lux</span>
        </div>
        <div class='metric-trend'>Min 10,000 lux needed</div>
    </div>
    """, unsafe_allow_html=True)

    # Soil
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>🌱</div>
        <div class='metric-label'>SOIL</div>
        <div class='metric-value-wrapper'>
            <span class='metric-value'>{data['soil_moisture']:.1f}</span>
            <span class='metric-unit'>%</span>
        </div>
        <div class='metric-trend'>Ideal 50-65%</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("<div class='loading-spinner'></div>", unsafe_allow_html=True)

# ===== AI PREDICTIONS =====
if prediction and prediction.get('temperature_1h'):
    st.markdown(f"""
    <div class='prediction-section'>
        <div class='prediction-title'>
            <span> AI Mindspore</span>
            <span class='prediction-badge'>+1 hour</span>
        </div>
        <div class='prediction-grid'>
            <div class='prediction-item'>
                <div class='prediction-label'>Temperature</div>
                <div class='prediction-value'>{prediction['temperature_1h']:.1f}<span class='prediction-unit'>°C</span></div>
            </div>
            <div class='prediction-item'>
                <div class='prediction-label'>Humidity</div>
                <div class='prediction-value'>{prediction['humidity_1h']:.1f}<span class='prediction-unit'>%</span></div>
            </div>
            <div class='prediction-item'>
                <div class='prediction-label'>Light</div>
                <div class='prediction-value'>{prediction['light_1h']:.0f}<span class='prediction-unit'>lux</span></div>
            </div>
            <div class='prediction-item'>
                <div class='prediction-label'>Soil</div>
                <div class='prediction-value'>{prediction['soil_1h']:.1f}<span class='prediction-unit'>%</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== AI STATUS =====
if training_status:
    st.markdown("""
    <div class='status-section'>
        <div class='status-title'> AI System Status</div>
        <div class='status-grid'>
    """, unsafe_allow_html=True)

    if training_status.get("status") == "active":
        st.markdown(f"""
        <div class='status-item'>
            <div class='status-label'>STATUS</div>
            <div class='status-value' style='color:#34c759;'>Active</div>
        </div>
        <div class='status-item'>
            <div class='status-label'>SAMPLES</div>
            <div class='status-value'>{training_status.get('samples', 0)}</div>
        </div>
        <div class='status-item'>
            <div class='status-label'>ACCURACY</div>
            <div class='status-value'>{(training_status.get('r2_score', 0) * 100):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='grid-column: 1/-1; text-align: center; padding: 20px; color: #8e9aab;'>
            ⏳ Initializing AI training...
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# ===== REFRESH BUTTON =====
if st.button("🔄 Refresh Data", key="refresh"):
    st.cache_data.clear()
    st.rerun()

# ===== FOOTER =====
st.markdown("""
<div class='footer'>
    <div> Smart Greenhouse · HarmonyOS Connect</div>
    <div style='margin-top: 8px;'>Real-time monitoring · AI-powered predictions</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===== AUTO-REFRESH =====
time.sleep(5)
st.cache_data.clear()
st.rerun()
