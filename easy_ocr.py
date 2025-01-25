import cv2
import numpy as np
import easyocr
from preprocess import tfidf_keywords

# Function to perform OCR using EasyOCR
def perform_ocr_easyocr(img_path):
    """
    This function reads an image from the provided path and performs OCR using EasyOCR.
    Returns the detected text.
    """
    # Initialize the EasyOCR Reader (You can specify languages like 'en' for English)
    reader = easyocr.Reader(['en'])  # Add more languages as needed (e.g., 'en', 'fr', 'de')

    # Read the image using OpenCV
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {img_path}")

    #img = apply_binarization(img)  # Pass image, not path

    # Perform OCR on the image
    results = reader.readtext(img)

    # Initialize an empty string to store detected text
    text = ""
    for (bbox, text_line, prob) in results:
        text += text_line + "\n"
        # Optionally, you can draw bounding boxes on the image
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        
    return text

# if __name__ == "__main__":
#     path = r"C:\Users\vedant raikar\Downloads\download.webp"
#     try:
#         text = perform_ocr_easyocr(path)
#         filter_text = tfidf_keywords(text)
#         print("Detected Filtered Text:")
#         print(text)

        
#     except Exception as e:
#         print(f"Error: {e}")