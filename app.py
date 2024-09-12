from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route('/check_link', methods=['POST'])
def check_link():
    try:
        # Read the link from urls.txt file
        with open('urls.txt', 'r') as file:
            link = file.readline().strip()

        # Set up Chrome options
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        # BrowserStack credentials
        browserstack_username = 'YOUR_BROWSERSTACK_USERNAME'
        browserstack_access_key = 'YOUR_BROWSERSTACK_ACCESS_KEY'

        # BrowserStack capabilities
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

        # Initialize the WebDriver with BrowserStack
        driver = webdriver.Remote(
            command_executor=f'https://{browserstack_username}:{browserstack_access_key}@hub-cloud.browserstack.com/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )

        # Navigate to the link
        driver.get(link)
        driver.implicitly_wait(10)

        # Get the second redirect URL
        second_redirect_url = driver.current_url
        driver.quit()

        return jsonify({'second_redirect_url': second_redirect_url})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
