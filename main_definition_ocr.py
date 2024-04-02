import cv2
import numpy as np
import requests
import io
import json
# from V1_ocr_processing import process_ocr_text 
from V2_ocr_processing import process_ocr_text 


# Read the image
path= 'img/img5.jpg'
img = cv2.imread(path)
height, width, _ = img.shape
roi = img

# Resize the image to reduce file size
roi_resized = cv2.resize(roi, (width // 2, height // 2))

# Compress the image with lower quality to reduce file size
_, compressedimage = cv2.imencode(".jpg", roi_resized, [cv2.IMWRITE_JPEG_QUALITY, 80])
file_bytes = io.BytesIO(compressedimage)

# Check file size
if file_bytes.getbuffer().nbytes <= 1024 * 1024:  
    url_api = "https://api.ocr.space/parse/image"
    result = requests.post(url_api,
                    files = {path: file_bytes},
                    data = {"apikey": "YOUR_API_KEY",  
                            "language": "fre"})  

    # Decode and process the result
    result = result.content.decode()
    result = json.loads(result)

    if 'ParsedResults' in result:
        parsed_results = result['ParsedResults'][0]
        ocr_text = parsed_results['ParsedText']
        print (ocr_text)

        # Call the OCR text processing
        json_result = process_ocr_text(ocr_text)

    print(json_result)
else:
    print("No results returned or an error occurred.")