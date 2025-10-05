import pandas as pd
import random
import datetime
from faker import Faker

faker = Faker()
random.seed(42)


# Definir les coordonnees geographiques de chaque zone
zone_coords = {
    "Zone Nord": {
        "lat": (14.7500, 14.7700),
        "log": (-17.4700, -17.4500)
    },
    "Centre ville": {
        "lat": (14.6900, 14.7100),
        "log": (-17.4600, -17.4400)
    },
    "Zone Sud": {
        "lat": (14.6300, 14.6500),
        "log": (-17.4800, -17.4600)
    }
}


#Cette fonction permet de generer une longitud et une latitude pour une zone donnee
def creer_coord (zone):
    lat_range = zone_coords[zone]["lat"]
    log_range = zone_coords[zone]["log"]
    return(
        round(random.uniform(*lat_range), 6),
        round(random.uniform(*log_range), 6)
    )


#Creeation des vehicule et leur capacite

vehicules = {
    "Bus":60,
    "Taxi": 4,
    "Train": 500,
    "Car rapide": 25
}

#Creation des listes des types de transports , leur type de consommation et leur compagnie
compagnie =["Aftu", "Dakar Dem Dikk","Ter", "Brt"]
energie_cons = ["Diesel","Electric", "Essence"]
status=["en service", "en panne ", "guarer"]


#initialisation du liste de donnee
Donnee_vehicule=[]

#creeation des donnees et stockage
for i in range(100):
    type_transport = random.choice(list(vehicules.keys()))
    vehicules_id = f"VEH_{i:03}"
    Donnee_vehicule.append({
        "vehicule_id":vehicules_id,
        "type_transport": type_transport,
        "nom_compagnie": random.choice(compagnie),
        "capacite":vehicules[type_transport],
        "status": random.choice(status),
        "consomation": random.choice(energie_cons)
    })

df = pd.DataFrame(Donnee_vehicule)

df.to_csv("n1_vehicules.csv", index=False)





