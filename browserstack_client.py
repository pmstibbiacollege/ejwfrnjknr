from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_redirect_url(url):
    browserstack_username = os.getenv('zrh_8ZqMwbDvWoy')
    browserstack_access_key = os.getenv('sbRQbrC7CqQfVoPzFK7c')

    # BrowserStack configuration
    capabilities = {
        'browser': 'Chrome',
        'browser_version': 'latest',
        'os': 'Windows',
        'os_version': '10',
        'name': 'Fetch Redirect URL Test'
    }
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Remote(
        command_executor='https://{}:{}@hub.browserstack.com/wd/hub'.format(browserstack_username, browserstack_access_key),
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
