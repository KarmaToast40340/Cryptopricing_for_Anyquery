import subprocess
import os
import requests
import csv


def delete_wallet_csv():
    csv_file_path = os.path.expanduser('Cryptopricingplugin/Wallet.csv')
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
        print(f"{csv_file_path} has been deleted.")
    else:
        print(f"The file {csv_file_path} does not exist.")

delete_wallet_csv()

def execute_bash_commands():
    # Chemin du répertoire où exécuter les commandes
    working_directory = os.path.expanduser("Cryptopricingplugin")
    
    # Chemin du fichier SQL
    sql_file_path = os.path.join(working_directory, "requests.sql")

    try:
        # Lire le contenu du fichier SQL
        with open(sql_file_path, "r") as sql_file:
            sql_commands = sql_file.read()
        
        # Exécuter Anyquery dans le répertoire spécifié
        result = subprocess.run(
            ["anyquery", "--dev"],
            input=sql_commands,  # Fournir les commandes SQL via stdin
            text=True,           # Indiquer que l'entrée/sortie est du texte
            capture_output=True, # Capturer stdout et stderr
            cwd=working_directory # Définit le répertoire de travail
        )
        
        # Afficher la sortie et les erreurs
        print("Output:", result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    execute_bash_commands()

# Définir votre token Notion et l'ID de la base de données
NOTION_TOKEN = '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'  # Remplacez par votre token
DATABASE_ID = '14486a6b24b6802698c9c019a1af6b69'  # Remplacez par l'ID de votre base de données Notion
NOTION_API_URL = "https://api.notion.com/v1/pages"
DATABASE_URL = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"  # URL pour récupérer les données

# Définir l'URL d'API Notion et les en-têtes nécessaires
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"  # Utilisez la version appropriée de l'API
}

# Fonction pour mettre à jour une page dans Notion
def update_notion_page(page_id, updated_properties):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.patch(url, headers=headers, json=updated_properties)
    return response.json()

# Fonction pour récupérer toutes les pages de la base de données Notion
def get_existing_notion_pages():
    try:
        response = requests.post(DATABASE_URL, headers=headers)
        if response.status_code == 200:
            return response.json()["results"]
        else:
            print(f"Error fetching database entries: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred while fetching data from Notion: {e}")
        return []

# Fonction pour ajouter ou mettre à jour une page dans Notion
def add_or_update_notion_page(data):
    # Récupérer toutes les pages existantes de la base de données Notion
    existing_pages = get_existing_notion_pages()
    
    # Chercher une page avec le même "Currency"
    page_to_update = None
    for page in existing_pages:
        currency_property = page['properties'].get('Currency', {}).get('title', [])
        if currency_property and currency_property[0].get('text', {}).get('content') == data["Currency"]:
            page_to_update = page
            break

    # Si une page avec cette "Currency" existe, mettre à jour
    if page_to_update:
        # ID de la page à mettre à jour
        page_id = page_to_update["id"]
        notion_data = {
            "properties": {
                "Currency": {
                    "title": [
                        {
                            "text": {
                                "content": data["Currency"]
                            }
                        }
                    ]
                },
                "Quantity": {
                    "number": float(data["Quantity"])
                },
                "UnitValue": {
                    "number": float(data["UnitValue"])
                },
                "TotalValue": {
                    "number": float(data["TotalValue"])
                }
            }
        }
        # Mettre à jour la page
        response = update_notion_page(page_id, notion_data)
        if response.get("object") == "page":
            print(f"Page {data['Currency']} updated successfully.")
        else:
            print(f"Failed to update page {data['Currency']}.")
    else:
        # Si aucune page avec cette "Currency" n'existe, créer une nouvelle page
        notion_data = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Currency": {
                    "title": [
                        {
                            "text": {
                                "content": data["Currency"]
                            }
                        }
                    ]
                },
                "Quantity": {
                    "number": float(data["Quantity"])
                },
                "UnitValue": {
                    "number": float(data["UnitValue"])
                },
                "TotalValue": {
                    "number": float(data["TotalValue"])
                }
            }
        }
        # Créer une nouvelle page
        response = requests.post(NOTION_API_URL, headers=headers, json=notion_data)
        if response.status_code == 200:
            print(f"Page {data['Currency']} added successfully.")
        else:
            print(f"Failed to add page {data['Currency']}.")

# Fonction pour mettre à jour les données à partir du fichier CSV
def update_wallet_from_csv(csv_file, is_notion_csv=False):
    try:
        with open(csv_file, mode='r') as file:
            # Lire le fichier CSV en utilisant DictReader
            reader = csv.reader(file)
            
            # Sauter la première ligne si le CSV est issu d'Anyquery
            if not is_notion_csv:
                next(reader)  # Cette ligne saute la première ligne (en-tête provenant d'Anyquery)

            # Ajouter les lignes au format Notion
            for row in reader:
                # Vérifier si la ligne est vide ou mal formatée
                if len(row) < 4:
                    print(f"Ignoring invalid line: {row}")
                    continue
                
                # Créer un dictionnaire correspondant aux noms de colonnes attendus
                row_dict = {
                    'Currency': row[0],
                    'Quantity': row[1],
                    'UnitValue': row[2],
                    'TotalValue': row[3]
                }
                
                # Afficher le contenu de chaque ligne pour déboguer
                print("Ligne du CSV traitée :", row_dict)

                # Vérification et conversion des valeurs en float
                try:
                    row_dict['Quantity'] = float(row_dict['Quantity'])
                    row_dict['UnitValue'] = float(row_dict['UnitValue'])
                    row_dict['TotalValue'] = float(row_dict['TotalValue'])
                except ValueError as e:
                    print(f"Error converting values to float for row {row_dict}: {e}")
                    continue  # Ignorer cette ligne et passer à la suivante
                
                # Ajouter ou mettre à jour chaque ligne de CSV dans Notion
                add_or_update_notion_page(row_dict)
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

if __name__ == "__main__":
    # Path to your Wallet.csv file
    csv_file_path = os.path.expanduser('Cryptopricingplugin/Wallet.csv')
    
    # Appeler la fonction avec is_notion_csv=True si c'est le fichier Notion
    update_wallet_from_csv(csv_file_path, is_notion_csv=True)
