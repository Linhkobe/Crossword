import numpy as np
import cv2
import json
import pytesseract
import re
from collections import OrderedDict
import os




crossword_size = 10  # Set to dimension of crossword (standard 15 x 15)

# 1. Loading the Image
img = cv2.imread('Crossword\img\image2.jpg')

# 2. Convert to HSV color space to detect colors
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 3. Define the range for orange color in HSV
orange_lower = np.array([10, 100, 100], dtype="uint8")
orange_upper = np.array([20, 255, 255], dtype="uint8")

# Create a mask for detecting orange areas
orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)

# Convert the original image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (7, 7), 0)

# 4. Use adaptive thresholding to get a binary image
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 2)
# thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


#  Combine the thresholded image with the orange mask to set orange areas to black
combined_mask = cv2.bitwise_or(thresh, orange_mask)

# Invert the combined image
thresh2 = cv2.bitwise_not(combined_mask)

# 5. Finding Contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 1)

max_area = -1

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
        if cv2.contourArea(cnt) > max_area:
            max_area = cv2.contourArea(cnt)
            max_cnt = cnt

# 6.Identifying crossword region
x, y, w, h = cv2.boundingRect(max_cnt)
cross_rect = thresh2[y:y+h, x:x+w]
cross_rect = cv2.resize(cross_rect, (crossword_size * 10, crossword_size * 10))

# 7. Creating Binary Matrix
cross = np.zeros((crossword_size, crossword_size))

for i in range(crossword_size):
    for j in range(crossword_size):
        box = cross_rect[i*10:(i+1)*10, j*10:(j+1)*10]
        if cv2.countNonZero(box) > 50:
            cross[i, j] = 1

# 8. Convert the numpy array to a list of lists
cross_dict = {"matrix binaire": cross.tolist()}

# 9. Save the JSON to a file
# with open('Crossword\crossword_binary_matrix.json', 'w') as json_file:
#     json.dump(cross_dict, json_file, indent=4)

# print(cross)



######################
# Configure the path to the Tesseract executable
os.environ['TESSDATA_PREFIX'] = r'C:\Users\thuyt\AppData\Local\Programs\Tesseract-OCR\tessdata'
text = pytesseract.image_to_string(thresh2, lang='fra')
# Patterns to identify the clues
horizontal_clue_pattern = re.compile(r'\b\d+\.\s')
vertical_clue_pattern = re.compile(r'\b[A-HJ]\.\s')  # Exclude I to avoid confusion with 1

# Using OrderedDict to maintain the order of insertion
definitions = {'Horizontal': OrderedDict(), 'Vertical': {}}
horizontal_clue_count = 1 
# Split text into lines
for line in text.splitlines():
    line = line.strip()
    if not line:
        continue  # Skip empty lines

    # Match horizontal clues
    horizontal_match = horizontal_clue_pattern.match(line)
    if horizontal_match:
        clue_number = int(horizontal_match.group().strip('. '))
        definitions['Horizontal'][clue_number] = line[horizontal_match.end():].split('. ')

    # Match vertical clues
    vertical_match = vertical_clue_pattern.match(line)
    if vertical_match:
        clue_letter = vertical_match.group().strip('. ')
        definitions['Vertical'][f'Column {clue_letter}'] = line[vertical_match.end():].split('. ')

    # Special case for the letter I mistaken as 1
    if line.startswith("1. "):
        # You might need additional checks here to distinguish between actual "1." and "I."
        clue_letter = "I"  # Assuming that "1." at the start of the line should be "I."
        definitions['Vertical'][f'Column {clue_letter}'] = line[2:].split('. ')  # Adjust index if needed

# Now sort the horizontal clues by the clue number
sorted_horizontal_clues = OrderedDict(sorted(definitions['Horizontal'].items()))
definitions['Horizontal'] = {f'Row {k}': v for k, v in sorted_horizontal_clues.items()}

# Print and save the structured data
print(json.dumps(definitions, indent=2, ensure_ascii=False))
with open('definitions.json', 'w', encoding='utf-8') as json_file:
    json.dump(definitions, json_file, indent=2, ensure_ascii=False)

print(f"JSON data saved ")

print(text)

# 10. Display the binary image
cv2.imshow('Binary Image', thresh2)
cv2.waitKey(0)
cv2.destroyAllWindows()
