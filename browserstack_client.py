from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def fetch_redirect_url(url):
    browserstack_username = os.getenv('BROWSERSTACK_USERNAME')
    browserstack_access_key = os.getenv('BROWSERSTACK_ACCESS_KEY')

    # BrowserStack configuration
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    capabilities = {
        'browserName': 'Chrome',
        'browserVersion': 'latest',
        'os': 'Windows',
        'osVersion': '10',
        'name': 'Fetch Redirect URL Test'
    }

    driver = webdriver.Remote(
        command_executor='https://{}:{}@hub.browserstack.com/wd/hub'.format(browserstack_username, browserstack_access_key),
        options=options
    )
    
    # Apply capabilities via options if necessary
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.setCacheDisabled', {'cacheDisabled': True})
    
    try:
        driver.get(url)
        
        # Wait for JavaScript redirection and get the final URL
        WebDriverWait(driver, 30).until(
            EC.url_changes(url)
        )
        final_url = driver.current_url
    finally:
        driver.quit()

    return final_url        WebDriverWait(driver, 30).until(
            EC.url_changes(url)
        )
        final_url = driver.current_url
    finally:
        driver.quit()

    return final_url
