import streamlit as st
import pandas as pd
import plotly.express as px
from apis import apod_generator
import os

# in the terminal: streamlit run dashboard.py
st.title("Water Quality Dashboard")
st.header("Internship Ready Software")
st.subheader("Prof. Gregory Reis")

st.divider()

df = pd.read_csv("biscayneBay_waterquality.csv")

tab1, tab2 ,tab3, tab4 = st.tabs(
    ["Descriptive Statistics",
     "2d Plots",
     "3d Plots",
     "Astronomy Picture of the Day"]
)

with tab1:
    st.dataframe(df)
    st.caption("Raw Data")
    st.divider()
    st.dataframe(df.describe())
    st.caption("Descriptive Statistics")

with tab2:
    fig1=px.line(df,
                 x="Time",
                 y="Temperature (c)")
    st.plotly_chart(fig1)
    fig2= px.scatter(df,
                     x= "ODO mg/L",
                     y="Temperature (c)",
                     color = "pH")
    st.plotly_chart(fig2)

    st.subheader("Temperature vs Salinity by Depth Range")

    # Slider for selecting depth range
    min_depth = float(df["Total Water Column (m)"].min())
    max_depth = float(df["Total Water Column (m)"].max())

    depth_range = st.slider(
        "Select Depth Range (m)",
        min_value=min_depth,
        max_value=max_depth,
        value=(min_depth, max_depth)
    )

    # Filter dataset based on slider selection
    filtered_df = df[
        (df["Total Water Column (m)"] >= depth_range[0]) &
        (df["Total Water Column (m)"] <= depth_range[1])
        ]

    # Scatter plot
    fig = px.scatter(
        filtered_df,
        x="Salinity (ppt)",
        y="Temperature (c)",
        color="Total Water Column (m)",
        title=f"Temperature vs Salinity for Depths {depth_range[0]}–{depth_range[1]} m",
        labels={
            "Sal ppt": "Salinity (ppt)",
            "Temperature (c)": "Temperature (°C)",
            "Total Water Column (m)": "Depth (m)"
        }
    )

    st.plotly_chart(fig)

with tab3:
    fig3 = px.scatter_3d(df,
                         x="Longitude",
                         y="Latitude",
                         z= "Total Water Column (m)",
                         color="Temperature (c)")
    fig3.update_scenes(zaxis_autorange="reversed")
    st.plotly_chart(fig3)

with tab4:
    st.title("NASA's Astronomy Picture of the Day")

    #TODO: Call a function that generates the APOD
    url = "https://api.nasa.gov/planetary/apod?api_key="
    response = apod_generator(url, os.getenv("NASA_API_KEY"))

    #TODO: display the APOD image and title and other features
    st.subheader(response["title"])
    st.image(response["hdurl"])
    st.subheader("Date: " + response["date"])




