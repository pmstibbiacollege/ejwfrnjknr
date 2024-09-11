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

    if not browserstack_username or not browserstack_access_key:
        raise ValueError("BrowserStack credentials are missing")

    # BrowserStack configuration
    capabilities = {
        'browserName': 'Chrome',
        'browserVersion': 'latest',
        'os': 'Windows',
        'osVersion': '10',
        'name': 'Fetch Redirect URL Test'
    }
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Remote(
        command_executor=f'https://{browserstack_username}:{browserstack_access_key}@hub.browserstack.com/wd/hub',
        options=options,
        desired_capabilities=capabilities
    )

    try:
        driver.get(url)
        
        # Wait for JavaScript redirection and get the final URL
        WebDriverWait(driver, 30).until(
            EC.url_changes(url)
        )
        final_url = driver.current_url
    finally:
        driver.quit()

    return final_url
