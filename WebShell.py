#!/usr/bin/env python3
"""
WebShell.py - A command-line web shell client

Copyright (C) 2024 Garland Glessner <gglessner@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import argparse
import urllib.parse
import urllib.request
import urllib.error
import socket


def main():
    parser = argparse.ArgumentParser(description='WebShell - Command-line web shell client')
    parser.add_argument('server_port', help='Server address in format host:port (e.g., localhost:8080)')
    parser.add_argument('prefix', help='URL prefix to prepend to commands')
    parser.add_argument('suffix', help='URL suffix to append to commands')
    
    args = parser.parse_args()
    
    # Parse server:port
    try:
        if ':' not in args.server_port:
            print("Error: Server must be in format host:port")
            sys.exit(1)
        
        host, port = args.server_port.split(':', 1)
        port = int(port)
        
        if not (1 <= port <= 65535):
            print("Error: Port must be between 1 and 65535")
            sys.exit(1)
            
    except ValueError:
        print("Error: Invalid port number")
        sys.exit(1)
    
    print(f"WebShell connecting to {host}:{port}")
    print(f"Prefix: {args.prefix}")
    print(f"Suffix: {args.suffix}")
    print("Type 'exit' or 'quit' to terminate")
    print()
    
    while True:
        try:
            # Get user input
            command = input("> ").strip()
            
            # Check for exit commands
            if command.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not command:
                continue
            
            # URL encode the command
            encoded_command = urllib.parse.quote(command)
            
            # Construct the URL
            url = f"http://{host}:{port}/{args.prefix}{encoded_command}{args.suffix}"
            
            # Make the web request
            try:
                with urllib.request.urlopen(url, timeout=30) as response:
                    # Read and decode the response as UTF-8
                    response_data = response.read().decode('utf-8')
                    print(response_data)
                    
            except urllib.error.HTTPError as e:
                print(f"HTTP Error {e.code}: {e.reason}")
            except urllib.error.URLError as e:
                print(f"URL Error: {e.reason}")
            except socket.timeout:
                print("Request timed out")
            except UnicodeDecodeError:
                print("Error: Response contains invalid UTF-8 data")
            except Exception as e:
                print(f"Error: {e}")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
