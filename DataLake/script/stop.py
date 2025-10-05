import pandas as pd
import random
from faker import Faker

fake = Faker()
random.seed(42)

# Coordonnées géographiques par zone
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

zones = list(zone_coords.keys())
stops_data = []

stop_counter = 1
for zone in zones:
    for i in range(5):
        lat, log = generate_coord(zone)
        stop_id = f"STOP_{stop_counter:03}"
        stop_counter += 1
        stops_data.append({
            "stop_id": stop_id,
            "name": f"{fake.word().capitalize()} {fake.word().capitalize()}",
            "latitude": lat,
            "longitude": log,
            "zone": zone,
            "shelter": random.choice([True, False])
        })

df = pd.DataFrame(stops_data)
df.to_csv("n4_arrets.csv", index=False)
