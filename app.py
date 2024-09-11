from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route('/check_link', methods=['POST'])
def check_link():
    # Read the link from urls.txt file
    with open('urls.txt', 'r') as file:
        link = file.readline().strip()

    # Set up Selenium with BrowserStack
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # BrowserStack credentials
    browserstack_username = 'YOUR_BROWSERSTACK_USERNAME'
    browserstack_access_key = 'YOUR_BROWSERSTACK_ACCESS_KEY'

    capabilities = {
        'os': 'Windows',
        'os_version': '10',
        'browser': 'Chrome',
        'browser_version': 'latest',
        'name': 'Flask App Test',
        'browserstack.local': 'false',
        'browserstack.selenium_version': '3.14.0'
    }

    driver = webdriver.Remote(
        command_executor=f'https://{browserstack_username}:{browserstack_access_key}@hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=capabilities,
        options=options
    )

    driver.get(link)
    driver.implicitly_wait(10)
    second_redirect_url = driver.current_url
    driver.quit()

    return jsonify({'second_redirect_url': second_redirect_url})

if __name__ == '__main__':
    app.run(debug=True)
