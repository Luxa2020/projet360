import mysql.connector
import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv("transport_com.csv")

# Remplacer les NaN par None pour MySQL
df = df.where(pd.notnull(df), None)

# Vérifier les noms de colonnes du CSV
print("Colonnes CSV :", df.columns)

# Configuration de la connexion
conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="root",
    database="testdb"
)

# Lancer la connexion
cursor = conn.cursor()

# Création de la table dans la DB
cursor.execute("DROP TABLE IF EXISTS operateurs")
cursor.execute(
    """
    
    CREATE TABLE IF NOT EXISTS operateurs(
        id INT AUTO_INCREMENT PRIMARY KEY,
        operateur LONGTEXT,
        city VARCHAR(500),
        etat VARCHAR(200),
        contry VARCHAR(200)
    )"""
)

# Insertion des données
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO operateurs (operateur, city, etat, contry) VALUES (%s, %s, %s, %s)",
        (row['Operator'], row['City'], row['State / Province'], row['Country'])
    )

# Envoi des données
conn.commit()      # Sauvegarder les changements
cursor.close()     # Fermer le curseur
conn.close()       # Fermer la connexion

print("Insertion terminée avec succès !")



# import mysql.connector
# import pandas as pd

# # 1️⃣ Connexion à la base
# conn = mysql.connector.connect(
#     host="localhost",
#     port=3307,
#     user="root",
#     password="root",
#     database="testdb"
# )

# cursor = conn.cursor()

# #  Exécuter la requête SELECT
# cursor.execute("SELECT * FROM operateurs")  # Lire toutes les lignes de la table

# #  Récupérer les résultats
# rows = cursor.fetchall()  # récupère toutes les lignes

# #  Afficher les résultats
# for row in rows:
#     print(row)

# #  Optionnel : convertir en DataFrame Pandas
# df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
# print(df)

# #  Fermer la connexion
# cursor.close()
# conn.close()
