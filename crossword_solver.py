import openai
import json
from config import OPENAI_API_KEY

#Configuration de l'API OpenAI
openai.api_key = "#################"

def obtenir_reponse(prompt):
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def generer_prompt(grille, indices_horizontaux, indices_verticaux):
    prompt = (
        "Voici une grille de mots croisés avec des indices. "
        "La grille est représentée par des cases vides (null) et des cases noires (1). "
        "Les indices horizontaux et verticaux sont listés ci-dessous. "
        "Remplissez la grille avec les réponses appropriées.\n\n"
        "Grille (cases noires représentées par des 1, cases à remplir par des null):\n" + 
        json.dumps(grille, indent=4) + "\n\n" +
        "Indices Horizontaux:\n" + "\n".join([f"{i+1}. {indice}" for i, indice in enumerate(indices_horizontaux)]) + "\n\n" +
        "Indices Verticaux:\n" + "\n".join([f"{chr(65+i)}. {indice}" for i, indice in enumerate(indices_verticaux)]) + "\n\n" +
        "Réponses:\n"
    )
    return prompt

def integrer_mot(grille, mot, position, orientation):
    ligne, colonne = position
    for lettre in mot:
        if orientation == 'horizontal':
            grille[ligne][colonne] = lettre
            colonne += 1
        elif orientation == 'vertical':
            grille[ligne][colonne] = lettre
            ligne += 1