import os
import markdown
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

class Preprocessor:
    def __init__(self, directory):
        self.directory = directory
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def nltk_pos_to_wordnet_pos(self, nltk_pos):
        if nltk_pos.startswith('J'):
            return wordnet.ADJ
        elif nltk_pos.startswith('V'):
            return wordnet.VERB
        elif nltk_pos.startswith('N'):
            return wordnet.NOUN
        elif nltk_pos.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def process_file(self, file):
        with open(file, 'r') as file:
            md_text = file.read()
            html = markdown.markdown(md_text)
            soup = BeautifulSoup(html, features="html.parser")
            text = soup.get_text()
            sentences = nltk.sent_tokenize(text)
            i = 0
            qa_dict = {}
            while i < len(sentences):
                if sentences[i].endswith('?'):
                    question = sentences[i]
                    answer = ''
                    i += 1
                    while i < len(sentences) and not sentences[i].endswith('?'):
                        answer += ' ' + sentences[i]
                        i += 1
                    qa_dict[question] = answer.strip()
                else:
                    i += 1
            return qa_dict

    def preprocess(self):
        files = [os.path.join(root, file) for root, dirs, files in os.walk(self.directory) for file in files if file.endswith('.md')]
        qa_dicts = [self.process_file(file) for file in files]
        qa_dict = {k: v for d in qa_dicts for k, v in d.items()}
        qa_dict = {q: a for q, a in qa_dict.items() if a.strip()}
        return qa_dict
