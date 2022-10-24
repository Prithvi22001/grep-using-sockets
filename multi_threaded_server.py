#!/usr/bin/env python3
'''
Multithreaded Server will create a server socket and for each client connection it will spawn a new thread to serve that client
Class Server -> __init__() Will initialize server socket parameters and logging parameters
                start() Will initialize and start the new thread for each client connection 
                server_content() Will receive client queries and send responses until client terminates the connection

main() -> Main method creates a server object and will exit the script if an error occurs or for a KeyboardInterrupt

'''
import socket
import sys
import threading
import os
import time
from utilities import extract_words #Method to extract words from worlist.txt given the client query
import plogger,logging

#The class template is borrowed from Homework 4 echoserver_better.py all modifications are done by me
class Server():

    def __init__(self, server_host, server_port,logging_level=10):
        '''
        server_host : Hostname for server
        server_port : Port for server
        logging_level : Sets the logging level higher logging level will only log different levels of logs more info can be found on logging library from the documentaion
        
        '''
        #Initializing server parameters
        self.server_host = server_host
        self.server_port = server_port
        self.server_backlog = 1

        #Setting up logger parameters
        self.logger=plogger.logger("server",level=logging_level)
        ch = logging.StreamHandler()
        format = "%(funcName)s | %(levelname)s | %(message)s   (%(filename)s:%(lineno)d)"
        ch.setFormatter(plogger.CustomFormatter(format))
        self.logger.handlers.pop()
        self.logger.addHandler(ch)

        self.start() 

    def start(self):

        #Initialize server socket on which to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creating TCP socket for server
            server_sock.bind((self.server_host, self.server_port))
            server_sock.listen(self.server_backlog)
            
            self.logger.info(f"Server running on : {self.server_host},{self.server_port}")
        
        #Incase of error the script would terminate
        except OSError as e:
            self.logger.error(f'Unable to open socket: {e}')
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Wait for client connection
        while True:

            # Client has connected
            [client_conn, client_addr] = server_sock.accept()
            self.logger.info(f'Client has connected with address: {client_addr}')

            # Create thread to serve client
            thread = threading.Thread(
                    target = self.serve_content,
                    args = (client_conn, client_addr))
            thread.daemon = True
            thread.start()
        
    def serve_content(self, client_conn, client_addr):

        self.logger.debug(f'{threading.current_thread().name} Serving content to client with address {client_addr}')

        #Keep receiving data from client until client terminates the connection by putting ; in query
        finish=True
        while finish:
            query = client_conn.recv(1024).decode()
            self.logger.debug(f'{threading.current_thread().name} got query {query}')
            if not query: break
            if query.find(";")!=-1:
                finish=False

            #Get words that match the query pattern
            response=extract_words(query.split(',') if ','in query else query)

            #Wait for 5 seconds
            time.sleep(5)

            #Send response to client 
            if type(response)==dict:
                #For multiple queries,sending each response separated by :
                for que,res in response.items():
                    client_conn.sendall(f"{res} :".encode())
            else:
                client_conn.sendall(response.encode())        

            #Send END!! to indicate end of response to client
            client_conn.send("END!!".encode())

        # Close connection to client
        client_conn.close()

def main():

    #Server socket parameters
    server_host = 'localhost'
    server_port = 50008

    #Parse command line parameters if any
    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    #Create Server object
    server = Server(server_host, server_port)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
    except Exception as e:
        print("Other exception"+str(e))

