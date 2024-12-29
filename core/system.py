import subprocess
import platform
import sys
import os
from config import NMAP_INSTALL_URL

def is_admin():
    """Check if script has admin privileges"""
    try:
        if platform.system() == 'Windows':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False

def install_nmap_windows():
    """Install nmap on Windows systems"""
    if platform.system() != 'Windows':
        print("This function is only for Windows systems", file=sys.stderr)
        return False
        
    if not is_admin():
        print("Administrator privileges required to install nmap", file=sys.stderr)
        return False
        
    try:
        # Set execution policy for current process only
        admin_cmd = ["powershell", "-Command", 
                    "Set-ExecutionPolicy", "Bypass", "-Scope", "Process", "-Force"]
        
        # Download and run nmap installer
        install_cmd = ["powershell", "-Command",
                      f"Invoke-WebRequest -Uri '{NMAP_INSTALL_URL}' -OutFile 'nmap_install.ps1'; " +
                      "if (Test-Path 'nmap_install.ps1') { " +
                      "    ./nmap_install.ps1; " +
                      "    Remove-Item 'nmap_install.ps1' " +
                      "} else { " +
                      "    Write-Error 'Failed to download installer' " +
                      "}"]
        
        subprocess.run(admin_cmd, check=True, capture_output=True)
        subprocess.run(install_cmd, check=True)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error during nmap installation: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error during installation: {e}", file=sys.stderr)
        return False

def ssh_connect(ip_address):
    """Establish SSH connection with proper validation"""
    if not ip_address:
        print("No IP address provided", file=sys.stderr)
        return False
        
    try:
        # Basic IP validation
        parts = ip_address.split('.')
        if len(parts) != 4 or not all(0 <= int(p) <= 255 for p in parts):
            raise ValueError("Invalid IP address format")
            
        # Get username for SSH connection
        username = input("Enter SSH username (default: root): ").strip() or "root"
        
        ssh_command = ["ssh", f"{username}@{ip_address}"]
        print(f"Connecting to {username}@{ip_address}...")
        
        return subprocess.run(ssh_command, check=True)
        
    except ValueError as e:
        print(f"Invalid IP address: {e}", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as e:
        print(f"SSH connection failed: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error during SSH connection: {e}", file=sys.stderr)
        return False
