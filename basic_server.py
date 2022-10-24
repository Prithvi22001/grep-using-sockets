#!/usr/bin/env python3
'''
Basic Server will create a server socket and serve only one client at a time.
Class Server -> __init__() Will initialize server socket parameters and logging parameters
                start() Will start the server,listen to client query and serve client
                
main() -> Main method creates a server object and will exit the script if an error occurs or for a KeyboardInterrupt

'''
import socket
import sys
from utilities import extract_words  #Method to extract words from queries
from get_word_list import make_wordlist_file #Method to make wordlist.txt file if it is not present
import time

#The class template is borrowed from Homework 4 echoserver_better.py all modifications are done by me
class Server():

    def __init__(self, server_host, server_port):
        '''
        server_host : Hostname for server
        server_port : Port for server
        
        '''
        #Initializing server parameters
        self.server_host = server_host
        self.server_port = server_port
        self.server_backlog = 1 #Only one client
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.server_host, self.server_port))
            server_sock.listen(self.server_backlog)
            print (f"Server running on : {self.server_host},{self.server_port}")

        #Incase of error the script would terminate       
        except OSError as e:
            print ('Unable to open socket: ', e)
            if server_sock:
                server_sock.close()
            sys.exit(1)

        #Wait for client connection
        while True :

            # Client has connected
            client_conn, client_addr = server_sock.accept()
            print ('Client has connected with address: ', client_addr)

            #Receive client query and set response to the client
            while True:
                query= client_conn.recv(1024)
            
                if not query: break
                response= extract_words(query.decode())
                
                #Wait for 5 seconds
                time.sleep(5)
                
                #Send response to client and "END!!" to indicate end of response 
                client_conn.sendall(response.encode())
                client_conn.send("END!!".encode())
                break


            #Close client connection since client can send only one query
            client_conn.close()


        
def main():

    #Server socket parameters
    server_host = 'localhost'
    server_port = 50008

    # Parse command line parameters if any
    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    # Create Server object
    server = Server(server_host, server_port)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
    except Exception as e:
        print(f"Other exception {e}")

