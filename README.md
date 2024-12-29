# Shell Generator

A Python-based shell script generator for creating remote shell connections. This tool supports both Windows and Unix-based systems (MacOS/Linux).

⚠️ **Disclaimer**: This tool is for educational purposes only. Use only on systems you own or have explicit permission to test.

## Features

- 🖥️ Multi-platform support (Windows, MacOS, Linux)
- 🌐 Automatic public IP detection
- 🔧 Automatic nmap/ncat installation
- 🔄 Interactive shell generation
- 🎯 Custom port configuration
- 🔒 SSH connection support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cozbrozdevarc/reverse_shell_generator.git
cd shell-generator
```

2. Install dependencies:
```bash
python install_dependencies.py
```

Or manually install using pip:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the main script:
```bash
python main.py
```

2. Follow the interactive prompts:
   - Enter target IP address (optional)
   - Confirm ncat/nmap installation
   - Select target operating system
   - Choose listening port
   - Wait for file generation
   - Follow connection instructions

## Project Structure
```
shell_generator/
├── main.py
├── config.py
├── core/
│   ├── generator.py
│   ├── network.py
│   └── system.py
├── utils/
│   └── animations.py
└── output/
    └── .gitkeep
```

## Requirements
- Python 3.6 or higher
- requests
- ncat/nmap (auto-installed if missing)

## Safety Notes
- Only use on systems you own or have permission to test
- Keep generated scripts secure
- Don't share connection details
- Use strong authentication

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
If you encounter any problems or have suggestions, please open an issue on the GitHub repository.
