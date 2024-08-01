import os
import json
from openai import OpenAI
import random

# Define the file path for the API key
api_key_filepath = 'api_key.txt'

# Check if the API key file exists
if not os.path.exists(api_key_filepath):
    raise ValueError(f"No API key file found at {api_key_filepath}")

# Load the API key from the file api_key.txt
with open(api_key_filepath, 'r') as api_key_file:
    api_key = api_key_file.readline().strip()  # Read the first line and strip whitespace
    if not api_key:
        raise ValueError("API key file is empty")

print(f"API Key found: {api_key}")

# Configure the OpenAI client
client = OpenAI(api_key=api_key)

def generate_text(prompt):
    try:
        # Create a chat completion with the specified prompt
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Tu es un expert des démarches administratives et des CERFA pour le site https://www.startdoc.fr/. Par ailleurs, tu prendras un soin particulier à avoir des formulations et un style humain (pas un des formulations IA standar)"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,  # Adjust as needed
            temperature=0.6
        )
        text = response.choices[0].message.content
        text = text.replace('\n', '').replace('\\n', '')  # Remove \n and \\n
        text = text.replace('| Startdoc', '')  # Remove "| Startdoc"
        return text
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

def generate_html_structure(title):
    # Define different HTML structures to choose from for variety
    structures = [
        f"<h2>Présentation du {title}</h2><p>[Contenu]</p>"
        f"<h2>Utilisation du {title}</h2><p>[Contenu]</p>"
        f"<h2>Cadre juridique et références</h2><p>[Contenu]</p>"
        f"<h2>Champs à compléter</h2><p>[Contenu]</p>"
        f"<h2>Avantages et inconvénients</h2><p>[Contenu]</p>"
        f"<h2>Démarches administratives</h2><p>[Contenu]</p>"
        f"<h2>Ressources supplémentaires</h2><p>[Contenu]</p>",
        
        f"<h2>Introduction au {title}</h2><p>[Contenu]</p>"
        f"<h2>Applications pratiques du {title}</h2><p>[Contenu]</p>"
        f"<h2>Législation en vigueur</h2><p>[Contenu]</p>"
        f"<h2>Instructions de remplissage</h2><p>[Contenu]</p>"
        f"<h2>Points forts et limitations</h2><p>[Contenu]</p>"
        f"<h2>Procédures administratives</h2><p>[Contenu]</p>"
        f"<h2>Informations complémentaires</h2><p>[Contenu]</p>",
        
        f"<h2>Vue d'ensemble du {title}</h2><p>[Contenu]</p>"
        f"<h2>Contextes d'utilisation du {title}</h2><p>[Contenu]</p>"
        f"<h2>Références légales</h2><p>[Contenu]</p>"
        f"<h2>Instructions détaillées</h2><p>[Contenu]</p>"
        f"<h2>Bénéfices et restrictions</h2><p>[Contenu]</p>"
        f"<h2>Formalités administratives</h2><p>[Contenu]</p>"
        f"<h2>Sources et liens utiles</h2><p>[Contenu]</p>",

        f"<h2>Description générale du {title}</h2><p>[Contenu]</p>"
        f"<h2>Utilisation courante du {title}</h2><p>[Contenu]</p>"
        f"<h2>Base légale et règlements</h2><p>[Contenu]</p>"
        f"<h2>Détails du formulaire</h2><p>[Contenu]</p>"
        f"<h2>Avantages et désavantages</h2><p>[Contenu]</p>"
        f"<h2>Processus administratif</h2><p>[Contenu]</p>"
        f"<h2>Informations additionnelles</h2><p>[Contenu]</p>",

        f"<h2>Aperçu du {title}</h2><p>[Contenu]</p>"
        f"<h2>Fonctionnalités du {title}</h2><p>[Contenu]</p>"
        f"<h2>Contexte juridique</h2><p>[Contenu]</p>"
        f"<h2>Guide de remplissage</h2><p>[Contenu]</p>"
        f"<h2>Avantages et contraintes</h2><p>[Contenu]</p>"
        f"<h2>Procédures à suivre</h2><p>[Contenu]</p>"
        f"<h2>Ressources utiles</h2><p>[Contenu]</p>",

        f"<h2>Introduction détaillée du {title}</h2><p>[Contenu]</p>"
        f"<h2>Utilisations possibles du {title}</h2><p>[Contenu]</p>"
        f"<h2>Références légales et réglementations</h2><p>[Contenu]</p>"
        f"<h2>Instructions spécifiques</h2><p>[Contenu]</p>"
        f"<h2>Points positifs et négatifs</h2><p>[Contenu]</p>"
        f"<h2>Démarches à suivre</h2><p>[Contenu]</p>"
        f"<h2>Informations additionnelles et sources</h2><p>[Contenu]</p>",

        f"<h2>Présentation du formulaire {title}</h2><p>[Contenu]</p>"
        f"<h2>Usage et application du {title}</h2><p>[Contenu]</p>"
        f"<h2>Réglementation et législation</h2><p>[Contenu]</p>"
        f"<h2>Détails et instructions</h2><p>[Contenu]</p>"
        f"<h2>Avantages et inconvénients</h2><p>[Contenu]</p>"
        f"<h2>Procédure administrative</h2><p>[Contenu]</p>"
        f"<h2>Informations et liens supplémentaires</h2><p>[Contenu]</p>",

        f"<h2>Vue d'ensemble du formulaire {title}</h2><p>[Contenu]</p>"
        f"<h2>Contextes d'application du {title}</h2><p>[Contenu]</p>"
        f"<h2>Références légales et réglementaires</h2><p>[Contenu]</p>"
        f"<h2>Guide détaillé</h2><p>[Contenu]</p>"
        f"<h2>Points forts et faibles</h2><p>[Contenu]</p>"
        f"<h2>Processus et démarches</h2><p>[Contenu]</p>"
        f"<h2>Sources et informations complémentaires</h2><p>[Contenu]</p>"
    ]
    return random.choice(structures)

