import streamlit as st
import requests


box = st.container()
st.set_page_config(page_icon="☁", page_title="Smart GreenHouse Interface")
st.toast("Welcome", icon ="😉")
st.header("Welcome to our User Interface", text_alignment="center")
st.markdown(""" <style>
.stApp {
background : radial-gradient(circle at center,
              #F1F8E9 0%,
              #C8E6C9 50%,
              #81C784 100%
              );


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












