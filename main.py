import subprocess

def get_chrome_version():
result = subprocess.run(['google-chrome', '--version'], stdout=subprocess.PIPE)
return result.stdout.decode('utf-8').strip()

chrome_version = get_chrome_version()
print(f"Google Chrome version: {chrome_version}")
