import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- 1. PAGE SETUP & CUSTOM CSS ---
st.set_page_config(page_title="Team Globe", layout="wide")

st.markdown("""
<style>
    /* IBM Plex Sans (Watson Font) */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif !important;
    }

    /* Space Background */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?q=80&w=3000&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-color: #000000;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}

    .title-text {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 600;
        margin-top: -40px;
        text-shadow: 0px 4px 20px rgba(0,0,0,0.8);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">🌍 Team Global Operations</div>', unsafe_allow_html=True)

# --- 2. DATA & REAL-TIME CALCULATIONS ---
team_data = [
    {"Name": "Deven", "Location": "Sabah, Malaysia", "Lat": 5.97, "Lon": 116.07, "Timezone": "Asia/Kuala_Lumpur"},
    {"Name": "Jenna", "Location": "KL, Malaysia", "Lat": 3.14, "Lon": 101.69, "Timezone": "Asia/Kuala_Lumpur"},
    {"Name": "Ethan", "Location": "Scotland", "Lat": 56.49, "Lon": -4.20, "Timezone": "Europe/London"},
    {"Name": "Lina", "Location": "Italy", "Lat": 41.87, "Lon": 12.56, "Timezone": "Europe/Rome"},
    {"Name": "Ben", "Location": "Yucatan, Mexico", "Lat": 20.97, "Lon": -89.59, "Timezone": "America/Merida"},
    {"Name": "Elizabeth", "Location": "Japan", "Lat": 35.68, "Lon": 139.69, "Timezone": "Asia/Tokyo"},
    {"Name": "Marisa", "Location": "NYC, USA", "Lat": 40.71, "Lon": -74.00, "Timezone": "America/New_York"},
    {"Name": "Branson", "Location": "South Africa", "Lat": -30.55, "Lon": 22.93, "Timezone": "Africa/Johannesburg"},
    {"Name": "Isidro", "Location": "Kolkata, India", "Lat": 22.57, "Lon": 88.36, "Timezone": "Asia/Kolkata"},
    {"Name": "Maya", "Location": "Nairobi, Kenya", "Lat": -1.29, "Lon": 36.82, "Timezone": "Africa/Nairobi"},
    {"Name": "Katryna", "Location": "Zambia", "Lat": -13.13, "Lon": 27.84, "Timezone": "Africa/Lusaka"},
    {"Name": "Zoe", "Location": "Ireland", "Lat": 53.41, "Lon": -8.24, "Timezone": "Europe/Dublin"},
    {"Name": "Maddy", "Location": "LA, USA", "Lat": 34.05, "Lon": -118.24, "Timezone": "America/Los_Angeles"},
    {"Name": "Sydney", "Location": "Belgium", "Lat": 50.50, "Lon": 4.47, "Timezone": "Europe/Brussels"},
    {"Name": "Andrew", "Location": "Berlin, Germany", "Lat": 52.52, "Lon": 13.40, "Timezone": "Europe/Berlin"},
]

df = pd.DataFrame(team_data)


# Function to get the time string and assign the correct icon
def get_time_and_icon(tz_string):
    tz = pytz.timezone(tz_string)
    now = datetime.now(tz)
    hour = now.hour

    # Format time for the hover box
    time_str = now.strftime('%I:%M %p')

    # Assign icons based on hour ranges
    if 9 <= hour < 17:
        icon = "☀️"  # 9 AM to 4:59 PM
    elif 17 <= hour < 21:
        icon = "🌗"  # 5 PM to 8:59 PM
    else:
        icon = "🌙"  # 9 PM to 8:59 AM

    return pd.Series([time_str, icon])


# Apply calculations
df[['Current Time', 'Icon']] = df['Timezone'].apply(get_time_and_icon)

# 1. Always-on text: Just the Icon and the Name
df['Map Label'] = df['Icon'] + " " + df['Name']

# 2. Hover text: The rich detailed data
df['Hover Info'] = "<b>" + df['Name'] + "</b><br>" + df['Location'] + "<br>Local Time: " + df['Current Time']

# --- 3. 3D INTERACTIVE GLOBE ---
fig = go.Figure(data=go.Scattergeo(
    lon=df['Lon'],
    lat=df['Lat'],
    text=df['Map Label'],  # What shows on the map constantly
    customdata=df['Hover Info'],  # Hidden data for the hover box
    hovertemplate="%{customdata}<extra></extra>",  # Forces hover to ONLY show customdata
    mode='markers+text',
    textposition="top right",
    marker=dict(
        size=8,
        color='#00ffcc',
        line=dict(width=1, color='white')
    )
))

fig.update_layout(
    font=dict(family="'IBM Plex Sans', sans-serif", size=13, color="white"),
    geo=dict(
        projection_type='orthographic',
        showland=True,
        landcolor="rgba(20, 30, 40, 0.9)",
        showocean=True,
        oceancolor="rgba(0, 0, 0, 0)",
        showcountries=True,
        countrycolor="rgba(100, 100, 100, 0.5)",
        bgcolor="rgba(0, 0, 0, 0)",
        resolution=50,
    ),
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    margin=dict(l=0, r=0, t=20, b=0),
    height=700
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
