from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

if __name__ == '__main__':
    app.run(debug=True)
