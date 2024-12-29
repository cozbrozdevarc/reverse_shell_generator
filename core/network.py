import requests
import subprocess
import shutil
import sys
from config import IPINFO_URL

def get_public_ip():
    try:
        response = requests.get(IPINFO_URL, timeout=10)
        response.raise_for_status()
        ip_data = response.json()
        return ip_data.get('ip')
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}", file=sys.stderr)
        return None

def check_ncat_installed():
    return shutil.which('ncat') is not None

def start_ncat_listener(port):
    try:
        # Validate port
        port_num = int(port)
        if not (1024 <= port_num <= 65535):
            raise ValueError("Port must be between 1024 and 65535")
            
        if not check_ncat_installed():
            print("Error: ncat is not installed. Please install nmap/ncat first.", file=sys.stderr)
            return False
            
        command = ['ncat', '-lvnp', str(port_num)]
        print(f"Starting listener on port {port_num}...")
        
        # Use shell=True on Windows to avoid console window
        use_shell = sys.platform.startswith('win')
        subprocess.run(command, shell=use_shell, check=True)
        return True
        
    except ValueError as e:
        print(f"Invalid port number: {e}", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error starting ncat listener: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error starting listener: {e}", file=sys.stderr)
        return False
