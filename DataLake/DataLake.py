# Import des librairies nécessaires
from pymongo import MongoClient       # Pour se connecter et manipuler MongoDB
import mysql.connector                # Pour se connecter à MySQL
import pandas as pd                   # Pour manipuler les données sous forme de DataFrame
from hdfs import InsecureClient       # Pour écrire des fichiers sur HDFS

# ---------------- MONGODB ----------------
# Connexion au serveur MongoDB local
mongo_client = MongoClient("mongodb://localhost:27017/")  # 27017 est le port par défaut de MongoDB

# Connexion à la base de données "vehicules"
mongo_db = mongo_client["vehicules"]

# Connexion à la collection "vehicules"
# Si elle n'existe pas, MongoDB la crée automatiquement lors de la première insertion
mongo_collection = mongo_db["vehicules"]

# Récupération de toutes les données de la collection
# find() retourne un curseur, list() convertit en liste de dictionnaires
mongo_data = list(mongo_collection.find())

# Conversion des données MongoDB en DataFrame Pandas pour une manipulation plus facile
df_mongo = pd.DataFrame(mongo_data)

# Supprimer la colonne '_id' générée automatiquement par MongoDB
# Cela évite des problèmes lors de l'écriture CSV ou traitement ultérieur
if '_id' in df_mongo.columns:
    df_mongo.drop(columns=['_id'], inplace=True)

# Afficher la forme du DataFrame pour vérifier le nombre de lignes et de colonnes
print("MongoDB data shape:", df_mongo.shape)

# ---------------- MYSQL ----------------
# Connexion à MySQL avec mysql.connector
mysql_conn = mysql.connector.connect(
    host="localhost",        # Hôte du serveur MySQL
    user="user",             # Nom d'utilisateur MySQL
    password="password",     # Mot de passe MySQL
    database="testdb",       # Nom de la base de données
    port=3307                # Port MySQL mappé par Docker
)

# Requête SQL pour récupérer les données d'une table spécifique
query = "SELECT * FROM operateurs;"  # Remplacer "votre_table" par le nom réel de votre table

# Lire les données MySQL directement dans un DataFrame Pandas
df_mysql = pd.read_sql(query, mysql_conn)

# Fermer la connexion MySQL après récupération des données
mysql_conn.close()

# Afficher la forme du DataFrame MySQL
print("MySQL data shape:", df_mysql.shape)

# ---------------- HDFS ----------------
# Connexion au HDFS via InsecureClient
# "localhost:9870" correspond au port web UI du NameNode
hdfs_client = InsecureClient('http://localhost:9870', user='hadoop')

# Chemins des fichiers à créer sur HDFS
hdfs_mongo_path = '/data/vehicules/mongo_vehicules.csv'  # Chemin HDFS pour MongoDB
hdfs_mysql_path = '/data/vehicules/mysql_table.csv'       # Chemin HDFS pour MySQL

# Ecriture du DataFrame MongoDB sur HDFS au format CSV
# overwrite=True permet d'écraser le fichier s'il existe déjà
with hdfs_client.write(hdfs_mongo_path, encoding='utf-8', overwrite=True) as f:
     df_mongo.to_csv(f, index=False)  # index=False pour ne pas écrire la colonne d'index


# Ecriture du DataFrame MySQL sur HDFS au format CSV
with hdfs_client.write(hdfs_mysql_path, encoding='utf-8', overwrite=True) as f:
    df_mysql.to_csv(f, index=False)


# Confirmation de l'écriture sur HDFS
print("Donnees inserees")
