from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Function to check if the URL is deceptive using Google Safe Browsing API
def check_url_safety(api_key, url):
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    payload = {
        "client": {
            "clientId": "yourcompanyname",
            "clientVersion": "1.5.2"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }
    params = {'key': api_key}
    response = requests.post(api_url, json=payload, params=params)
    result = response.json()

    if "matches" in result:
        return "Warning: The URL is flagged as deceptive."
    else:
        return "The URL is safe."

# Function to send email
def send_email(subject, body):
    smtp_server = 'mail.ntbs.co.in'
    smtp_port = 465
    smtp_user = 'nirmal.bhonsle@ntbs.co.in'
    smtp_password = 'Ntbs@5163'
    
    from_email = 'CKSoftwares System <nirmal.bhonsle@ntbs.co.in>'
    to_email = 'officialraybin@protonmail.com'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: Check your username/password.")
    except smtplib.SMTPConnectError:
        print("SMTP Connection Error: Check your server settings.")
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to replace placeholders in the URL
def process_url(url):
    if '[EMail_LocalPart]' in url and '[EMail_DomainPart]' in url:
        return url.replace('[EMail_LocalPart]', 'test').replace('[EMail_DomainPart]', 'test.com')
    elif '[[-User-]]' in url and '[[-Domain-]]' in url:
        return url.replace('[[-User-]]', 'test').replace('[[-Domain-]]', 'test.com')
    else:
        return None

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.txt'):
        with open('urls.txt', 'w') as f:
            f.write(file.read().decode('utf-8'))
        return jsonify({'message': 'File uploaded and contents updated successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/check_links', methods=['POST'])
def check_links():
    try:
        results = []
        
        with open('urls.txt', 'r') as file:
            urls = file.readlines()

        for original_url in urls:
            original_url = original_url.strip()
            processed_url = process_url(original_url)

            if processed_url:
                options = Options()
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')

                # BrowserStack credentials
                browserstack_username = 'hitenvasoya_uXSGHj'
                browserstack_access_key = 'JJSDpLRW35ssHmpiRnEp'

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

                driver.get(processed_url)
                driver.implicitly_wait(30)
                second_redirect_url = driver.current_url
                driver.quit()

                # Get the base URL and subdomain from the second_redirect_url
                parsed_url = urlparse(second_redirect_url)
                base_url = parsed_url.netloc
                subdomain = parsed_url.hostname.split('.')[0] if len(parsed_url.hostname.split('.')) > 2 else ''

                # Get the subdomain of the original URL
                original_url_parsed = urlparse(original_url)
                original_subdomain = original_url_parsed.hostname.split('.')[0] if len(original_url_parsed.hostname.split('.')) > 2 else ''

                # Check if the second_redirect_url is deceptive
                api_key = "AIzaSyDyOPmvplb1WtijK21xb4ApvRZwCxtsA18"
                safety_status = check_url_safety(api_key, second_redirect_url)

                if safety_status == "Warning: The URL is flagged as deceptive.":
                    subject = f"Link tester: {original_subdomain}"
                    body = f"Cheers from Priest, This link is down: {original_subdomain} pythonanywhere.com"
                    send_email(subject, body)

                results.append({
                    'original_subdomain': original_subdomain,
                    'safety_status': safety_status
                })

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
