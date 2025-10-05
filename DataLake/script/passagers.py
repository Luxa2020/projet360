import pandas as pd
import random
from faker import Faker

fake = Faker()
random.seed(42)

# Zones fixes
zones = ["Zone Nord", "Centre-ville", "Zone Sud"]

# 5 arrêts par zone
zone_stops = {
    "Zone Nord": [f"STOP_NORD_{i}" for i in range(1, 6)],
    "Centre-ville": [f"STOP_CENTRE_{i}" for i in range(1, 6)],
    "Zone Sud": [f"STOP_SUD_{i}" for i in range(1, 6)],
}

# Capacités par type de transport
vehicle_types = {
    "Bus": 60,
    "Taxi": 4,
    "Train": 500,
    "Car rapide": 25
}

# Lire les véhicules
vehicules_df = pd.read_csv("n1_vehicules.csv")
vehicle_ids = vehicules_df["vehicule_id"].tolist()

# Associer à chaque véhicule sa zone (même logique que dans n2)
vehicle_zones = {vid: random.choice(zones) for vid in vehicle_ids}

# Associer à chaque véhicule sa capacité (donnée dans n1)
vehicle_capacity = dict(zip(
    vehicules_df["vehicule_id"], 
    vehicules_df["capacite"]
))

data = []
for _ in range(100):
    veh_id = random.choice(vehicle_ids)
    zone = vehicle_zones[veh_id]
    stop_id = random.choice(zone_stops[zone])
    capacity = vehicle_capacity[veh_id]
    
    data.append({
        "passenger_count": random.randint(0, capacity),
        "timestamp": fake.date_time_between(start_date="-2d", end_date="now").strftime('%Y-%m-%d %H:%M:%S'),
        "vehicle_id": veh_id,
        "stop_id": stop_id,
        "boarding": random.choice([True, False]),
        "alighting": random.choice([True, False])
    })

df = pd.DataFrame(data)
df.to_csv("n3_passagers.csv", index=False)
