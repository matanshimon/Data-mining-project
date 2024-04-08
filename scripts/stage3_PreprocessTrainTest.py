# Classifier Random Forest
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
import os
import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import hamming_loss, jaccard_score
from sklearn.metrics import accuracy_score

def run():
    # Load the data
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "processed", "features.csv")
    p = os.path.join(script_dir, "..", "data", "processed", "processed.csv")

    # Title,Word Frequency,Sentiment,Length,Number of Characters,Entity Frequency,Topics,Genres
    data = pd.read_csv(data_path)

    # Convert Genre into numerical values
    genres_lists = data['Genres'].apply(ast.literal_eval)
    data['Genres'] = genres_lists
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(genres_lists)

    X_other = data[['Sentiment', 'Length', 'Number of Characters']].to_numpy()

    # Split the data
    train_data, test_data, y_train, y_test = train_test_split(data, y, test_size=0.2, random_state=42)

    # Transform the data into numpy arrays
    X_train_other = train_data[['Sentiment', 'Length', 'Number of Characters']].to_numpy()
    X_test_other = test_data[['Sentiment', 'Length', 'Number of Characters']].to_numpy()

    # Train the models
    clf_other = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_other.fit(X_train_other, y_train)

    # Combine the results
    y_pred = clf_other.predict(X_test_other)
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: {:.2%}".format(accuracy))

    # Evaluate the model
    print("Hamming Loss:", hamming_loss(y_test, y_pred))
    print("Jaccard Score:", jaccard_score(y_test, y_pred, average='samples'))