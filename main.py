import subprocess

def install_chrome():
    # Download the Google Chrome package
    subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'])

    # Install the package
    subprocess.run(['sudo', 'dpkg', '-i', 'google-chrome-stable_current_amd64.deb'])

    # Fix any missing dependencies
    subprocess.run(['sudo', 'apt-get', 'install', '-f'])

    # Verify the installation
    result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    install_chrome()
