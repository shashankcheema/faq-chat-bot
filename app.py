from flask import Flask, render_template, request
from preprocessor import Preprocessor
from model import Model

app = Flask(__name__)

preprocessor = Preprocessor('/path/to/markdown/files')
qa_dict = preprocessor.preprocess()

model = Model(qa_dict)
model.train()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(model.get_response(userText))

if __name__ == "__main__":
    app.run()
