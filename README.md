# WebShell.py

A command-line web shell client that allows you to execute shell commands through HTTP requests.

## Description

WebShell.py is a Python script that creates an interactive command-line interface for sending shell commands to a remote web server. It URL-encodes your commands and sends them via HTTP requests, then displays the server's response as UTF-8 text.

## Features

- Interactive command-line interface with `>` prompt
- URL encoding of shell commands for safe transmission
- HTTP request handling with proper error management
- UTF-8 response display
- Clean exit handling (Ctrl+C, EOF, or exit commands)
- Command-line argument validation
- No external dependencies (uses only Python standard library)

## Installation

No installation required! This script uses only Python standard library modules.

### Requirements

- Python 3.6 or higher
- No external dependencies

## Usage

```bash
python WebShell.py <server:port> <prefix> <suffix>
```

### Arguments

- `server:port` - Target server address and port (e.g., `localhost:8080`)
- `prefix` - URL prefix to prepend to commands (e.g., `cmd=`)
- `suffix` - URL suffix to append to commands (e.g., `.html`)

### Examples

```bash
# Basic usage
python WebShell.py localhost:8080 cmd= .html

# With different server
python WebShell.py 192.168.1.100:3000 exec= .php

# With custom prefix/suffix
python WebShell.py myserver.com:80 /shell?cmd= &output=text
```

### How it works

1. You type a shell command at the `>` prompt
2. The command gets URL-encoded
3. A request is sent to `http://server:port/prefix[encoded_command]suffix`
4. The server's response is displayed as UTF-8 text
5. The process repeats until you exit

### Example Session

```
$ python WebShell.py localhost:8080 cmd= .html
WebShell connecting to localhost:8080
Prefix: cmd=
Suffix: .html
Type 'exit' or 'quit' to terminate

> ls -la
total 8
drwxr-xr-x 2 user user 4096 Jan 15 10:30 .
drwxr-xr-x 3 user user 4096 Jan 15 10:29 ..
-rw-r--r-- 1 user user  123 Jan 15 10:30 file.txt

> whoami
user

> exit
Goodbye!
```

## Exit Commands

- Type `exit` or `quit` to terminate the program
- Press `Ctrl+C` to interrupt and exit
- Press `Ctrl+D` (EOF) to exit

## Error Handling

The script handles various error conditions:

- Invalid server:port format
- Invalid port numbers (must be 1-65535)
- HTTP errors (404, 500, etc.)
- Network timeouts
- Connection failures
- Invalid UTF-8 responses

## Security Note

This tool is designed for legitimate system administration and testing purposes. Always ensure you have proper authorization before using this tool on any system.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Author

**Garland Glessner**  
Email: gglessner@gmail.com

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions, please open an issue on GitHub or contact the author at gglessner@gmail.com.
