import json
from flask import Flask, request, jsonify
import os
import process_definition_image
import process_grid_image
import extract_words
import prompt_engine  # Import the prompt_engine module

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200

@app.route('/process-grid', methods=['POST'])
def process_grid():
    grid_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'grid.jpg')
    try:
        cropped_crossword = process_grid_image.parse_grid(grid_image_path)
        binary_matrix = process_grid_image.convert_to_binary_matrix(cropped_crossword, crossword_size=10)
        
        if not os.path.exists('json'):
            os.makedirs('json')
        
        matrix_path = 'json/matrix.json'
        with open(matrix_path, 'w', encoding='utf-8') as f:
            json.dump({"matrix_binaire": binary_matrix.tolist()}, f, ensure_ascii=False, indent=4)
        
        print(f"JSON result saved to {matrix_path}")

        return jsonify({"matrix_binaire": binary_matrix.tolist()}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/process-definition', methods=['POST'])
def process_definition():
    definition_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'definition.jpg')
    api_key = "K89603096888957"  
    try:
        print(f"Processing definition for image: {definition_image_path}")
        definitions = process_definition_image.process_definition(definition_image_path, api_key)
        
        if not os.path.exists('json'):
            os.makedirs('json')

        with open('json/definition.json', 'w', encoding='utf-8') as f:
            json.dump(definitions, f, ensure_ascii=False, indent=4)
        
        print(f"JSON result saved to json/definition.json")

        # Process words after processing the definition
        process_words()

        return jsonify(definitions), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/process-words', methods=['POST'])
def process_words_endpoint():
    try:
        process_words()
        return jsonify({"message": "Words processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_words():
    try:
        extract_words.process_words()  # Call the function to process words
        print("Words processed successfully and saved to json/info_words.json")

        # Process predictions after processing words
        process_predictions()
    except Exception as e:
        print(f"Error processing words: {str(e)}")

def process_predictions():
    try:
        print("Starting prediction process...")
        prompt_engine.run_prompt_engine()  # Call the function to process predictions
        print("Predictions processed successfully and saved.")
    except Exception as e:
        print(f"Error processing predictions: {str(e)}")

@app.route('/get-french-predictions', methods=['GET'])
def get_french_predictions():
    try:
        with open('json/french_predictions.json', 'r', encoding='utf-8') as f:
            french_predictions = json.load(f)
        return jsonify(french_predictions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
