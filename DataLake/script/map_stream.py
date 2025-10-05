import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Charger les données
df = pd.read_csv("n2_positions.csv")

# Créer une carte centrée sur Dakar
m = folium.Map(location=[14.6928, -17.4467], zoom_start=12)

# Ajouter les marqueurs pour chaque véhicule
for _, row in df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"Véhicule: {row['vehicle_id']}<br>Speed: {row['speed_kmh']} km/h",
        icon=folium.Icon(color="blue", icon="bus", prefix="fa")
    ).add_to(m)

# Afficher la carte
st.title("📍 Carte des positions des véhicules")
st_data = st_folium(m, width=700, height=500)
