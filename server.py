# Flask backend server with AI and scraping logic
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Jojo Plus Integrated Fullsite'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
