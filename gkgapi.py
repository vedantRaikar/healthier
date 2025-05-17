import requests

def check_drug_interaction(drug1, drug2):
    url = "https://api.fda.gov/drug/label.json"
    params = {"search": f"{drug1} OR {drug2}", "limit": 5}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        interactions = []

        for result in data.get("results", []):
            if "drug_interactions" in result:
                interactions.append(result["drug_interactions"])

        if interactions:
            return interactions
        else:
            return f"No interaction data found for {drug1} and {drug2}."
    else:
        return f"API request failed with status code {response.status_code}."

# Example Usage
drug1 = "Aspirin"
drug2 = "Ibuprofen"
interaction_info = check_drug_interaction(drug1, drug2)
print(interaction_info)
