from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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

        # Desired capabilities for BrowserStack
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['os'] = 'Windows'
        capabilities['os_version'] = '10'
        capabilities['browser'] = 'Chrome'
        capabilities['browser_version'] = 'latest'
        capabilities['name'] = 'Flask App Test'
        capabilities['browserstack.local'] = 'false'
        capabilities['browserstack.selenium_version'] = '3.14.0'

        # Set up the Selenium WebDriver with BrowserStack
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
