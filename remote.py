#!/usr/bin/env python3
"""
remote.py - A remote shell server

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

import socket
import threading
import subprocess
import sys
import os
import signal


class RemoteShellServer:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        
    def start_server(self):
        """Start the remote shell server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            print(f"Remote shell server listening on {self.host}:{self.port}")
            print("Waiting for connections...")
            print("Press Ctrl+C to stop the server")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Connection from {client_address[0]}:{client_address[1]}")
                    
                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"Socket error: {e}")
                        
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.stop_server()
        except Exception as e:
            print(f"Server error: {e}")
            self.stop_server()
    
    def handle_client(self, client_socket, client_address):
        """Handle a client connection and provide remote shell"""
        try:
            # Send welcome message
            welcome_msg = f"Remote Shell Server - Connected from {client_address[0]}:{client_address[1]}\n"
            welcome_msg += "Type 'exit' to disconnect\n"
            welcome_msg += "=" * 50 + "\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            while True:
                # Send prompt
                prompt = f"{os.getcwd()}$ "
                client_socket.send(prompt.encode('utf-8'))
                
                # Receive command
                command = client_socket.recv(4096).decode('utf-8').strip()
                
                if not command:
                    break
                    
                # Handle exit command
                if command.lower() in ['exit', 'quit']:
                    client_socket.send("Goodbye!\n".encode('utf-8'))
                    break
                
                # Execute command
                try:
                    # Change to home directory for cd commands
                    if command.startswith('cd '):
                        new_dir = command[3:].strip()
                        if new_dir:
                            try:
                                os.chdir(new_dir)
                                result = f"Changed directory to: {os.getcwd()}\n"
                            except OSError as e:
                                result = f"Error changing directory: {e}\n"
                        else:
                            os.chdir(os.path.expanduser('~'))
                            result = f"Changed directory to: {os.getcwd()}\n"
                    else:
                        # Execute other commands
                        process = subprocess.Popen(
                            command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            cwd=os.getcwd()
                        )
                        
                        # Get output
                        output, _ = process.communicate()
                        result = output if output else f"Command executed (exit code: {process.returncode})\n"
                    
                    # Send result to client
                    client_socket.send(result.encode('utf-8'))
                    
                except Exception as e:
                    error_msg = f"Error executing command: {e}\n"
                    client_socket.send(error_msg.encode('utf-8'))
                    
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            print(f"Client {client_address[0]}:{client_address[1]} disconnected")
    
    def stop_server(self):
        """Stop the server and cleanup"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Server stopped")


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nReceived interrupt signal")
    sys.exit(0)


def main():
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create and start the server
    server = RemoteShellServer()
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
