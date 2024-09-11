from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

app = Flask(__name__)

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Optional
chrome_options.binary_location = os.environ.get('CHROME_PATH')  # Ensure correct path

chrome_service = Service(executable_path=os.environ.get('CHROMEDRIVER_PATH'))

def get_second_redirect_url(initial_url):
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get(initial_url)
    
    try:
        # Wait for JavaScript to modify the page
        WebDriverWait(driver, 10).until(
            EC.url_changes(initial_url)  # Wait for the URL to change
        )
        # Check the new URL (the second redirect)
        second_redirect_url = driver.current_url
    finally:
        driver.quit()

    return second_redirect_url

@app.route('/check_redirect', methods=['POST'])
def check_redirect():
    if request.is_json:
        data = request.get_json()
        initial_url = data.get('url')
    elif request.form:
        initial_url = request.form.get('url')
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

    if not initial_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        second_redirect_url = get_second_redirect_url(initial_url)
        return jsonify({"second_redirect_url": second_redirect_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
