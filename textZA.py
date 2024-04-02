import pytesseract
from PIL import Image
import json
import re

# Charger l'image
image_path = "Crossword\img\TEST.png"
img = Image.open(image_path)

# Utiliser Tesseract pour extraire le texte de l'image
text = pytesseract.image_to_string(img)

# Expression régulière pour extraire les lignes avec le format attendu
pattern = r'(\d+|[A-Z])\.\s+(.*)'

# Recherche des lignes correspondant au format attendu
matches = re.findall(pattern, text)

# Création d'un dictionnaire pour stocker les données
data = {}

# Parcours des questions et stockage dans le dictionnaire
for match in matches:
    prefix = match[0]
    phrases = match[1].split(". ")
    for i, phrase in enumerate(phrases):
        if len(phrases) > 1:
            data[f"{prefix}.{i+1}"] = phrase.strip()
        else:
            data[prefix] = phrase.strip()

# Écriture des données dans un fichier JSON avec l'encodage UTF-8
output_file = "output.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print("Fichier JSON créé avec succès !")

print(text)