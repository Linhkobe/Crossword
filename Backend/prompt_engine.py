def run_prompt_engine():
    import openai
    import json
    import os
    from googletrans import Translator
    import re

    # Define paths
    script_dir = os.path.dirname(__file__)
    json_dir_path = os.path.join(script_dir, 'json')

    # Load the JSON data
    definition_path = os.path.join(json_dir_path, 'definition.json')
    with open(definition_path, 'r', encoding='utf-8') as file:
        definitions = json.load(file)

    info_words_path = os.path.join(json_dir_path, 'info_words.json')
    with open(info_words_path, 'r', encoding='utf-8') as file:
        word_info = json.load(file)

    matrix_path = os.path.join(json_dir_path, 'matrix.json')
    with open(matrix_path, 'r', encoding='utf-8') as file:
        matrix = json.load(file)['matrix_binaire']

    # Initialize the Google Translator
    translator = Translator()

    # Set the OpenAI API key
    openai.api_key = 'YOUR_API_KEY'

    # Function to translate definitions
    def translate_definitions(definitions):
        translated_definitions = {}
        for key, items in definitions.items():
            translated_definitions[key] = []
            for item in items:
                translated_definition = translator.translate(item['definition'], src='fr', dest='en').text
                translated_item = {
                    "mot": item["mot"],
                    "taille": item["taille"],
                    "definition": translated_definition
                }
                translated_definitions[key].append(translated_item)
        return translated_definitions

    # Translate horizontal and vertical definitions
    horizontal_definitions = translate_definitions(word_info['HORIZONTALEMENT'])
    vertical_definitions = translate_definitions(word_info['VERTICALEMENT'])

    # Format the output
    output = "Solve the crossword puzzle given the following definitions:\n"
    output += "Please return only the predicted words for each definition, i mean just all the words for HORIZONTAL and VERTICAL, no more than that please\n"
    output += "HORIZONTAL DEFINITIONS:\n"
    for row, items in horizontal_definitions.items():
        if len(items) == 1:
            output += f"\"{row}\" : Predict word with definition as \"{items[0]['definition']}\"\n"
        else:
            for idx, item in enumerate(items, start=1):
                output += f"\"{row}.{idx}\" : Predict word with definition as \"{item['definition']}\"\n"

    output += "\nVERTICAL DEFINITIONS:\n"
    for col, items in vertical_definitions.items():
        if len(items) == 1:
            output += f"\"{col}\" : Predict word with definition as \"{items[0]['definition']}\"\n"
        else:
            for idx, item in enumerate(items, start=1):
                output += f"\"{col}.{idx}\" : Predict word with definition as \"{item['definition']}\"\n"

    # Print the formatted output
    print(output)


    def get_predictions(prompt):
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1500,
            temperature=0.5,
            n=1,
            stop=None
        )

        return response.choices[0].message['content']

    prompt = output + "\nPlease provide the predicted word for each definition.\n"

    predictions = get_predictions(prompt)
    print(prompt)
    print(predictions)
    # print(type(predictions))

    # Define the function to parse the predictions text
    def parse_predictions_text(predictions_text):
        predictions_dict = {
            "HORIZONTAL": {},
            "VERTICAL": {}
        }

        # Split the text into lines
        lines = predictions_text.split('\n')
        section = None

        # Regex to match the pattern
        horizontal_pattern = re.compile(r'^(\d+(\.\d+)?)\.? (.+)$')
        vertical_pattern = re.compile(r'^([A-J](\.\d+)?)\.? (.+)$')

        for line in lines:
            line = line.strip()
            if line.startswith("HORIZONTAL:"):
                section = "HORIZONTAL"
            elif line.startswith("VERTICAL:"):
                section = "VERTICAL"
            elif section == "HORIZONTAL":
                match = horizontal_pattern.match(line)
                if match:
                    key = match.group(1)
                    value = match.group(3)
                    predictions_dict[section][key] = value
            elif section == "VERTICAL":
                match = vertical_pattern.match(line)
                if match:
                    key = match.group(1)
                    value = match.group(3)
                    predictions_dict[section][key] = value

        return predictions_dict

    # Parse the predictions
    parsed_predictions = parse_predictions_text(predictions)

    # Define the path to save the JSON file
    english_predictions_path = os.path.join(json_dir_path, 'english_predictions.json')

    # Save the parsed predictions to a JSON file
    with open(english_predictions_path, 'w', encoding='utf-8') as file:
        json.dump(parsed_predictions, file, ensure_ascii=False, indent=4)

    print(f"English predictions saved to {english_predictions_path}")

    print("#############################\n")
    print("Deuxième prompt\n")

    # Combine the predictions with the info_words data
    def combine_predictions_with_info(predictions, info_words):
        combined_info = {"HORIZONTAL": {}, "VERTICAL": {}}

        # Combine horizontal words
        for key, items in info_words["HORIZONTALEMENT"].items():
            if len(items) == 1:
                item = items[0]
                combined_info["HORIZONTAL"][key] = {
                    "prediction": predictions["HORIZONTAL"].get(key, ""),
                    "mot": item["mot"],
                    "taille": item["taille"],
                    # "definition": item["definition"]
                    "definition": translator.translate(item["definition"], src='fr', dest='en').text
                }
            else:
                for idx, item in enumerate(items, start=1):
                    sub_key = f"{key}.{idx}"
                    combined_info["HORIZONTAL"][sub_key] = {
                        "prediction": predictions["HORIZONTAL"].get(sub_key, ""),
                        "mot": item["mot"],
                        "taille": item["taille"],
                        "definition": translator.translate(item["definition"], src='fr', dest='en').text
                    }

        # Combine vertical words
        for key, items in info_words["VERTICALEMENT"].items():
            if len(items) == 1:
                item = items[0]
                combined_info["VERTICAL"][key] = {
                    "prediction": predictions["VERTICAL"].get(key, ""),
                    "mot": item["mot"],
                    "taille": item["taille"],
                    # "definition": item["definition"]
                    "definition": translator.translate(item["definition"], src='fr', dest='en').text
                }
            else:
                for idx, item in enumerate(items, start=1):
                    sub_key = f"{key}.{idx}"
                    combined_info["VERTICAL"][sub_key] = {
                        "prediction": predictions["VERTICAL"].get(sub_key, ""),
                        "mot": item["mot"],
                        "taille": item["taille"],
                        # "definition": item["definition"]
                        "definition": translator.translate(item["definition"], src='fr', dest='en').text
                    }

        return combined_info

    combined_info = combine_predictions_with_info(parsed_predictions, word_info)

    # Create the second_prompt
    second_prompt = "Solve the crossword puzzle given the following clues and instructions:\n"
    second_prompt += "1) Please return only the predicted words in French for each suggestion horizontally and vertically, I mean just all the words for HORIZONTAL and VERTICAL, no more than that.\n"
    second_prompt += "2) You start with the first word in the first row of the crossword grid, pay attention that some words in rows/columns use common cells meaning that they share the same letter, take this point into account to predict the words in French.\n\n"
    second_prompt += "3) You must predict a word in French that has close meaning with the given english word, it must have the exact number of letters indicated for each suggestion, it also uses the cells of the crossword grid as follows:\n\n"
    second_prompt += "4) Analyze the cells of the crossword grid that each word uses and predict the word in French that fits the definition.\n\n"
    second_prompt += "5) Analyze the semantic of the suggestion/clue, see if you're asked to find a verb, noun, adjective, or french slang, etc.\n\n"

    # Format horizontal words
    second_prompt += "\"HORIZONTAL\":\n"
    for key, item in combined_info["HORIZONTAL"].items():
        cells = ', '.join(item["mot"])
        second_prompt += f"    \"{key}\": (predict this word in French that has close meaning with {item['prediction']}, this word must have {item['taille']} letters and it uses cells {cells} of the crossword grid\n"
        second_prompt += f"     with definition as \"{item['definition']}\")\n"

    # Format vertical words
    second_prompt += "\n\"VERTICAL\":\n"
    for key, item in combined_info["VERTICAL"].items():
        cells = ', '.join(item["mot"])
        second_prompt += f"    \"{key}\": (predict this word in French that has close meaning with {item['prediction']}, this word must have {item['taille']} letters and it uses cells {cells} of the crossword grid\n"
        second_prompt += f"     with definition as \"{item['definition']}\")\n"

    # Print the second_prompt
    print(second_prompt)

    french_predictions = get_predictions(second_prompt)
    print("#############################\n")
    print("French Predictions\n")
    print(french_predictions)

    def parse_french_predictions_text(predictions):
        # Initialize the main dictionary structure
        parsed_predictions = {"HORIZONTAL": {}, "VERTICAL": {}}
        current_section = None

        # Split the predictions into lines for processing
        lines = predictions.split('\n')

        for line in lines:
            # Check if the line indicates a section
            if "HORIZONTAL" in line:
                current_section = "HORIZONTAL"
            elif "VERTICAL" in line:
                current_section = "VERTICAL"
            elif current_section and line.strip():  # Ensure the line is not empty and a section is selected
                # Parse the prediction line and add it to the correct section
                key, value = line.split(')')[0], ')'.join(line.split(')')[1:]).strip()
                parsed_predictions[current_section][key] = value

        return parsed_predictions

    parsed_french_predictions = parse_french_predictions_text(french_predictions)

    # Define the path to save the JSON file
    french_predictions_path = os.path.join(json_dir_path, 'french_predictions.json')

    # Save the parsed predictions to a JSON file
    with open(french_predictions_path, 'w', encoding='utf-8') as file:
        json.dump(parsed_french_predictions, file, ensure_ascii=False, indent=4)

    print(f"French predictions saved to {french_predictions_path}")

# Ensure the run_prompt_engine function is defined
if __name__ == "__main__":
    run_prompt_engine()
