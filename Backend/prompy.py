import openai
import json
import requests
import os

requests.packages.urllib3.disable_warnings()
session = requests.Session()
session.verify = False
openai.api_requestor._session = session

script_dir = os.path.dirname(__file__)
json_dir_path = os.path.join(script_dir, 'json')

# Load the JSON data
definition_path = os.path.join(json_dir_path, 'definition.json')
with open(definition_path, 'r') as file:
    definitions = json.load(file)

info_words_path = os.path.join(json_dir_path, 'info_words.json')
with open(info_words_path, 'r') as file:
    word_info = json.load(file)

matrix_path = os.path.join(json_dir_path, 'matrix.json')
with open(matrix_path, 'r') as file:
    matrix = json.load(file)['matrix_binaire']

openai.api_key = '####################'

def generate_prompt(definitions, word_info, matrix):
    prompt = "Solve the following crossword puzzle:\n\n"
    
    prompt += "Grid:\n"
    for row in matrix:
        prompt += ''.join(['1' if cell == 1 else '0' for cell in row]) + "\n"
    
    prompt += "\nHorizontal Definitions:\n"
    for key, items in word_info['HORIZONTALEMENT'].items():
        for item in items:
            prompt += f"{key}: {item['definition']} ({item['taille']} letters)\n"
    
    prompt += "\nVertical Definitions:\n"
    for key, items in word_info['VERTICALEMENT'].items():
        for item in items:
            prompt += f"{key}: {item['definition']} ({item['taille']} letters)\n"
    
    return prompt

def solve_crossword(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1500,
        temperature=0.5,
        n=1, 
        stop=None
    )
    return response.choices[0].text.strip()

def fill_grid(solution, word_info, matrix):
    grid = [[' ' if cell == 1 else '#' for cell in row] for row in matrix]
    
    for line in solution.split('\n'):
        parts = line.split(': ')
        if len(parts) == 2:
            key, word = parts
            if key in word_info['HORIZONTALEMENT']:
                items = word_info['HORIZONTALEMENT'][key]
                for item in items:
                    positions = item['mot']
                    for i, pos in enumerate(positions):
                        row = int(pos[1]) - 1
                        col = ord(pos[0]) - ord('A')
                        grid[row][col] = word[i]
            elif key in word_info['VERTICALEMENT']:
                items = word_info['VERTICALEMENT'][key]
                for item in items:
                    positions = item['mot']
                    for i, pos in enumerate(positions):
                        row = int(pos[1]) - 1
                        col = ord(pos[0]) - ord('A')
                        grid[row][col] = word[i]

    return grid

# Generate the prompt
prompt = generate_prompt(definitions, word_info, matrix)
print("Prompt Generated:")
print(prompt)

# Solve the crossword
solution = solve_crossword(prompt)
print("Solution Received:")
print(solution)

# Fill the grid with the solution
filled_grid = fill_grid(solution, word_info, matrix)
print("Filled Grid:")
for row in filled_grid:
    print(''.join(row))
