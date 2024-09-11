from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

app = Flask(__name__)

# Function to read the URL from url.txt file
def get_url_from_txt(file_path='url.txt'):
    with open(file_path, 'r') as file:
        return file.readline().strip()

# Function to get the second redirect URL using Selenium
def get_second_redirect(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Specify the path to the Chrome binary
    options.binary_location = "/usr/bin/google-chrome"

    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the URL
    driver.get(url)

    # Wait for the redirect to complete (adjust time if necessary)
    driver.implicitly_wait(10)

    # Get the final redirected URL
    second_redirect_url = driver.current_url

    driver.quit()
    return second_redirect_url

# Flask route to check the URL redirection
@app.route('/check_url', methods=['GET'])
def check_url():
    url = get_url_from_txt()  # Read the URL from url.txt
    final_url = get_second_redirect(url)  # Get the final redirect URL
    return jsonify({"redirected_url": final_url})  # Return as JSON response

# Route to check if Chrome is installed (for debugging)
@app.route('/check_chrome', methods=['GET'])
def check_chrome():
    chrome_binary = "/usr/bin/google-chrome"
    files_in_usr_bin = os.listdir("/usr/bin/")
    return jsonify({
        "chrome_installed": os.path.exists(chrome_binary),
        "files_in_usr_bin": files_in_usr_bin
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to port 5000 if PORT isn't set
    app.run(host='0.0.0.0', port=port, debug=True)
