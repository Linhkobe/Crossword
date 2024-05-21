import process_grid_image

def test_parse_grid():
    image_path = "uploads/grid.jpg"  
    try:
        cropped_crossword = process_grid_image.parse_grid(image_path, flag=0)
        if cropped_crossword is not None and cropped_crossword.size > 0:
            binary_matrix = process_grid_image.convert_to_binary_matrix(cropped_crossword, crossword_size=10)
            print(binary_matrix)

            json_filename = "json/crossword_binary_matrix.json"
            process_grid_image.export_to_json(binary_matrix, json_filename)
        else:
            print("No crossword image could be processed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_parse_grid()
