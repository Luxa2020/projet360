import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from folium import PolyLine, DivIcon
from geopy.distance import geodesic
import numpy as np
import plotly.express as px
import folium.plugins as plugins

# Configuration page
st.set_page_config(page_title="Application de  suivi Véhicules Temps Réel", layout="wide")
st_autorefresh(interval=3000, key="refresh_map")

#  CSS personnalisé optimisé
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #001F3F 0%, #003366 100%);
        color: white;
    }
    
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: white !important;
    }
    
    /* Conteneur principal des KPIs - RÉDUIT */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 15px 0;
        padding: 0 5px;
    }
    
    /* Carte KPI moderne - DIMENSIONS RÉDUITES */
    .kpi-card {
        background: linear-gradient(135deg, #0074D9 0%, #0056b3 100%);
        border-radius: 12px;
        padding: 14px 17px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 116, 217, 0.4);
    }
    
    .kpi-icon {
        font-size: 27px;
        margin-bottom: 5px;
        opacity: 0.9;
    }
    
    .kpi-label {
        font-size: 30px;
        font-weight: 500;
        opacity: 0.85;
        margin: 5px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 40px;
        font-weight: 700;
        margin: 3px 0;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .kpi-unit {
        font-size: 25px;
        opacity: 0.7;
        font-weight: 400;
    }
    
    /* Style pour le selectbox */
    .stSelectbox > div > div {
        background-color: #0074D9;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Titres avec style - RÉDUIT */
    .section-title {
        font-size: 30px;
        font-weight: 700;
        margin: 20px 0 15px 0;
        padding-left: 10px;
        border-left: 4px solid #0074D9;
    }
    
    /* Amélioration des graphiques - RÉDUIT */
    .plot-container {
        background: rgba(0, 116, 217, 0.1);
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Carte améliorée */
    .map-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        margin: 15px 0;
    }
    
    /* Alertes stylées - RÉDUIT */
    .alert-box {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        border-radius: 8px;
        padding: 10px 15px;
        margin: 8px 0;
        box-shadow: 0 4px 12px rgba(255, 68, 68, 0.3);
        font-size: 13px;
    }
    
    /* Animation de chargement */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .updating {
        animation: pulse 2s infinite;
    }
    
    /* Réduction espace titre */
    h1 {
        margin-bottom: 10px !important;
        font-size: 28px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title(" Suivi en temps réel des véhicules 🚗")

# Centre de la carte (Dakar)
center = [14.695, -17.445]

try:
    df = pd.read_csv("n2_positions.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # Carte Folium avec plugins pour animation
    m = folium.Map(location=center, zoom_start=13, tiles="CartoDB positron")
    
    # Activer le plugin d'animation
    plugins.TimestampedGeoJson(
        {
            'type': 'FeatureCollection',
            'features': []
        },
        period='PT1S',
        add_last_point=True,
        auto_play=True,
        loop=True,
        max_speed=1,
        loop_button=True,
        date_options='YYYY-MM-DD HH:mm:ss',
        time_slider_drag_update=True
    ).add_to(m)

    # Couleurs pour les véhicules
    colors = ["#FF0000", "#0000FF", "#00FF00", "#FFA500", "#800080", "#8B0000", "#87CEEB", "#5F9EA0"]
    
    stats = []
    alerts = []

    for i, (vehicule_id, group) in enumerate(df.groupby("vehicule_id")):
        color = colors[i % len(colors)]
        coords = group[["latitude", "longitude"]].values.tolist()
        times = group["timestamp"].tolist()
        speeds = group["speed_kmh"].tolist()

        distance = sum(geodesic(coords[i], coords[i+1]).km for i in range(len(coords)-1))
        duration = (times[-1] - times[0]).total_seconds() / 60
        avg_speed = np.mean(speeds)
        max_speed = np.max(speeds)
        avg_traffic = group["traffic_level"].mean()
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

        if max_speed > 100:
            alerts.append(f"🚨 Vitesse excessive détectée pour {vehicule_id}: {max_speed} km/h")
        if frequent_stops >= 3:
            alerts.append(f"😴 Véhicule {vehicule_id} s'arrête souvent")

        # Tracer l'itinéraire complet (ligne continue)
        if len(coords) > 1:
            PolyLine(
                coords, 
                color=color, 
                weight=4, 
                opacity=0.7,
                popup=f"Itinéraire {vehicule_id}"
            ).add_to(m)
            
            # Ajouter des points intermédiaires pour montrer le trajet
            for idx, (coord, speed, time) in enumerate(zip(coords, speeds, times)):
                if idx % 3 == 0:  # Afficher un point tous les 3 pour éviter surcharge
                    folium.CircleMarker(
                        location=coord,
                        radius=2,
                        color=color,
                        fill=True,
                        fillColor=color,
                        fillOpacity=0.6,
                        popup=f"Point {idx} - {speed} km/h"
                    ).add_to(m)

        # Position actuelle avec icône de voiture
        last_row = group.iloc[-1]
        
        # Déterminer la rotation en fonction de la direction
        direction_angles = {
            'Nord': 0, 'Sud': 180, 'Est': 90, 'Ouest': 270,
            'Nord-Est': 45, 'Nord-Ouest': 315, 'Sud-Est': 135, 'Sud-Ouest': 225
        }
        angle = direction_angles.get(last_row['direction'], 0)
        
        # Créer une icône de voiture personnalisée avec rotation
        car_icon_html = f"""
            <div style="transform: rotate({angle}deg); font-size: 24px;">
                🚗
            </div>
        """
        
        popup_text = f"""
        <div style="font-family: Arial; font-size: 12px;">
            <b>🆔 {last_row['vehicule_id']}</b><br>
            🛣️ Route: {last_row['route_id']}<br>
            🧭 Direction: {last_row['direction']}<br>
            💨 Vitesse: <b>{last_row['speed_kmh']} km/h</b><br>
            🔴 Trafic: {last_row['traffic_level']}<br>
            ⏱️ {last_row['timestamp'].strftime('%H:%M:%S')}
        </div>
        """
        
        folium.Marker(
            location=[last_row["latitude"], last_row["longitude"]],
            popup=folium.Popup(popup_text, max_width=250),
            icon=DivIcon(html=car_icon_html)
        ).add_to(m)
        
        # Ajouter un cercle pulsant autour de la position actuelle
        folium.CircleMarker(
            location=[last_row["latitude"], last_row["longitude"]],
            radius=15,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.2,
            weight=2
        ).add_to(m)

    # === Sélection du véhicule ===
    stats_df = pd.DataFrame(stats)
    st.markdown("<br>", unsafe_allow_html=True)
    selected_vehicle = st.selectbox("🚘 Sélectionnez un véhicule", stats_df["id"].unique())
    selected_stats = stats_df[stats_df["id"] == selected_vehicle].iloc[0]
    selected_data = df[df["vehicule_id"] == selected_vehicle]

    # === KPIs en grille 3x2 - RÉDUITS ===
    # Première ligne (3 KPIs)
    st.markdown("""
    <div class='kpi-grid'>
        <div class='kpi-card'>
            <div class='kpi-icon'>📍</div>
            <div class='kpi-label'>Distance</div>
            <div class='kpi-value'>{}<span class='kpi-unit'> km</span></div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-icon'>⚡</div>
            <div class='kpi-label'>Moy. Vitesse</div>
            <div class='kpi-value'>{}<span class='kpi-unit'> km/h</span></div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-icon'>💨</div>
            <div class='kpi-label'>Vitesse Max</div>
            <div class='kpi-value'>{}<span class='kpi-unit'> km/h</span></div>
        </div>
    </div>
    """.format(
        selected_stats['distance'],
        selected_stats['avg_speed'],
        selected_stats['max_speed']
    ), unsafe_allow_html=True)
    
    # Deuxième ligne (3 KPIs)
    st.markdown("""
    <div class='kpi-grid'>
        <div class='kpi-card'>
            <div class='kpi-icon'>⏱️</div>
            <div class='kpi-label'>Durée</div>
            <div class='kpi-value'>{}<span class='kpi-unit'> min</span></div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-icon'>🔴</div>
            <div class='kpi-label'>Trafic</div>
            <div class='kpi-value'>{}</div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-icon'>🛑</div>
            <div class='kpi-label'>Arrêts</div>
            <div class='kpi-value'>{}</div>
        </div>
    </div>
    """.format(
        selected_stats['duration'],
        selected_stats['avg_traffic'],
        selected_stats['frequent_stops']
    ), unsafe_allow_html=True)

    # === Carte en priorité ===
    st.markdown("<div class='section-title'>🗺️ Suivi en direct</div>", unsafe_allow_html=True)
    st.markdown("<div class='map-container'>", unsafe_allow_html=True)
    st_folium(m, width=None, height=550, key="main_map")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.success(f"🕒 Mise à jour auto : {datetime.now().strftime('%H:%M:%S')} • Actualisation toutes les 3s")

    # === Dashboard - Graphiques compacts ===
    st.markdown("<div class='section-title'>📊 Analyses</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
        st.markdown("#### 📊 Vitesses")
        fig_hist = px.histogram(selected_data, x="speed_kmh", nbins=15,
                                color_discrete_sequence=["#7FDBFF"],
                                labels={"speed_kmh": "Vitesse (km/h)", "count": "Freq."})
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", size=10),
            margin=dict(l=20, r=20, t=10, b=20),
            height=280,
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
        st.markdown("#### 🟢 Trafic")
        fig_pie = px.pie(selected_data, names="traffic_level",
                         color_discrete_sequence=px.colors.sequential.Blues,
                         hole=0.4)
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", size=10),
            margin=dict(l=20, r=20, t=10, b=20),
            height=280,
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # === Alertes compactes ===
    st.markdown("<div class='section-title'>🚦 Alertes</div>", unsafe_allow_html=True)
    if alerts:
        for alert in alerts:
            st.markdown(f"<div class='alert-box'>{alert}</div>", unsafe_allow_html=True)
    else:
        st.success("✅ Aucune alerte")

except FileNotFoundError:
    st.error(" Fichier `n2_positions.csv` non trouvé.")
except Exception as e:
    st.error(f" Erreur : {e}")