import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        print(f"Connexion à {url}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(" Connexion réussie!")
        
    except requests.exceptions.RequestException as e:
        print(f" Erreur lors de la connexion : {e}")
        return None
    
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Chercher tous les tableaux
        tables = soup.find_all("table")
        
        if not tables:
            print(" Aucun tableau trouvé sur la page.")
            return None
        
        print(f" {len(tables)} tableau(x) trouvé(s)")
        
        # Traiter chaque tableau
        all_data = []
        
        for idx, table in enumerate(tables, 1):
            print(f"\n--- Tableau {idx} ---")
            
            # Extraire les en-têtes (th)
            headers_row = table.find("tr")
            headers = []
            
            if headers_row:
                th_elements = headers_row.find_all(["th", "td"])
                headers = [th.get_text(strip=True) for th in th_elements]
                print(f"En-têtes: {headers}")
            
            # Extraire toutes les lignes de données
            rows = table.find_all("tr")[1:]  # Skip header row
            table_data = []
            
            for row in rows:
                cells = row.find_all(["td", "th"])
                row_data = [cell.get_text(strip=True) for cell in cells]
                if row_data:  # Ignorer les lignes vides
                    table_data.append(row_data)
            
            print(f"Nombre de lignes de données: {len(table_data)}")
            
            # Afficher les premières lignes
            if table_data:
                print("\nPremières lignes:")
                for i, row in enumerate(table_data[:5], 1):
                    print(f"  {i}. {row}")
                
                if len(table_data) > 5:
                    print(f"  ... et {len(table_data) - 5} autres lignes")
            
            # Stocker les données avec les en-têtes
            all_data.append({
                'headers': headers,
                'data': table_data
            })
        
        return all_data
        
    except Exception as e:
        print(f" Erreur lors du parsing HTML : {e}")
        return None

def save_to_csv(table_data, filename="scraped_data.csv"):
    """Sauvegarder les données du premier tableau en CSV"""
    if not table_data or not table_data[0]['data']:
        print(" Pas de données à sauvegarder")
        return
    
    try:
        headers = table_data[0]['headers']
        data = table_data[0]['data']
        
        # Créer un DataFrame pandas
        df = pd.DataFrame(data, columns=headers if headers else None)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f" Données sauvegardées dans {filename}")
        
    except Exception as e:
        print(f" Erreur lors de la sauvegarde : {e}")

# Lancement
if __name__ == "__main__":
    url = "https://www.transit.land/operators"
    
    # Scraper les tableaux
    scraped_data = scrape_table(url)
    
    if scraped_data:
        # Optionnel : sauvegarder en CSV
        save_to_csv(scraped_data, "transit_operators.csv")
        
        # Afficher un résumé
        print(f"\ Résumé: {len(scraped_data)} tableau(x) extrait(s)")
        for i, table in enumerate(scraped_data, 1):
            print(f"  Tableau {i}: {len(table['headers'])} colonnes, {len(table['data'])} lignes")