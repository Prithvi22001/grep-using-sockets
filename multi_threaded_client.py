#!/usr/bin/env python3

import socket
import sys
from pprint import pprint

class Client():

    def __init__(self, server_host, server_port):
        self.start(server_host, server_port)

    def start(self, server_host, server_port):

        # Try to connect to echo server
        try:
            client_sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
            print(f"Connecting to server {server_host},{server_port}")

            client_sock.connect((server_host, server_port))
        except OSError as e:
            print ('Unable to connect to socket: ', e)
            if client_sock:
                client_sock.close()
            sys.exit(1)

        finish_queries=True
        while finish_queries:
            query=input("Enter query (multiple queries can be separated by , to end type ;): ")
            if query==';':
                break
            elif query.find(';')!=-1:
                query=query[:-1]
                finish_queries=False
                
            client_sock.sendall(query.encode())

            # Get response data from server and print it
            finish=True
            answer=[]
            while finish:    
                data = client_sock.recv(1024).decode()
                #print(f"recev {data}")
                if not data: 
                    break
                # print ("From Server:", data)
                # print(data)
                # break
                answer.extend(data.split())
                if data.find('END!!') !=-1:
                    pprint(answer[:-1])
                    answer=[]
                    finish=False
                if data.find(':') !=-1:
                    pprint(answer[:-1])
                    answer=[]
        client_sock.close()
def main():

    # Echo server socket parameters
    server_host = 'localhost'
    server_port = 50008

    # Parse command line parameters if any
    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    # Create EchoClient object
    client = Client(server_host, server_port)

if __name__ == '__main__':
    main()
