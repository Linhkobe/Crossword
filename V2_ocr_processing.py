import json
import re

# Split the text into "HORIZONTALEMENT" and "VERTICALEMENT" sections
def process_ocr_text(ocr_text):
    parts = re.split('(HORIZONTALEMENT|VERTICALEMENT)', ocr_text)
    horizontal_text = parts[2] if 'HORIZONTALEMENT' in parts else ""
    vertical_text = parts[4] if 'VERTICALEMENT' in parts else ""

    # Process the "HORIZONTALEMENT" part
    horizontal_clues = []
    for line in horizontal_text.split('\n'):
        line = line.strip()
        if not line or re.match(r'^\d+\.$', line) or re.match(r'^[A-J]\.$', line, re.I) or re.match(r'^[A-J]$', line, re.I) or re.match(r'^(\d+_$)', line):
            continue  
        line = re.sub(r'^(\d+\.\s*)|([A-J]\.\s*)', '', line, flags=re.I)
        if line:
            horizontal_clues.append(line)


    # Process the "VERTICALEMENT" part
    vertical_clues = []
    for line in vertical_text.split('\n'):
        line = line.strip()
        if not line or line.isalpha() or re.match(r'^[A-Jl]\.$', line):
            continue
        if re.match(r'^[A-Jl]\.', line):
            line = re.sub(r'^[A-Jl]\.\s*', '', line)
        vertical_clues.append(line)

    # Number and split definitions
    def process_clues(clues, is_horizontal=True):
        result_dict = {}
        for i, clue in enumerate(clues, start=1):
            sub_clues = clue.replace("...", ". ").split(". ")
            if len(sub_clues) > 1:
                cleaned_sub_clues = [f"{sub_clue.strip()}." if not sub_clue.strip().endswith(".") else sub_clue.strip() for sub_clue in sub_clues]
                key = f"{i}" if is_horizontal else f"{chr(64+i)}"
                result_dict[key] = cleaned_sub_clues
            else:
                key = f"{i}" if is_horizontal else f"{chr(64+i)}"
                result_dict[key] = sub_clues[0].strip() + ("." if not sub_clues[0].strip().endswith(".") else "")
        return result_dict

    # Combine results and save to JSON
    result = {
        "HORIZONTALEMENT": process_clues(horizontal_clues, is_horizontal=True),
        "VERTICALEMENT": process_clues(vertical_clues, is_horizontal=False)
    }

    json_filepath = 'results-json/definition-v2.json'
    with open(json_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)

    print("ok")

    return result
