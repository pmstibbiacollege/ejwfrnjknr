import subprocess
import os
import shutil

def install_chrome():
    # Create a directory for Chrome
    chrome_dir = os.path.expanduser('~/chrome')
    os.makedirs(chrome_dir, exist_ok=True)
    os.chdir(chrome_dir)

    # Download the Google Chrome package
    subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'], check=True)

    # Extract the package
    subprocess.run(['ar', 'x', 'google-chrome-stable_current_amd64.deb'], check=True)
    subprocess.run(['tar', 'xvf', 'data.tar.xz'], check=True)

    # Move the binaries to a local bin directory
    bin_dir = os.path.expanduser('~/bin')
    os.makedirs(bin_dir, exist_ok=True)
    shutil.move('opt/google/chrome/google-chrome', os.path.join(bin_dir, 'google-chrome'))

    # Add the local bin directory to your PATH
    bashrc_path = os.path.expanduser('~/.bashrc')
    with open(bashrc_path, 'a') as bashrc:
        bashrc.write('export PATH=$HOME/bin:$PATH\n')

    # Refresh the shell environment
    subprocess.run(['bash', '-c', 'source ~/.bashrc'], shell=True)

    # Verify the installation
    result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    install_chrome()
