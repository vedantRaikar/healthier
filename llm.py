import streamlit as st 
from groq import Groq
from ocr import perform_ocr
import os
from dotenv import load_dotenv
import json 
from concurrent.futures import ThreadPoolExecutor


# Load environment variables from .env file
client = Groq(
    api_key=st.secrets["API_KEY"],
)


#taking user details
def enter_details():
    name = st.text_input("What's your name?")
    age = st.text_input("Enter your age:")
    gender = st.selectbox("Enter your gender:", ("Male", "Female", "Other"))
    disease = st.text_area("Enter the details of any disease you have:") 
    #return str('The persons age is: '+ age + ' the patients name is: '+ name + 'the persons gender is: '+ gender +' The details about the persons health conditions: ' +disease)
    if st.button("Submit"):
        # When the button is pressed, return the user details as a formatted string
        return f'The person\'s age is: {age}, the patient\'s name is: {name}, the person\'s gender is: {gender}, The details about the person\'s health conditions: {disease}'
    else:
        # Return None if the button hasn't been pressed yet
        return None

   
#generating the output
def generate_content(prompt):
    response = client.chat.completions.create(
        
    messages=[
        {"role": "system","content": "you are a health assistant"},
        {"role": "user","content": prompt,}],
        model="gemma-7b-it",# Or "Llama-3-8B" depending on your preference
        )
    return response

#main
#image_path = r"C:\Users\vedant raikar\Desktop\ocr health project\tesseract-ocr-project\test files\img4.jpg"
#text = perform_ocr(image_path)
#text = text.rstrip('\n')
#userdetails = enter_details()
#output = generate_content("analyse this food ingredients:"+text+"based on these user details: "+userdetails+"And give a personalized response.")
#print(output.choices[0].message.content)


def main():
    st.title("Personalized Health Assistant")
    #image_path = r"C:\Users\vedant raikar\Desktop\ocr health project\tesseract-ocr-project\test files\img4.jpg"
    uploaded_file = st.file_uploader("Upload an image of food ingredients", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file is not None:
        image_path = uploaded_file.name
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    # Using ThreadPoolExecutor to parallelize OCR and user input
    if uploaded_file is not None:
        
        user_details = enter_details()

        # Parallelize OCR processing
        with ThreadPoolExecutor() as executor:
            ocr_future = executor.submit(perform_ocr, image_path)
            ocr_text = ocr_future.result()

        # Generate content based on OCR text and user details
        prompt = f"Analyze these food ingredients: {ocr_text} based on these user details: {user_details} and give a personalized response."
        output = generate_content(prompt)

        # Print the personalized response
        # Display the personalized response
        st.subheader("Personalized Response")
        st.write(output.choices[0].message.content)
        #print(output.choices[0].message.content)
    else:
        st.warning("Please upload an image to analyze.")

if __name__ == "__main__":
    main()


