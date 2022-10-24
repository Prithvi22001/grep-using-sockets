#!/usr/bin/env python3
'''
Multithreaded client can send multiple queries to server and get response for each query.
Class Client  -> __init__() Will initialize the server parameter to connect to server and set logging parameters.
                start() Will create a client socket and connect to server,it will send queries to server until ; is type in query

                For example : Client can sent queries in following format :  
                -a*z (Will send a*z query and get response connection to server will still be open)
                -a*z,b*z (Will send a*z and b*z query and get responses for both queries connection to server will still be open)
                -a*z; (Will send a*z query and get response connection to server will be closed)
                -; (Will close connection to server)

main() -> Main method creates a client object and will exit the script if an error occurs or for a KeyboardInterrupt
'''

import socket
import sys
import plogger,logging

#The class template is borrowed from Homework 4 echoclient_better.py all modifications are done by me
class Client():

    def __init__(self, server_host, server_port,logging_level=10):
        '''
        server_host : Hostname for server
        server_port : Port for server
        logging_level : Sets the logging level higher logging level will only log different levels of logs more info can be found on logging library from the documentaion

        '''
        #Setting up logger parameters
        self.logger=plogger.logger("client",level=logging_level)
        ch = logging.StreamHandler()
        format = "%(funcName)s | %(levelname)s | %(message)s   (%(filename)s:%(lineno)d)"
        ch.setFormatter(plogger.CustomFormatter(format))
        self.logger.handlers.pop()
        self.logger.addHandler(ch)
        
        self.start(server_host, server_port)

    def start(self, server_host, server_port):

        # Try to connect to Server
        try:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.logger.info(f"Connecting to server {server_host},{server_port}")

            client_sock.connect((server_host, server_port))
        
        #Incase of error the script would terminate       
        except OSError as e:
            self.logger.error (f'Unable to connect to socket: {e}')
            if client_sock:
                client_sock.close()
            sys.exit(1)

        #Accept queries from client and send it to server
        finish_queries=True
        while finish_queries:
            query=input("Enter query (multiple queries can be separated by , to end type ;): ")
            
            #Terminate if ; in query
            if query==';':
                break
            elif query.find(';')!=-1:
                query=query[:-1]
                finish_queries=False
                
            #Send query to client
            client_sock.sendall(query.encode())

            # Get response data from server and print it
            finish=True
            answer=""
            while finish:    
                data = client_sock.recv(1024).decode()
                if not data: 
                    break                
                answer+=data
                if data.find('END!!') !=-1:
                    finish=False
            _=[print(f"{que} --> {res.split()}") for que,res in zip(query.split(','),answer.split('END!!')[:-1][0].split(':'))]


        #Close client socket
        client_sock.close()

def main():

    #Server socket parameters
    server_host = 'localhost'
    server_port = 50008

    # Parse command line parameters if any
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