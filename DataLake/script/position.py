import pandas as pd
import random
from faker import Faker
from datetime import datetime

fake = Faker()
random.seed(42)

# Définir les zones et leurs coordonnées
zone_coords = {
    "Zone Nord": {"lat": (14.7500, 14.7700), "log": (-17.4700, -17.4500)},
    "Centre-ville": {"lat": (14.6900, 14.7100), "log": (-17.4600, -17.4400)},
    "Zone Sud": {"lat": (14.6300, 14.6500), "log": (-17.4800, -17.4600)},
}

# Fonction pour générer des coordonnées dans une zone
def generate_coord(zone):
    lat_range = zone_coords[zone]["lat"]
    log_range = zone_coords[zone]["log"]
    return (
        round(random.uniform(*lat_range), 6),
        round(random.uniform(*log_range), 6)
    )

# Lire les véhicules depuis le fichier n1
vehicules_df = pd.read_csv("n1_vehicules.csv")
vehicle_ids = vehicules_df["vehicule_id"].tolist()

# Attribuer une zone fixe par véhicule
zones = list(zone_coords.keys())
vehicle_zones = {vid: random.choice(zones) for vid in vehicle_ids}

# Routes
routes = [f"R{i:02}" for i in range(10)]
directions = ["Nord", "Sud", "Est", "Ouest", "Nord-Est", "Sud-Ouest"]

# Générer les données de position
data = []
for _ in range(100):
    veh_id = random.choice(vehicle_ids)
    zone = vehicle_zones[veh_id]
    lat, log = generate_coord(zone)
    
    data.append({
        "route_id": random.choice(routes),
        "vehicule_id": veh_id,
        "timestamp": fake.date_time_between(start_date="-2d", end_date="now").strftime('%Y-%m-%d %H:%M:%S'),
        "latitude": lat,
        "longitude": log,
        "speed_kmh": round(random.uniform(0, 80), 1),
        "direction": random.choice(directions),
        "traffic_level": random.randint(0, 3)
    })

# Sauvegarder le fichier
df = pd.DataFrame(data)
df.to_csv("n2_positions.csv", index=False)
