import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from folium import PolyLine
from geopy.distance import geodesic
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Suivi Véhicules Temps Réel", layout="wide")
st_autorefresh(interval=5000, key="refresh_map")  # Auto-refresh toutes les 5 secondes

st.title("🚗 Suivi en temps réel des véhicules")

# Centre de la carte (Dakar)
center = [14.695, -17.445]

# Lire les données
try:
    df = pd.read_csv("n2_positions.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # Carte Folium
    m = folium.Map(location=center, zoom_start=13)

    # Couleurs pour différencier les véhicules
    colors = ["red", "blue", "green", "orange", "purple", "darkred", "lightblue", "cadetblue"]

    stats = []
    alerts = []

    for i, (vehicule_id, group) in enumerate(df.groupby("vehicule_id")):
        color = colors[i % len(colors)]

        coords = group[["latitude", "longitude"]].values.tolist()
        times = group["timestamp"].tolist()
        speeds = group["speed_kmh"].tolist()

        # Distance parcourue
        distance = sum(geodesic(coords[i], coords[i+1]).km for i in range(len(coords)-1))

        # Durée de trajet
        duration = (times[-1] - times[0]).total_seconds() / 60  # en minutes

        # Vitesse moyenne/max
        avg_speed = np.mean(speeds)
        max_speed = np.max(speeds)

        # Niveau de trafic moyen
        avg_traffic = group["traffic_level"].mean()

        # Arrêts fréquents
        stop_counts = group.groupby(["latitude", "longitude"]).size()
        frequent_stops = stop_counts[stop_counts > 1].count()

        stats.append({
            "id": vehicule_id,
            "distance": round(distance, 2),
            "duration": round(duration, 2),
            "avg_speed": round(avg_speed, 1),
            "max_speed": round(max_speed, 1),
            "avg_traffic": round(avg_traffic, 1),
            "frequent_stops": frequent_stops
        })

        # Alertes
        if max_speed > 100:
            alerts.append(f"🚨 Vitesse excessive détectée pour {vehicule_id}: {max_speed} km/h")
        if frequent_stops >= 3:
            alerts.append(f"😴 Véhicule {vehicule_id} s'arrête souvent")

        # Trajectoire historique
        if len(coords) > 1:
            PolyLine(coords, color=color, weight=3, opacity=0.6).add_to(m)

        # Marqueur
        last_row = group.iloc[-1]
        popup_text = f"""
        🆔 Véhicule: {last_row['vehicule_id']}<br>
        🛣️ Route: {last_row['route_id']}<br>
        🧭 Direction: {last_row['direction']}<br>
        💨 Vitesse: {last_row['speed_kmh']} km/h<br>
        🔴 Trafic: {last_row['traffic_level']}<br>
        ⏱️ {last_row['timestamp']}
        """
        folium.Marker(
            location=[last_row["latitude"], last_row["longitude"]],
            popup=popup_text,
            icon=folium.Icon(color=color, icon="car", prefix="fa")
        ).add_to(m)

        # Ligne du haut : KPIs (col1) et Carte (col2)
    col1, col2 = st.columns([1, 2])

    with col1:
        stats_df = pd.DataFrame(stats)

        # Sélection de véhicule
        selected_vehicle = st.selectbox("🚘 Sélectionnez un véhicule", stats_df["id"].unique())

        # Filtrer les stats et les données pour ce véhicule
        selected_stats = stats_df[stats_df["id"] == selected_vehicle].iloc[0]
        selected_data = df[df["vehicule_id"] == selected_vehicle]

        st.header("📊 KPIs")
        st.metric("📍 Distance (km)", selected_stats["distance"])
        st.metric("💨 Vitesse max (km/h)", selected_stats["max_speed"])
        st.metric("⚡ Vitesse moyenne", selected_stats["avg_speed"])
        st.metric("⏱️ Durée (min)", selected_stats["duration"])
        st.metric("🔴 Trafic moyen", selected_stats["avg_traffic"])
        st.metric("🛑 Arrêts fréquents", selected_stats["frequent_stops"])

    with col2:
        st_folium(m, width=1000, height=500)
        st.success(f"🕒 Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")

    # Ligne du bas : Graphiques
    col3, col4 = st.columns(2)

    with col3:
        st.header("📈 Vitesse")
        st.plotly_chart(px.line(selected_data, x="timestamp", y="speed_kmh", title="Évolution de la vitesse"), use_container_width=True)

    with col4:
        st.header("📉 Trafic")
        st.plotly_chart(px.line(selected_data, x="timestamp", y="traffic_level", title="Évolution du trafic"), use_container_width=True)


    st.header("🚦 Alertes")
    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.info("Aucune alerte détectée")

except FileNotFoundError:
    st.error(" Fichier `n2_positions.csv` non trouvé.")
except Exception as e:
    st.error(f" Erreur : {e}")
