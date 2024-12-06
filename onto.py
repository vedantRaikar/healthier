from SPARQLWrapper import SPARQLWrapper, JSON

def query_wikidata(keyword):
    """Query Wikidata to find related entities for a given keyword."""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
    # SPARQL query to retrieve broader, narrower, and related terms
    query = f"""
    SELECT ?item ?itemLabel WHERE {{
      ?item ?label "{keyword}"@en.  # Match keyword with any label
      ?item rdfs:label ?itemLabel.
      FILTER (lang(?itemLabel) = "en")
    }}
    LIMIT 20
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    entities = []
    for result in results["results"]["bindings"]:
        entities.append(result["itemLabel"]["value"])
    
    return entities

# Example Usage
keyword = "NS 414"
related_entities = query_wikidata(keyword)
print("Related Entities:", related_entities)
