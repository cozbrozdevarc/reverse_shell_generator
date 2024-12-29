import subprocess
import sys
import os

def install_dependencies():
    try:
        # Get the absolute path to requirements.txt
        reqs_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        
        if not os.path.exists(reqs_path):
            print(f"Error: Could not find requirements.txt at {reqs_path}", file=sys.stderr)
            return False
            
        print("Upgrading pip...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', reqs_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        
        print("All dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}", file=sys.stderr)
        if e.stderr:
            print(f"Details: {e.stderr.decode()}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error during installation: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)
