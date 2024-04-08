import os
import json
import nltk
import spacy
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from collections import Counter
from gensim import corpora, models
from tqdm import tqdm
from stage1_SubtitleExractor import subtitle_extracttor

subtitle_extracttor()

def feature_extraction():
    nltk.download('punkt')
    nlp = spacy.load('en_core_web_sm')

    script_dir = os.path.dirname(os.path.realpath(__file__))
    data1_path = os.path.join(script_dir, "..", "data", "raw", "subtitle.json")
    features_f_path = os.path.join(script_dir, "..", "data", "processed", "features.csv")

    data = []
    with open(data1_path, 'r') as file:
        for line in file:
            json_line = json.loads(line)
            title = json_line.get('movieName')
            text = json_line.get('text')
            genres = json_line.get('genre')
            data.append((title, text, genres))

    # Feature extraction
    features = []
    for title, text, genres in tqdm(data):
        if text == "":
            continue
        
        # Word Frequency
        word_freq = Counter(nltk.word_tokenize(text.lower()))
        
        
        # Sentiment Analysis
        sentiment = TextBlob(text).sentiment.polarity

        # Length of Subtitles
        length = len(text)

        # Number of Characters (assuming each sentence is a dialogue from a character)
        num_characters = len(nltk.sent_tokenize(text))

        # Named Entity Recognition (NER)
        doc = nlp(text)
            
        entities = [ent.label_ for ent in doc.ents]
        entity_freq = Counter(entities)
        

        # Topic Modeling
        texts = [nltk.word_tokenize(doc) for doc in nltk.sent_tokenize(text)]

        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        ldamodel = models.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)
        topics = ldamodel.print_topics(num_words=3)

        features.append((title, word_freq, sentiment, length, num_characters, entity_freq, topics, genres))

    # Convert to DataFrame for easier manipulation
    import pandas as pd

    df = pd.DataFrame(features, columns=['Title', 'Word Frequency', 'Sentiment', 'Length', 'Number of Characters', 'Entity Frequency', 'Topics', 'Genres'])

    df.to_csv(features_f_path, index=False)