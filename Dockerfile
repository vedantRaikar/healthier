FROM python:3.9

# Install Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Set the entry point for Streamlit
ENTRYPOINT ["streamlit", "run"]
CMD ["llm.py"]
