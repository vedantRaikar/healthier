import streamlit as st
from groq import Groq
from easy_ocr import perform_ocr_easyocr
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from context import fetch_wikipedia_context
from preprocess import tfidf_keywords
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
key = os.getenv('API_KEY')
client = Groq(api_key=key)

def enter_details():
    """Prompt user for their details and return them as a formatted string."""
    name = st.text_input("What's your name?")
    age = st.text_input("Enter your age:")
    gender = st.selectbox("Enter your gender:", ("Male", "Female", "Other"))
    disease = st.text_area("Enter the details of any disease you have:")

    if st.button("Submit"):
        return f"The person's age is: {age}, the patient's name is: {name}, the person's gender is: {gender}, The details about the person's health conditions: {disease}"
    return None

def generate_content(prompt, context):
    """Generate a response using the Groq client based on the given prompt and context."""
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"You are a health assistant with the following context: {context}. Think step by step."},
            {"role": "user", "content": prompt},
        ],
        model="llama-3.1-8b-instant",  # Or "Llama-3-8B" depending on your preference
    )
    return response

def process_uploaded_image(uploaded_file):
    """Compress and save the uploaded image."""
    image_path = uploaded_file.name
    try:
        # Open the uploaded image
        image = Image.open(uploaded_file)
        # Compress the image and save it as JPEG
        compressed_image_path = f"compressed_{image_path}"
        image = image.convert("RGB")  # Ensure compatibility with JPEG
        image.save(compressed_image_path, "JPEG", optimize=True, quality=70)
        return compressed_image_path
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

def analyze_image_and_generate_response(image_path, user_details):
    """Perform OCR on the image, extract context, and generate a personalized response."""
    with ThreadPoolExecutor() as executor:
        # Perform OCR in parallel
        ocr_future = executor.submit(perform_ocr_easyocr, image_path)
        ocr_text = ocr_future.result()

    if not ocr_text.strip():
        st.error("The image contains no recognizable text.")
        return

    # Extract keywords and fetch context
    keys = tfidf_keywords(ocr_text)
    if not keys:
        st.error("Unable to extract relevant keywords from the image.")
        return

    context = fetch_wikipedia_context(keys)

    # Generate concise summary
    summary_prompt = (
        f"Generate a concise summary of the context, emphasizing key points related to health, food products, "
        f"and their nutritional or functional elements. Highlight essential details considering these keywords: {keys}."
    )
    summary = generate_content(summary_prompt, context)

    # Generate personalized response
    analysis_prompt = (
        f"Analyze the following food ingredients: {ocr_text}, taking into account the user's details: {user_details}. "
        f"Provide health benefits, potential concerns, and recommendations, including unfamiliar ingredients and their effects."
    )
    personalized_response = generate_content(analysis_prompt, summary)

    # Display personalized response
    st.subheader("Personalized Response")
    st.write(personalized_response.choices[0].message.content)

def main():
    """Main Streamlit app function."""
    st.title("Personalized Health Assistant")

    # Upload an image from the gallery
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        image_path = process_uploaded_image(uploaded_file)
        if image_path:
            user_details = enter_details()

            if user_details:
                analyze_image_and_generate_response(image_path, user_details)
            else:
                st.warning("Please submit your details to proceed.")
        else:
            st.error("Failed to process the uploaded image.")
    else:
        st.warning("Please upload an image to analyze.")

if __name__ == "__main__":
    main()
