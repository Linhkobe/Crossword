import pytesseract
from PIL import Image
import json
import re

def fix_common_ocr_errors(text):
    # Replace the '|' character with 'I'
    text = text.replace('|', 'I')
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Check and replace '4' with '1' in specific conditions
    for i, line in enumerate(lines):
        # Apply the replacement rule only to lines where it's likely to be a mistake
        # For example, you might want to only apply this to the first occurrence
        # or based on additional conditions
        if i == 0 and line.startswith('4'):  # Example condition for the first line
            lines[i] = '1' + line[1:]
        elif '4.' in line:  # Example of avoiding changing '4' to '1' in numbered lists
            # You might want to refine this condition based on your specific needs
            pass  # No action for now, but you can add specific logic here
    
    # Join the lines back into a single text string
    text = '\n'.join(lines)
    
    return text


# Load the uploaded image
image_path = "Crossword\img\image2.jpg"
img = Image.open(image_path)

# Use Tesseract to extract text from the image
text = pytesseract.image_to_string(img)

# Apply the common OCR error corrections to the extracted text
text = fix_common_ocr_errors(text)

# Regular expression pattern to extract lines with the expected format
pattern = r'(\d+|[A-Z])\.\s+(.*)'

# Search for lines matching the expected format
matches = re.findall(pattern, text)

# Create a dictionary to store the data
data = {}

# Iterate over the matches and store them in the dictionary
# Each match contains a prefix and the associated phrase(s)
for match in matches:
    prefix = match[0]  # This is the line number or the letter
    phrases = match[1].split(". ")  # Split if there are multiple phrases
    # Store each phrase under the correct prefix, adding a suffix if multiple phrases exist
    for i, phrase in enumerate(phrases):
        if len(phrases) > 1:
            data[f"{prefix}.{i+1}"] = phrase.strip()
        else:
            data[prefix] = phrase.strip()

# Write the data to a JSON file with UTF-8 encoding
output_file = "outputTZ.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(text)
print("JSON file created successfully!")
