import time
import random
import pandas as pd

# Initialisation des 100 véhicules
vehicles = [f"VEH_{i:03}" for i in range(100)]

# Générer des positions initiales autour de Dakar
positions = {
    veh_id: {
        "latitude": random.uniform(14.6900, 14.7100),
        "longitude": random.uniform(-17.4600, -17.4400),
        "speed_kmh": round(random.uniform(20, 60), 1),
        "direction": random.choice(["Nord", "Sud", "Est", "Ouest", "Sud-Est", "Nord-Ouest"])
    }
    for veh_id in vehicles
}

def update_position(pos):
    # Simuler un léger déplacement aléatoire
    delta_lat = random.uniform(-0.0005, 0.0005)
    delta_log = random.uniform(-0.0005, 0.0005)
    pos["latitude"] += delta_lat
    pos["longitude"] += delta_log
    pos["latitude"] = round(pos["latitude"], 6)
    pos["longitude"] = round(pos["longitude"], 6)
    pos["speed_kmh"] = round(random.uniform(20, 60), 1)
    return pos

# Simuler le streaming temps réel
try:
    while True:
        records = []
        timestamp = pd.Timestamp.now()
        for veh_id, pos in positions.items():
            pos = update_position(pos)
            record = {
                "timestamp": timestamp,
                "vehicle_id": veh_id,
                "latitude": pos["latitude"],
                "longitude": pos["longitude"],
                "speed_kmh": pos["speed_kmh"],
                "direction": pos["direction"]
            }
            records.append(record)

        df = pd.DataFrame(records)
        print(df.head(3))  # Exemple : afficher seulement les 3 premières lignes
        df.to_csv("stream_positions.csv", mode='a', index=False, header=False)  # append
        time.sleep(60)  # Pause de 5 secondes pour simuler le temps réel

except KeyboardInterrupt:
    print(" Simulation stoppée par l'utilisateur.")
