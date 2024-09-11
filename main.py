import subprocess
import os
import shutil

def install_chrome():
    # Create a directory for Chrome
    os.makedirs(os.path.expanduser('~/chrome'), exist_ok=True)
    os.chdir(os.path.expanduser('~/chrome'))

    # Download the Google Chrome package
    subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'])

    # Extract the package
    subprocess.run(['ar', 'x', 'google-chrome-stable_current_amd64.deb'])
    subprocess.run(['tar', 'xvf', 'data.tar.xz'])

    # Move the binaries to a local bin directory
    os.makedirs(os.path.expanduser('~/bin'), exist_ok=True)
    shutil.move('opt/google/chrome/google-chrome', os.path.expanduser('~/bin/google-chrome'))

    # Add the local bin directory to your PATH
    with open(os.path.expanduser('~/.bashrc'), 'a') as bashrc:
        bashrc.write('export PATH=$HOME/bin:$PATH\n')
    subprocess.run(['source', os.path.expanduser('~/.bashrc')], shell=True)

    # Verify the installation
    chrome_path = os.path.expanduser('~/bin/google-chrome')
    if not os.path.exists(chrome_path):
        chrome_path = os.path.expanduser('~/bin/google-chrome-stable')

    result = subprocess.run([chrome_path, '--version'], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    install_chrome()
