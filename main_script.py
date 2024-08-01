import os
import json
from openai import OpenAI

# Définir le chemin du fichier de clé API
api_key_filepath = 'api_key.txt'

# Vérifier l'existence du fichier de clé API
if not os.path.exists(api_key_filepath):
    raise ValueError(f"No API key file found at {api_key_filepath}")

# Charger la clé API à partir du fichier api_key.txt
with open(api_key_filepath, 'r') as api_key_file:
    api_key = api_key_file.readline().strip()  # Lire la première ligne et supprimer les espaces blancs
    if not api_key:
        raise ValueError("API key file is empty")

print(f"API Key found: {api_key}")

# Configurer le client OpenAI
client = OpenAI(api_key=api_key)

def generate_text(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Tu es un expert des démarches administratives et des CERFA pour le site https://www.startdoc.fr/. Par ailleurs, tu prendras un soin particulier à avoir des formulations et un style humain (pas un des formulations IA standar)"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,  # Ajustez en fonction de vos besoins
            temperature=0.2
        )
        return response.choices[0].message.content.replace('\n', '').replace('\\n', '')
    except Exception as e:
        print(f"Error generating text: {e}")
        return ""

def append_to_json_file(filepath, entry):
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r+') as file:
                data = json.load(file)
                data.append(entry)
                file.seek(0)
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            with open(filepath, 'w') as file:
                json.dump([entry], file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
        return False

def process_cerfa_documents(input_filepath, output_filepath, test_mode=False):
    print("Loading data from file...")
    with open(input_filepath, 'r') as file:
        data = json.load(file)

    # Charger ou créer le fichier JSON de sortie
    if os.path.exists(output_filepath):
        with open(output_filepath, 'r') as file:
            processed_data = json.load(file)
    else:
        processed_data = []

    # Créer un ensemble d'URLs déjà traitées
    processed_urls = {entry['url'] for entry in processed_data}

    # Filtrer les URLs non traitées et les trier
    urls_to_process = [entry for entry in data if entry['url'] not in processed_urls]
    urls_to_process = sorted(urls_to_process, key=lambda x: x['url'])

    # Limiter à 2 entrées en mode test
    if test_mode:
        urls_to_process = urls_to_process[:2]

    print(f"Processing {len(urls_to_process)} entries...")

    for entry in urls_to_process:
        url = entry['url']
        title = entry['title']
        
        # Générer le texte explicatif de 1500 mots
        prompt = (
            f"Écris un texte de 1500 mots en HTML (sans <!DOCTYPE ou head, tu commences directement par un H2) pour expliquer et décrire le CERFA intitulé '{title}'. "
            "Tu adaptes les H2 et la structure en fonction du CERFA. "
            "Écris des paragraphes complets en utilisant des balises HTML propres (par exemple, <p> pour les paragraphes, <ul><li> pour les listes à puces, et <strong> pour la mise en gras). "
            "Tu n'injecteras que du html basique donc pas de \\n ou \\n\\n ou de **. "
            "Voici un modèle générique à adapter : "
            "<h2>Présentation du CERFA</h2><p>[Contenu]</p>"
            "<h2>Description des cas d’usage</h2><p>[Contenu]</p>"
            "<h2>Textes de lois et références</h2><p>[Contenu]</p>"
            "<h2>Les champs à remplir dans le CERFA</h2><p>[Contenu]</p>"
            "<h2>[Rajouter un H2 pertinent]</h2><p>[Contenu]</p>"
            "<h2>[Rajouter un H2 pertinent]</h2><p>[Contenu]</p>"
            "<h2>Table de synthèse</h2><p>[Contenu]</p>"
        )
        print(f"Generating text for {title}...")
        generated_text = generate_text(prompt)
        if not generated_text:
            print(f"Failed to generate text for {title}. Skipping.")
            continue
        
        # Générer la méta description optimisée pour le SEO
        prompt_meta = f"Génère une méta description optimisée pour le SEO (moins de 130 caractères) pour le CERFA intitulé '{title}'."
        print(f"Generating meta description for {title}...")
        meta_description = generate_text(prompt_meta)
        if not meta_description:
            print(f"Failed to generate meta description for {title}. Skipping.")
            continue
        
        # Ajouter les résultats à la liste
        result_entry = {
            'url': url,
            'title': title,
            'meta_description': meta_description,
            'generated_text': generated_text
        }
        print(f"Generated text and meta description for {title}.")

        # Écrire les résultats dans le nouveau fichier JSON immédiatement
        if append_to_json_file(output_filepath, result_entry):
            print(f"Appended result for {title} to {output_filepath}")
        else:
            print(f"Failed to append result for {title}. Stopping the script.")
            break

    print("Process completed.")

# Utilisation du script
input_filepath = '/Users/simonazoulay/CERFA_TEXT_GEN/filtered_urls.json'
output_filepath = '/Users/simonazoulay/CERFA_TEXT_GEN/generated_text_meta.json'
process_cerfa_documents(input_filepath, output_filepath, test_mode=True)
