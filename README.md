
# CERFA Document Processing

This project is designed to fetch, filter, and process CERFA documents from a given sitemap. It consists of two main scripts. The first script retrieves URLs from a sitemap, filters them based on certain criteria, and saves the filtered URLs into a JSON file. The second script uses the filtered URLs to generate detailed descriptions and meta descriptions for the CERFA documents using the OpenAI API.

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Scripts Breakdown](#scripts-breakdown)
    - [fetch_sitemap.py](#fetch_sitemappy)
    - [process_cerfa_documents.py](#process_cerfa_documentspy)
5. [Results](#results)
6. [Configuration](#configuration)
7. [Contributing](#contributing)
8. [License](#license)

## Overview
This project automates the process of generating explanatory content for CERFA documents. It scrapes URLs from a given sitemap, filters them, and generates human-readable content and SEO meta descriptions using OpenAI's GPT-4 model.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/cerfa-documents-processing.git
    ```
2. Navigate to the project directory:
    ```sh
    cd cerfa-documents-processing
    ```
3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. **Fetch and filter URLs:**
    - Run the `fetch_sitemap.py` script to fetch URLs from the sitemap and filter them based on specific criteria.
    - The filtered URLs will be saved in `filtered_urls.json`.
    ```sh
    python fetch_sitemap.py
    ```

2. **Process CERFA documents:**
    - Run the `process_cerfa_documents.py` script to generate descriptive content and meta descriptions for the filtered CERFA documents.
    - The generated content will be saved in `generated_text_meta.json`.
    ```sh
    python process_cerfa_documents.py
    ```

## Scripts Breakdown

### fetch_sitemap.py

#### Functions:

1. `fetch_sitemap(url)`
    - Fetches the sitemap XML from the given URL.
    - **Parameters:**
        - `url`: URL of the sitemap.
    - **Returns:** Sitemap XML as a string.

2. `parse_sitemap(sitemap_xml)`
    - Parses the sitemap XML to extract URLs.
    - **Parameters:**
        - `sitemap_xml`: XML string of the sitemap.
    - **Returns:** List of URLs.

3. `filter_cerfa_urls(urls)`
    - Filters URLs containing the keyword 'cerfa'.
    - **Parameters:**
        - `urls`: List of URLs.
    - **Returns:** List of filtered URLs.

4. `fetch_page_content(url)`
    - Fetches the HTML content of a given URL.
    - **Parameters:**
        - `url`: URL of the page.
    - **Returns:** HTML content as a string.

5. `filter_urls(urls)`
    - Further filters URLs based on the content of the pages.
    - **Parameters:**
        - `urls`: List of URLs.
    - **Returns:** List of dictionaries with filtered URL information.

6. `save_to_json(data, filename)`
    - Saves data to a JSON file.
    - **Parameters:**
        - `data`: Data to save.
        - `filename`: Name of the JSON file.

### process_cerfa_documents.py

#### Functions:

1. `generate_text(prompt)`
    - Generates text using the OpenAI API based on the provided prompt.
    - **Parameters:**
        - `prompt`: Prompt for the text generation.
    - **Returns:** Generated text as a string.

2. `append_to_json_file(filepath, entry)`
    - Appends an entry to a JSON file.
    - **Parameters:**
        - `filepath`: Path to the JSON file.
        - `entry`: Entry to append.

3. `process_cerfa_documents(input_filepath, output_filepath, test_mode)`
    - Processes CERFA documents and generates content and meta descriptions.
    - **Parameters:**
        - `input_filepath`: Path to the input JSON file with filtered URLs.
        - `output_filepath`: Path to the output JSON file for generated content.
        - `test_mode`: Boolean flag for test mode.

## Results
The generated JSON file `generated_text_meta.json` contains the URL, title, meta description, and generated text for each CERFA document. Example entry:
```json
{
    "url": "https://www.startdoc.fr/documents/1479-cerfa-10431-05-demande-de-capital-deces/",
    "title": "CERFA 10431-05 : Demande de capital décés | Startdoc",
    "meta_description": "Demandez votre capital décès facilement avec le CERFA 10431-05 sur Startdoc. Téléchargement rapide et assistance complète.",
    "generated_text": "<h2>Présentation du CERFA 10431-05 : Demande de capital décès</h2><p>Le formulaire CERFA 10431-05 est un document administratif français utilisé pour faire une demande de capital décès...</p>"
}
```

## Configuration
- Ensure you have your OpenAI API key stored in `api_key.txt`.
- Modify the `input_filepath` and `output_filepath` in `process_cerfa_documents.py` as needed.
- You can adjust the prompts in `generate_text` function to customize the generated content.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
