import os
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

additions = ['lar', 'gacha', 'tacha', 'siz', 'sizlar', 'gan', 'dagi', 'ning', 'ni',
             'ga', 'da', 'dan', 'cha', 'oq', 'dek', 'la', 'qa', 'ta', 'chi', 'li', 'si',
             'ki', 'gi', 'ti', "g'i", 'i', 'im', 'lar']

file_path = os.path.join(os.getcwd(), 'comment', 'checkComment', 'negPosWords.csv')


def checkText(text: str, dataFile: str = file_path) -> dict:
    # Load the data into a Pandas dataframe
    data = pd.read_csv(f'{dataFile}', on_bad_lines='skip')

    # Augment the data
    data = pd.concat([data, data.sample(frac=0.5, random_state=42)], ignore_index=True)

    # Fill in missing values
    data = data.fillna('')

    # Clean the data
    data['text'] = data['text'].str.replace('[^a-zA-Z\s]', '').str.lower()

    # Normalize the data
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(data['text'])

    # Split the data into training and testing sets
    train_features, test_features, train_labels, test_labels = train_test_split(features, data['label'], test_size=0.2,
                                                                                random_state=42)

    # Train a logistic regression model on the training data
    classifier = LogisticRegression()
    classifier.fit(train_features, train_labels)

    # Evaluate the model on the testing data
    accuracy = classifier.score(test_features, test_labels)
    print("Aniqlik:", accuracy)

    # Remove attachments
    clean_text = re.sub(r'[^\w\s\']+', '', text)
    words = clean_text.split()
    for word in words:
        for addition in additions:
            if word.endswith(addition):
                word = word.replace(addition, '')
                clean_text = clean_text + " " + word

    # Use the model to predict the label of a new text input
    new_text = [clean_text.lower().replace('[^a-zA-Z\s]', '')]
    new_features = vectorizer.transform(new_text)
    predicted_label = classifier.predict(new_features)[0]
    return {"text": new_text[0], "label": predicted_label}
