import pandas as pd
import requests
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

class Model:
    def __init__(self, qa_dict):
        self.qa_dict = qa_dict
        self.vectorizer = CountVectorizer()
        self.encoder = LabelEncoder()
        self.clf = RandomForestClassifier()

    def train(self):
        df = pd.DataFrame(list(self.qa_dict.items()), columns=['Question', 'Answer'])
        X = self.vectorizer.fit_transform(df['Question']).toarray()
        y = self.encoder.fit_transform(df['Answer'])
        self.clf.fit(X, y)

    def get_response(self, question):
        X = self.vectorizer.transform([question]).toarray()
        pred = self.clf.predict(X)
        if max(self.clf.predict_proba(X)[0]) > 0.5:
            return self.encoder.inverse_transform(pred)[0]
        else:
            return self.get_stackoverflow_response(question)

    def get_stackoverflow_response(self, question):
        question = question.replace(' ', '+')
        response = requests.get(f"https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=relevance&q={question}&site=stackoverflow")
        data = json.loads(response.text)
        if not data['items']:
            return "I'm sorry, I couldn't find an answer to your question on Stack Overflow."
        else:
            return f"I found a similar question on Stack Overflow: {data['items'][0]['link']}"
