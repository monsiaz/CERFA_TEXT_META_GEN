
# CERFA Text Generation Script

## Overview

This script is designed to generate relevant content for CERFA document pages to improve their SEO ranking and increase downloads on the platform. It leverages the OpenAI API to generate detailed HTML content and SEO-optimized meta descriptions for each CERFA document.

## Script Logic

1. **API Key Management**:
    - The script reads the OpenAI API key from a file named `api_key.txt`.
    - If the file does not exist or is empty, the script raises an error.

2. **Pricing Configuration**:
    - Pricing information for different OpenAI models (`gpt-4-turbo` and `gpt-4o`) is defined.

3. **Text Generation Function**:
    - `generate_text(prompt, model)`: This function sends a prompt to the OpenAI API and returns the generated text and tokens used.

4. **JSON File Handling**:
    - `append_to_json_file(filepath, entry)`: This function appends new entries to a JSON file.

5. **HTML Structure Generation**:
    - `generate_html_structure(title)`: This function generates different HTML structures to ensure content variety.

6. **Processing CERFA Documents**:
    - `process_cerfa_documents(input_filepath, output_filepath, test_mode)`: This function processes the CERFA documents, generates content using the OpenAI API, and saves the results to an output JSON file.
    - The function limits the processing to 2 entries when in test mode.

7. **Cost Estimation**:
    - The script estimates the total cost based on the number of URLs processed and the pricing of the OpenAI models.

## Usage

1. **Preparation**:
    - Ensure you have an OpenAI API key saved in a file named `api_key.txt`.

2. **Running the Script**:
    - Adjust the `input_filepath` and `output_filepath` variables to point to your input and output JSON files.
    - Run the script in test mode or full mode as needed.

```python
# Example usage
input_filepath = '/path/to/filtered_urls.json'
output_filepath = '/path/to/generated_text_meta.json'
process_cerfa_documents(input_filepath, output_filepath, test_mode=True)
```

## File Descriptions

- `api_key.txt`: Contains the OpenAI API key.
- `filtered_urls.json`: Input file with a list of CERFA document URLs and titles.
- `generated_text_meta.json`: Output file where the generated content and meta descriptions are saved.

## Error Handling

- The script handles errors related to missing API keys, failed API requests, and JSON file operations. Errors are logged to the console for troubleshooting.

## Notes

- Adjust the `max_tokens` and `temperature` parameters in the `generate_text` function as needed.
- Ensure your API key has sufficient quota to handle the number of requests.

## Contributing

- Contributions are welcome. Please fork the repository and submit a pull request.

## License

- This project is licensed under the MIT License.
