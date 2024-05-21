import json

with open('json/matrix.json', 'r', encoding='utf-8') as file:
    matrix_data = json.load(file)

with open('json/definition.json', 'r', encoding='utf-8') as file:
    definitions_data = json.load(file)

def is_start_of_word(matrix, i, j, direction):
    if direction == "horizontal":
        return (j == 0 or matrix[i][j - 1] == 0) and (j < len(matrix[i]) - 1 and matrix[i][j + 1] == 1)
    elif direction == "vertical":
        return (i == 0 or matrix[i - 1][j] == 0) and (i < len(matrix) - 1 and matrix[i + 1][j] == 1)

def is_end_of_word(matrix, i, j, direction):
    if direction == "horizontal":
        return (j == len(matrix[i]) - 1 or matrix[i][j + 1] == 0)
    elif direction == "vertical":
        return (i == len(matrix) - 1 or matrix[i + 1][j] == 0)

def extract_words(matrix):
    words_horizontal = {}
    words_vertical = {}
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    for i in range(num_rows):
        j = 0
        while j < num_cols:
            if matrix[i][j] == 1 and is_start_of_word(matrix, i, j, "horizontal"):
                start_j = j
                while j < num_cols and matrix[i][j] == 1:
                    j += 1
                end_j = j - 1
                words_horizontal.setdefault(i + 1, []).append([(i + 1, k + 1) for k in range(start_j, end_j + 1)])
            j += 1

    for j in range(num_cols):
        i = 0
        while i < num_rows:
            if matrix[i][j] == 1 and is_start_of_word(matrix, i, j, "vertical"):
                start_i = i
                while i < num_rows and matrix[i][j] == 1:
                    i += 1
                end_i = i - 1
                words_vertical.setdefault(chr(65 + j), []).append([(k + 1, j + 1) for k in range(start_i, end_i + 1)])
            i += 1

    return words_horizontal, words_vertical

def split_definitions(definitions, words):
    split_defs = {}
    for key, value in definitions.items():
        word_count = len(words.get(key, []))
        parts = [part.strip() for part in value.split('. ') if part.strip()]

        if word_count > 1 and len(parts) > 1:
            split_defs[key] = parts[:word_count]
        else:
            split_defs[key] = parts
        if key in words:
            while len(split_defs[key]) < word_count:
                split_defs[key].append('')
    return split_defs

def create_result_json(matrix, definitions):
    result = {"HORIZONTALEMENT": {}, "VERTICALEMENT": {}}
    matrix = matrix["matrix_binaire"]

    words_horizontal, words_vertical = extract_words(matrix)
    
    definitions["HORIZONTALEMENT"] = split_definitions(definitions["HORIZONTALEMENT"], words_horizontal)
    definitions["VERTICALEMENT"] = split_definitions(definitions["VERTICALEMENT"], words_vertical)

    for row, words in words_horizontal.items():
        for idx, word in enumerate(words):
            definition_key = str(row)
            if definition_key in definitions["HORIZONTALEMENT"] and idx < len(definitions["HORIZONTALEMENT"][definition_key]):
                result["HORIZONTALEMENT"].setdefault(definition_key, []).append({
                    "mot": ["{}{}".format(chr(64 + pos[1]), pos[0]) for pos in word],
                    "taille": len(word),
                    "definition": definitions["HORIZONTALEMENT"][definition_key][idx]
                })

    for col, words in words_vertical.items():
        for idx, word in enumerate(words):
            definition_key = col
            if definition_key in definitions["VERTICALEMENT"] and idx < len(definitions["VERTICALEMENT"][definition_key]):
                result["VERTICALEMENT"].setdefault(definition_key, []).append({
                    "mot": ["{}{}".format(chr(64 + pos[1]), pos[0]) for pos in word],
                    "taille": len(word),
                    "definition": definitions["VERTICALEMENT"][definition_key][idx]
                })

    return result

result_json = create_result_json(matrix_data, definitions_data)

with open('json/info_words.json', 'w', encoding='utf-8') as file:
    json.dump(result_json, file, ensure_ascii=False, indent=4)

print("finished : json/info_words.json")
