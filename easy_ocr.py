import cv2
import numpy as np
from PIL import Image
import tempfile
import easyocr

# Step 1: Normalization
def normalize_image(image):
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    normalized_img = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
    return normalized_img

# Step 2: Skew Correction
def deskew(image):
    co_ords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(co_ords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# Step 3: Image Scaling
def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename

# Step 4: Noise Removal
def remove_noise(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

# Step 5: Thinning and Skeletonization
def thinning(image):
    kernel = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(image, kernel, iterations=1)
    return eroded

# Step 6: Gray Scaling
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 7: Thresholding or Binarization
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Step 8: Rotation Correction
def correct_rotation(image):
    edges = cv2.Canny(image, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta) - 90
            angles.append(angle)
        median_angle = np.median(angles)
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        rotated_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated_image
    return image

def preprocess_image(file_path):

    image = cv2.imread(file_path)
    gray_image = get_grayscale(image)
    normalized_image = normalize_image(gray_image)
    deskewed_image = deskew(normalized_image)
    rotated_image = correct_rotation(deskewed_image)
    high_dpi_image_path = set_image_dpi(rotated_image)
    high_dpi_image = cv2.imread(high_dpi_image_path)
    denoised_image = remove_noise(high_dpi_image)
    thinned_image = thinning(denoised_image)
    binary_image = thresholding(thinned_image)
    return binary_image



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
    img = preprocess_image(img)
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

