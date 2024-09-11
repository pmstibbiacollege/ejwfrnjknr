import subprocess

def install_chrome():
    # Download the Google Chrome package
    subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'], check=True)

    # Install the package
    subprocess.run(['su', '-', '-c', 'dpkg -i google-chrome-stable_current_amd64.deb'], check=True)

    # Fix any missing dependencies
    subprocess.run(['su', '-', '-c', 'apt-get install -f -y'], check=True)

    # Verify the installation
    result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    install_chrome()
