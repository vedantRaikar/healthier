import streamlit as st
from groq import Groq
from easy_ocr import perform_ocr_easyocr
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from context import fetch_wikipedia_context
from preprocess import tfidf_keywords

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
    """Save the uploaded file and perform OCR."""
    image_path = uploaded_file.name
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return image_path

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

def enable_flashlight():
    """Embed JavaScript to enable flashlight on supported devices."""
    st.components.v1.html(
        """
        <style>
            .flashlight-btn {
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-align: center;
                transition: background-color 0.3s ease;
            }
            .flashlight-btn:hover {
                background-color: #45a049;
            }
        </style>
        <script>
        async function enableFlashlight() {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            const track = stream.getVideoTracks()[0];
            const capabilities = track.getCapabilities();
            if (capabilities.torch) {
                await track.applyConstraints({ advanced: [{ torch: true }] });
                alert('Flashlight enabled!');
            } else {
                alert('Flashlight not supported on this device.');
            }
        }
        </script>
        <button class="flashlight-btn" onclick="enableFlashlight()">Enable Flashlight</button>
        """,
        height=100,
    )

def main():
    """Main Streamlit app function."""
    st.title("Personalized Health Assistant")

    # Enable camera input
    enable_camera = st.checkbox("Enable camera")

    if enable_camera:
        enable_flashlight()

    uploaded_file = st.camera_input("Take a picture", disabled=not enable_camera)

    if uploaded_file is not None:
        image_path = process_uploaded_image(uploaded_file)
        user_details = enter_details()

        if user_details:
            analyze_image_and_generate_response(image_path, user_details)
        else:
            st.warning("Please submit your details to proceed.")
    else:
        st.warning("Please upload an image to analyze.")

if __name__ == "__main__":
    main()