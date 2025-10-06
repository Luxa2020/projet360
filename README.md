Projet DataFlow360


Groupe3-Thème : Optimisation du Transport Urbain par Analyse Intelligente des Données

Plateforme de suivi et d’analyse du transport urbain en temps réel, basée sur les données GPS des véhicules


Fonctionnalites:

    Liste les principales fonctions :

        -Suivi des véhicules en temps réel

        -Visualisation sur carte

        -Calcul des distances / vitesses

        -Génération de rapports ou statistiques

        -Notifications ou alertes
        



Architechture du projet

    DataLake: Collecte et ingestion des donnees brutes
    EDA-ETL: Traitement et Transformation des donnees 
    DataWareHouse: Stockages des donnees structures
    ELK: Ingestion des donnees en temps reel
    Visualisation ddes trafifs


    360/
        |360env/                # Creer un environnement virtuel
        |DataLake/              # Dossier collecte de donnees
        |  --Scrap/
        |  -----scrap.py        # Donnees scrapes
        |  --script/
        |  -----script.py       # Donnees generees
        |  --st/
        |  -----st.py           # Donnees simules a partir de Donnees generees
        |  stockageDbDif/       # Stockages des donnees sur differentes bases
        |  --mongo.py           # Stockages de certaines  donnees sur mongo 
        |  --SQLDb.py           # Stockages certaines sur SQL
        |  DataLake.py          # Stockages des donnees brutes dans une seule base
        |  
        |elk/                   # Ingestion temps reel
        |EDA-ETL/               # Chargement et transformation des donnees
        |DataWareHouse/         #Stockages des datamarts (etapes sautees)
        |  --    
        |cart.py                #applications streamlit pour visualisations et suivi en temps reel
        |.gitignore             # ignorer le deploiement des bases de donnees(mongo,sql,hdfs)
        |docker-compose.yml     #dockerisation des bases pour evites les versions 
        |requirements.txt       # liste des dependances utilisees
        |README.md              # Documentation du projet
        |.env                   # Confidentialite des mots de passes
        |DesFichiers.csv inutiles


Installation et exécution:

        git clone https://github.com/Luxa2020/projet360
        cd 360
        pip install -r requirements.txt
        docker-compose up -d
        streamlit run cart.py



Technologies:

     python3                # langage de programmation
     streamlit              # framework python
     folium                 # librairie python pour le map
     mongodb                # base de donnees NoSql
     mysql                  # Base de donnees SQL
     hdfs                   # ouitls Big Data pour stockage brute
     beautifulSoup          # librairie pour le scraping

