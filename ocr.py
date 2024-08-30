#import libraries
import cv2
import pytesseract
import numpy as np 


# Function to preprocess the image
def preprocess_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return img

#function to perform ocr 
def perform_ocr(img_path):
    pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract/tesseract.exe"
    img = cv2.imread(img_path)  
    img = preprocess_image(img)
    text = pytesseract.image_to_string(img, config='--oem 3 --psm 6') 
    #data = pytesseract.image_to_data(img , output_type=pytesseract.Output.DICT)
    #n_boxes = len(data['level'])
    #for i in range(n_boxes):
        #(x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        #confidence = int(data['conf'][i])
        #if confidence > 0: # Only consider confident detections
            #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.putText(img, str(confidence), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return text

#image_path = r"C:\Users\vedant raikar\Desktop\ocr health project\tesseract-ocr-project\test files\img7.webp"
#text  = perform_ocr(image_path)
#print(text)



