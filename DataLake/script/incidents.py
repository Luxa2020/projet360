import pandas as pd
import random
import uuid
from faker import Faker

fake = Faker()
random.seed(42)

# Liste des 20 identifiants de véhicules (cohérents avec les fichiers précédents)
vehicle_ids = [f"VEH_{i:03}" for i in range(20)]

# Liste d'exemples d'incidents réalistes
descriptions = [
    "Panne moteur",
    "Crevaison",
    "Retard passagers",
    "Accident",
    "Manifestation"
]

# Génération de 100 incidents
data = []
for _ in range(100):
    data.append({
        "incident_id": f"INC_{uuid.uuid4().hex[:6].upper()}",  # identifiant unique
        "vehicle_id": random.choice(vehicle_ids),              # cohérence avec véhicules
        "timestamp": fake.date_time_between(start_date="-2d", end_date="now"),  # heure réaliste
        "description": random.choice(descriptions),
        "delay_minutes": random.randint(1, 60),                # délai en minutes
        "severity": random.randint(1, 5)                       # gravité de 1 (léger) à 5 (grave)
    })

# Export au format CSV
df = pd.DataFrame(data)
df.to_csv("n5_incidents.csv", index=False)
