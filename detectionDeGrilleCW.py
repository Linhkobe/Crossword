import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
import operator

def distance_between(p1, p2):
    """Returns the scalar distance between two points"""
    a = p2[0] - p1[0]
    b = p2[1] - p1[1]
    return np.sqrt((a ** 2) + (b ** 2))
# Fonction pour prÃ©traiter une image
def pre_process_image(img, skip_dilate=False, flag=0):
    """Uses blurring, adaptive thresholding, and dilation to expose the main features of an image."""

    proc = cv2.GaussianBlur(img.copy(), (9, 9), 0)
    proc = cv2.adaptiveThreshold(proc, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    proc = cv2.bitwise_not(proc, proc)

    if not skip_dilate:
        kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
        proc = cv2.dilate(proc, kernel)

    # show_image(proc, 'Pre-processed image with binary threshold for contour detection', flag)
    return proc

# Fonction pour trouver les coins d'un plus grand polygone dans une image
def find_corners_of_largest_polygon(img):
    """Finds the 4 extreme corners of the largest contour in the image."""
    contours, h = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    polygon = contours[0]

    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))

    return [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]

def crop_and_warp(img, crop_rect, flag=0):
    """Crops and warps a rectangular section from an image into a square of similar size."""

    top_left, top_right, bottom_right, bottom_left = crop_rect[0], crop_rect[1], crop_rect[2], crop_rect[3]

    src = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')

    side = max([
        distance_between(bottom_right, top_right),
        distance_between(top_left, bottom_left),
        distance_between(bottom_right, bottom_left),
        distance_between(top_left, top_right)
        ])
    
    dst = np.array([[0, 0], [side - 1, 0], [side - 1, side - 1], [0, side - 1]], dtype='float32')

    m = cv2.getPerspectiveTransform(src, dst)

    warp = cv2.warpPerspective(img, m, (int(side), int(side)))
    # show_image(warp, 'extracted and warped CrossWord from the above image', flag)
    
    return warp

# Fonction pour analyser la grille CrossWord
def parse_grid(path, flag=0):
    original = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    
    if original is None:  # Check if the image was loaded successfully
        raise FileNotFoundError(f"Unable to load image at path: {path}")

    rgb_img = cv2.cvtColor(original.copy(), cv2.COLOR_BGR2RGB)
    # show_image(original, 'Original image', flag)

    processed = pre_process_image(original, flag=flag)
    corners = find_corners_of_largest_polygon(processed)
    if not corners:  # Check if corners were found
        raise ValueError("No corners were found in the image.")

    # Draw lines on the RGB image for visualization
    cv2.line(rgb_img, tuple(corners[0]), tuple(corners[1]), (255, 0, 0), 3)
    cv2.line(rgb_img, tuple(corners[1]), tuple(corners[2]), (255, 0, 0), 3)
    cv2.line(rgb_img, tuple(corners[2]), tuple(corners[3]), (255, 0, 0), 3)
    cv2.line(rgb_img, tuple(corners[3]), tuple(corners[0]), (255, 0, 0), 3)
    # show_image(rgb_img, 'CrossWord to extract', flag)
    
    cropped = crop_and_warp(original, corners, flag)
    return cropped

def convert_to_binary_matrix(img, crossword_size=10):
    # Resize the image to ensure it's a square where each cell is 10x10 pixels
    img_resized = cv2.resize(img, (crossword_size * 10, crossword_size * 10))
    binary_matrix = np.zeros((crossword_size, crossword_size), dtype=np.uint8)

    # Iterate over each cell in the resized image and determine if it's filled (white) or not (black)
    for i in range(crossword_size):
        for j in range(crossword_size):
            cell = img_resized[i*10:(i+1)*10, j*10:(j+1)*10]
            if np.mean(cell) > 127:  # if the average color is closer to white
                binary_matrix[i, j] = 1
            else:
                binary_matrix[i, j] = 0

    return binary_matrix

def export_to_json(matrix, filename):
    # Convert the numpy array to a list of lists
    matrix_list = matrix.tolist()
    cross_dict = {"matrix binaire": matrix_list}

    # Save the JSON to a file
    with open(filename, 'w') as json_file:
        json.dump(cross_dict, json_file, indent=4)
    print(f"Matrix exported to {filename}")



# Export the binary matrix to a JSON file
if __name__ == "__main__":
    image_path = "img/img5.jpg"  # Make sure this path is correct
    cropped_crossword = parse_grid(image_path, flag=0)

    if cropped_crossword is not None and cropped_crossword.size > 0:
        binary_matrix = convert_to_binary_matrix(cropped_crossword, crossword_size=10)
        print(binary_matrix)

        # Define the path for the JSON file
        json_filename = "results-json/crossword_binary_matrix.json"
        export_to_json(binary_matrix, json_filename)
    else:
        print("No crossword image could be processed.")