import cv2
import numpy as np
import requests
import io
import json
import re
import os

def filter_and_store_lines(ocr_text):
    lines = ocr_text.split('\n')
    valid_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\d+[-.,_]?$|^[A-Za-z][-.,_]?$', line):
            continue
        valid_lines.append(line)
    
    return valid_lines

def remove_keys_from_lines(valid_lines):
    filtered_lines = []
    for line in valid_lines:
        line_without_key = re.sub(r'^\d+[-.,_]?\s*', '', line)
        line_without_key = re.sub(r'^[A-Za-z][-.,_]\s*', '', line_without_key)
        filtered_lines.append(line_without_key)
        print(f"Filtered Line without Key: {line_without_key}")
    return filtered_lines

def process_filtered_lines(filtered_lines):
    horiz_definitions = {}
    vert_definitions = {}

    current_section = None
    current_lines = []

    vert_key_index = 0
    vert_keys = 'ABCDEFGHIJ'

    horiz_key_index = 1

    for line in filtered_lines:
        if "HORIZONTALEMENT" in line:
            current_section = "horizontal"
            current_lines = []
            continue
        elif "VERTICALEMENT" in line:
            current_section = "vertical"
            current_lines = []
            continue

        if current_section == "horizontal":
            horiz_definitions[str(horiz_key_index)] = line.strip()
            horiz_key_index += 1
        elif current_section == "vertical":
            if vert_key_index < len(vert_keys):
                vert_definitions[vert_keys[vert_key_index]] = line.strip()
                vert_key_index += 1

    return {'HORIZONTALEMENT': horiz_definitions, 'VERTICALEMENT': vert_definitions}

def process_definition(image_path, api_key):
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    roi = img

    roi_resized = cv2.resize(roi, (width // 2, height // 2))

    _, compressedimage = cv2.imencode(".jpg", roi_resized, [cv2.IMWRITE_JPEG_QUALITY, 80])
    file_bytes = io.BytesIO(compressedimage)

    if file_bytes.getbuffer().nbytes <= 1024 * 1024:
        url_api = "https://api.ocr.space/parse/image"
        files = {"file": ("definition.jpg", file_bytes, "image/jpeg")}
        result = requests.post(url_api,
                        files=files,
                        data={"apikey": api_key,
                              "language": "fre"})

        result = result.content.decode()
        result = json.loads(result)

        if 'ParsedResults' in result:
            parsed_results = result['ParsedResults'][0]
            ocr_text = parsed_results['ParsedText']
            print("OCR Text:", ocr_text)

            valid_lines = filter_and_store_lines(ocr_text)
            for line in valid_lines:
                print(f"Filtered Line: {line}")
            
            filtered_lines = remove_keys_from_lines(valid_lines)
            json_result = process_filtered_lines(filtered_lines)
            print(json_result)
            return json_result
        else:
            raise Exception("No results returned or an error occurred.")
    else:
        raise ValueError("Image size exceeds limit of 1MB.")

if __name__ == "__main__":
    if not os.path.exists('json'):
        os.makedirs('json')

    image_path = "uploads/definition.jpg"
    api_key = "K89603096888957"
    definitions = process_definition(image_path, api_key)
    print(definitions)

    with open('json/definition.json', 'w', encoding='utf-8') as f:
        json.dump(definitions, f, ensure_ascii=False, indent=4)
    print(f"JSON result saved to json/definition.json")
