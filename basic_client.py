#!/usr/bin/env python3
'''
Basic client can send one query to server and get response and terminate.
Class Client  -> __init__() Will initialize the server parameter to connect to server 
                start() Will create a client socket and connect to server,it will one query to server 

main() -> Main method creates a client object and will exit the script if an error occurs or for a KeyboardInterrupt
'''

import socket
import sys

#The class template is borrowed from Homework 4 echoclient_better.py all modifications are done by me
class Client():
    
    def __init__(self, server_host, server_port):
        '''
        server_host : Hostname for server
        server_port : Port for server
        
        '''

        self.start(server_host, server_port)

    def start(self, server_host, server_port):

        # Try to connect to echo server
        try:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Connecting to server {server_host},{server_port}")

            client_sock.connect((server_host, server_port))

        #Incase of error the script would terminate       
        except OSError as e:
            print ('Unable to connect to socket: ', e)
            if client_sock:
                client_sock.close()
            sys.exit(1)

        query=input("Enter query : ")
        client_sock.sendall(query.encode())

        # Get response data from server and print it
        finish=True
        answer=[]
        while finish:    
            data = client_sock.recv(1024).decode()
            if not data: 
                break
            answer.extend(data.split())
            if data.find('END!!') !=-1:
                finish=False

        #Close client socket
        client_sock.close()
        print(answer[:-1])

def main():

    #Server socket parameters
    server_host = 'localhost'
    server_port = 50008

    #Parse command line parameters if any
    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    # Create Client object
    client = Client(server_host, server_port)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
    except Exception as e:
        print(f"Other exception {e}")
