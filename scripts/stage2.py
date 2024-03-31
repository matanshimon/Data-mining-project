import json
import spacy
import pandas as pd

# Load the English model of spaCy
nlp = spacy.load("en_core_web_sm")

# Read the JSON objects from the file
trailers = []
with open("../data/raw/subtitles.txt", "r") as f:
    for line in f:
        try:
            trailer = json.loads(line)
            trailers.append(trailer)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON: {line}")

# Prepare lists to store data
titles = []
nouns_list = []
verbs_list = []
adjectives_list = []
entities_list = []

# Loop over the trailers
for trailer in trailers:
    # Tokenize the 'text' field
    doc = nlp(trailer['text'])

    # Extract the nouns, verbs, and adjectives
    nouns = [token.lemma_ for token in doc if token.pos_ == 'NOUN']
    verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB']
    adjectives = [token.lemma_ for token in doc if token.pos_ == 'ADJ']

    # Extract the named entities
    named_entities = [ent.text for ent in doc.ents]

    # Append data to lists
    titles.append(trailer['title'])
    nouns_list.append(nouns)
    verbs_list.append(verbs)
    adjectives_list.append(adjectives)
    entities_list.append(named_entities)

# Create a DataFrame
df = pd.DataFrame({
    'Title': titles,
    'Nouns': nouns_list,
    'Verbs': verbs_list,
    'Adjectives': adjectives_list,
    'Named Entities': entities_list
})

# Save DataFrame to a CSV file
df.to_csv('../data/processed/trailers.csv', index=False)