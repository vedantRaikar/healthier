import requests
from dotenv import load_dotenv
import os 

load_dotenv()

hf_key = os.getenv('hf_key')
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": hf_key}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": {
	"source_sentence": "vitamin C",
	"sentences": ['Vitamin C', 'Ascorbic acid', 'Chris Jericho','Kool-Aid','Apple cider']
},
})

print(output)