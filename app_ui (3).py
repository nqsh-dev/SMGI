import streamlit as st
import requests


box = st.container()
st.set_page_config(page_icon="☁", page_title="Smart GreenHouse Interface")
st.toast("Welcome", icon ="😉")
st.header("Welcome to our User Interface", text_alignment="center")
image_url="https://tse2.mm.bing.net/th/id/OIP.mR7CJ6OBkrJnjcLs8eVRzwHaHa?rs=1&pid=ImgDetMain&o=7&rm=3"


st.markdown(f"""
<style>
.stApp {{
    background:
    linear-gradient(rgba(255,255,255,0.30), rgba(255,255,255,0.30)),
    url("{image_url}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

.block-container {{
    backdrop-filter: blur(4px);
    background-color: rgba(255,255,255,0.25);
    border-radius: 12px;
    padding: 2rem;
}}
</style>
""", unsafe_allow_html=True)





st.markdown(""" <style>
.stApp {

color: #000000;
}
</style> """, unsafe_allow_html=True)
url = "https://actual-reindeer-humiya-11975376.koyeb.app/api/v1/sensors/latest"
response = requests.get(url)
data = response.json()
url1 = "https://actual-reindeer-humiya-11975376.koyeb.app/api/v1/predictions/latest"
response1 = requests.get(url1)
prediction = response1.json()

col_temp, col_humidity, col_lux, col_prediction = st.columns(4, gap="xxlarge", vertical_alignment="center")



with col_temp:
     with st.container(border=True):
        st.subheader("Temperature🌡")
        st.write("⁰C")
        st.write(data["temperature"] )

with col_humidity:
     with st.container(border=True):
        st.subheader("Humidity💧")
        st.write("%")
        st.write(data["humidity"] )


with col_lux:
     with st.container(border=True):
        st.subheader("Light Intensity🔥")
        st.write("lux")
        st.write(data["light"] )

with col_prediction:
        with st.container(border=True):
            st.subheader("Prediction❄")
            st.write("⁰C")
            st.write(prediction["temperature_1h"] )