def process_cerfa_documents(input_filepath, output_filepath, test_mode=False):
    print("Loading data from file...")
    with open(input_filepath, 'r') as file:
        data = json.load(file)

    # Load or create the output JSON file
    if os.path.exists(output_filepath):
        with open(output_filepath, 'r') as file:
            processed_data = json.load(file)
    else:
        processed_data = []

    # Create a set of already processed URLs
    processed_urls = {entry['url'] for entry in processed_data}

    # Filter unprocessed URLs and sort them
    urls_to_process = [entry for entry in data if entry['url'] not in processed_urls]
    urls_to_process = sorted(urls_to_process, key=lambda x: x['url'])

    # Limit to 2 entries in test mode
    if test_mode:
        urls_to_process = urls_to_process[:2]

    print(f"Processing {len(urls_to_process)} entries...")

    for entry in urls_to_process:
        url = entry['url']
        title = entry['title']
        
        # Generate the explanatory text of 1500 words
        html_structure = generate_html_structure(title)
        prompt = (
            f"Écris un texte de 1500 mots en HTML (sans <!DOCTYPE ou head, tu commences directement par un H2) pour expliquer et décrire le CERFA intitulé '{title}'. "
            "Tu adaptes les H2 et la structure en fonction du CERFA. "
            "Écris des paragraphes complets en utilisant des balises HTML propres (par exemple, <p> pour les paragraphes, <ul><li> pour les listes à puces, et <strong> pour la mise en gras). "
            "Tu n'injecteras que du html basique donc pas de \\n ou \\n\\n ou de **. "
            "Voici un modèle générique à adapter : "
            f"{html_structure}"
        )
        print(f"Generating text for {title}...")
        generated_text = generate_text(prompt)
        if not generated_text:
            print(f"Failed to generate text for {title}. Skipping.")
            continue
        
        # Generate the SEO optimized meta description
        prompt_meta = f"Génère une méta description optimisée pour le SEO (moins de 130 caractères) pour le CERFA intitulé '{title}'."
        print(f"Generating meta description for {title}...")
        meta_description = generate_text(prompt_meta)
        if not meta_description:
            print(f"Failed to generate meta description for {title}. Skipping.")
            continue
        
        # Add results to the list
        result_entry = {
            'url': url,
            'title': title,
            'meta_description': meta_description,
            'generated_text': generated_text
        }
        print(f"Generated text and meta description for {title}.")

        # Write results to the new JSON file immediately
        if append_to_json_file(output_filepath, result_entry):
            print(f"Appended result for {title} to {output_filepath}")
        else:
            print(f"Failed to append result for {title}. Stopping the script.")
            break

    print("Process completed.")

# Usage of the script
input_filepath = '/Users/simonazoulay/CERFA_TEXT_GEN/filtered_urls.json'
output_filepath = '/Users/simonazoulay/CERFA_TEXT_GEN/generated_text_meta.json'
process_cerfa_documents(input_filepath, output_filepath, test_mode=True)
