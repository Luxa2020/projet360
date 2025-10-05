from pymongo import MongoClient, errors
import pandas as pd
import os

folder_path = "/home/lux/Documents/veille/360/DataLake/script/"


client = MongoClient("mongodb://localhost:27017/")
db = client["vehicules_db"]

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        filepath = os.path.join(folder_path, filename)
        
        df = pd.read_csv(filepath)
        df = df.where(pd.notnull(df), None)

        # On choisit un ou plusieurs champs comme identifiant unique
        # Par exemple ici, on suppose qu'il y a une colonne 'id' ou on peut créer un hash
        if 'id' not in df.columns:
            df['id'] = df.apply(lambda row: hash(tuple(row)), axis=1)  # hash de toute la ligne

        data = df.to_dict(orient="records")
        collection_name = os.path.splitext(filename)[0]
        collection = db[collection_name]

        # Création d'un index unique sur 'id' pour éviter les doublons
        collection.create_index("id", unique=True)

        for record in data:
            try:
                collection.insert_one(record)
            except errors.DuplicateKeyError:
                # On ignore les doublons
                continue

        print(f"{len(data)} documents traités dans '{collection_name}'")
