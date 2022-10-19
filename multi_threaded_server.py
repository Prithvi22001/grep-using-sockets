#!/usr/bin/env python3
#
# COMP 332, Fall 2018
# Wesleyan University
#
# Simple multi-threaded echo server that echos back whatever is sent to it
#
# Usage:
#   python3 echo_server.py <server_host> <server_port>
#

import json
import socket
import sys
import threading
from time import sleep
from urllib import response
from utilities import extract_words

class Server():

    def __init__(self, server_host, server_port):

        self.server_host = server_host
        self.server_port = server_port
        self.server_backlog = 1
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            server_sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.server_host, self.server_port))
            server_sock.listen(self.server_backlog)
            print (f"Server running on : {self.server_host},{self.server_port}")
        except OSError as e:
            print ('Unable to open socket: ', e)
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Wait for client connection
        client_number=0
        while True:

            # Client has connected
        
            [client_conn, client_addr] = server_sock.accept()
            print ('Client has connected with address: ', client_addr)

            # Create thread to serve client
            thread = threading.Thread(
                    target = self.serve_content,
                    name=client_number,
                    args = (client_conn, client_addr))
            #self.thread_number=thread.name
            #client_number+=1        
            thread.daemon = True
            thread.start()
        


    def serve_content(self, client_conn, client_addr):

        print (f'{threading.current_thread().name} Serving content to client with address {client_addr}')

        # Receive data from client
        finish=True
        while finish:
            query = client_conn.recv(1024).decode()
            print(f"reecevied {query}")
            if not query: break
            if query.find(";")!=-1:
                finish=False
            
            response=extract_words(query.split(',') if ','in query else query)

            # sleep(5)
            if type(response)==dict:
                for que,res in response.items():
                    #print(f"{que}: {res}")
                    #print('~~~~~~')
                    #print(f"{que}: {res}".encode())
                    client_conn.sendall(f"{res}".encode())
                    client_conn.send(":".encode())
            else:
                client_conn.sendall(response.encode())        


            client_conn.send("END!!".encode())

        # Close connection to client
        client_conn.close()

def main():

    # Echo server socket parameters
    server_host = 'localhost'
    server_port = 50008

    # Parse command line parameters if any
    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    # Create EchoServer object
    server = Server(server_host, server_port)

if __name__ == '__main__':
    try:
        main()
    # except KeyboardInterrupt:
    #     print("Shutting down")
    except Exception:
        print("Other exception")

