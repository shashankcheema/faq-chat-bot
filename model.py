from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class Model:
    def __init__(self, qa_dict):
        self.qa_dict = qa_dict
        self.vectorizer = CountVectorizer()
        self.encoder = LabelEncoder()
        self.clf = RandomForestClassifier(n_estimators=100)

    def train(self):
        df = pd.DataFrame(list(self.qa_dict.items()), columns=['Question', 'Answer'])
        X = self.vectorizer.fit_transform(df['Question']).toarray()
        y = self.encoder.fit_transform(df['Answer'])
        self.clf.fit(X, y)

    def get_response(self, question):
        question = self.vectorizer.transform([question]).toarray()
        prediction = self.clf.predict(question)
        response = self.encoder.inverse_transform(prediction)
        return response
