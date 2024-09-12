from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

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

        return jsonify({'second_redirect_url': second_redirect_url})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
