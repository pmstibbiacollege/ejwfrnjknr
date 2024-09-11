from flask import Flask, jsonify
import os
from browserstack_client import fetch_redirect_url

app = Flask(__name__)

@app.route('/')
def index():
    # Read the URL from a text file
    with open('urls.txt', 'r') as file:
        url = file.readline().strip()
    
    # Fetch the second redirect URL using BrowserStack
    redirect_url = fetch_redirect_url(url)
    
    return jsonify({'redirect_url': redirect_url})

if __name__ == '__main__':
    app.run(debug=True)
