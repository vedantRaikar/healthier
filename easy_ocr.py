# Import required libraries
import easyocr
import cv2
import numpy as np


# Function to calculate skew angle and rotate the image
def correct_image_rotation(img):
    """
    Detect and correct the rotation of the image.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    
    if lines is not None:
        angles = []
        for line in lines:
            rho, theta = line[0]
            angle = np.degrees(theta) - 90  # Convert to degrees and normalize
            angles.append(angle)

        # Calculate the median angle (robust to outliers)
        median_angle = np.median(angles)

        # Rotate the image to correct orientation
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        rotated_img = cv2.warpAffine(img, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        return rotated_img

    # If no lines are detected, return the original image
    return img


# Preprocessing function with rotation correction
def preprocess_image(img_path):
    """
    Preprocess the image for OCR by correcting rotation, applying grayscale conversion, 
    OTSU thresholding, dilation, and contour extraction.
    """
    # Read the image using OpenCV
    img = cv2.imread(img_path)

    # Correct image rotation
    img = correct_image_rotation(img)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply OTSU thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Define a rectangular kernel for dilation
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Apply dilation
    dilation = cv2.dilate(thresh, rect_kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Create a mask to highlight regions of interest
    mask = np.zeros_like(img)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)

    # Combine the mask with the original image
    preprocessed_img = cv2.bitwise_and(img, mask)
    return preprocessed_img


# Function to perform OCR using EasyOCR
def perform_ocr_easyocr(img_path):
    """
    Perform OCR using EasyOCR with preprocessing.
    """
    # Preprocess the image
    preprocessed_img = preprocess_image(img_path)

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])  # Specify languages as needed

    # Perform OCR on the preprocessed image
    results = reader.readtext(preprocessed_img)

    # Extract and format detected text
    text = ""
    for (bbox, text_line, prob) in results:
        text += f"{text_line}\n"

    return text

