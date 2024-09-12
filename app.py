from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import requests

app = Flask(__name__)

# Function to check if the URL is deceptive using Google Safe Browsing API
def check_url_safety(api_key, url):
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    payload = {
        "client": {
            "clientId": "yourcompanyname",
            "clientVersion": "1.5.2"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }
    params = {'key': api_key}
    response = requests.post(api_url, json=payload, params=params)
    result = response.json()

    if "matches" in result:
        return "Warning: The URL is flagged as deceptive."
    else:
        return "The URL is safe."

@app.route('/check_link', methods=['POST'])
def check_link():
    try:
        with open('urls.txt', 'r') as file:
            link = file.readline().strip()

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        # BrowserStack credentials
        browserstack_username = 'zrh_Z82hYaNwHkX'
        browserstack_access_key = 'Dcsmx8XkFQD7sLwjzLLG'

        capabilities = {
            'bstack:options': {
                'os': 'Windows',
                'osVersion': '10',
                'browserName': 'Chrome',
                'browserVersion': 'latest',
                'projectName': 'Flask App Test',
                'buildName': 'Build 1',
                'sessionName': 'Check Link',
                'local': 'false',
                'seleniumVersion': '3.14.0'
            }
        }

        driver = webdriver.Remote(
            command_executor=f'https://{browserstack_username}:{browserstack_access_key}@hub-cloud.browserstack.com/wd/hub',
            options=options
        )

        driver.get(link)
        driver.implicitly_wait(30)
        second_redirect_url = driver.current_url
        driver.quit()

        # Get the base URL from the second_redirect_url
        base_url = urlparse(second_redirect_url).netloc

        # Check if the base URL is deceptive
        api_key = "AIzaSyDyOPmvplb1WtijK21xb4ApvRZwCxtsA18"
        safety_status = check_url_safety(api_key, second_redirect_url)

        return jsonify({
            'second_redirect_url': second_redirect_url,
            'base_url': base_url,
            'safety_status': safety_status
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
