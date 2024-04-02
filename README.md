# Crossword

## Overview
This branch focuses on processing crossword puzzles from images. It involves two main steps: extracting the crossword grid into a binary matrix and detecting and processing the text for definitions.

### Contributors
- TRINH Thi Thanh Thuy
- HASSAD Zakaria

## File Descriptions

### `detectionDeGrilleCW.py`
- **Purpose**: Analyzes photos to extract a crossword grid and convert it into a binary matrix.
- **Output**: Generates a JSON file named `crossword_binary_matrix.json`.
- **Usage**: Execute the script to produce the JSON file. You can visualize the structure of this binary matrix and check its accuracy using the [JSON Visualizer](https://www.jsonvisual.com/).
  ![image](https://github.com/Linhkobe/Crossword/assets/130557192/4763f722-8472-4727-8e87-ec207a6df7fb)


### `main_definition_ocr.py`
- **Purpose**: Uses OCR API to detect and extract text from the crossword definitions in the images.
- **Output**: Raw text extracted from images.
- **Additional Info**: To use the OCR API, you can easily obtain an API key within minutes from [OCR Space API](https://ocr.space/ocrapi). The API is free for up to 25,000 requests per month.

### `V1_ocr_processing.py` & `V2_ocr_processing.py`
- **Purpose**: Process the text detected by OCR to conform to a JSON format.
- **Output**: 
  - `V1_ocr_processing.py` outputs `definition-v1.json`
  - `V2_ocr_processing.py` outputs `definition-v2.json`
- **Difference**: Both scripts are similar, but they output different versions of the JSON structure, catering to varying data structuring needs.

## How to Use

1. **Extracting the Crossword Grid**:
   - Run `python detectionDeGrilleCW.py`.
   - Check the generated `crossword_binary_matrix.json` using the JSON Visualizer.

2. **Extracting Crossword Definitions**:
   - Obtain an API key from [OCR Space API](https://ocr.space/ocrapi).
   - Run `python main_definition_ocr.py` to extract text from images.
   - Process the extracted text to JSON format using:
     - `python V1_ocr_processing.py` for version 1 JSON format. (`definition-v1.json`)
     - `python V2_ocr_processing.py` for version 2 JSON format. (`definition-v1.json`)

