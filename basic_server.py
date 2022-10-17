#!/usr/bin/env python3

from datetime import datetime
import socket
import sys
import threading
from utilities import extract_words  #Module to extract words from queries
import time

class Server():

    def __init__(self, server_host, server_port):

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
        except OSError as e:
            print ('Unable to open socket: ', e)
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Wait for client connection
        # end_time=datetime.datetime.now()+datetime.timedelta(seconds=600)
        # print(end_time)
        while True :#and not(datetime.datetime.now()>end_time):

        # Client has connected
        
            client_conn, client_addr = server_sock.accept()
            print ('Client has connected with address: ', client_addr)

            while True:
                query= client_conn.recv(1024)
                # print(query)
                if not query: break
                response= extract_words(query.decode())
                time.sleep(5)
                client_conn.sendall(response.encode())
                client_conn.send("END!!".encode())
                break
                # print(response.split()[-1])
            print("done sending")
            client_conn.close()


        # if client_conn:
        #     print(f"closing connecetion")
        #     client_conn.close()
        #     server_sock.close()
        #     sys.exit(1)
            # # Create thread to serve client
            # thread = threading.Thread(
            #         target = self.serve_content,
            #         args = (client_conn, client_addr))
            # thread.daemon = True
            # thread.start()

        # server_sock.close()

    # def serve_content(self, client_conn, client_addr):

    #     print ('Serving content to client with address', client_addr)

    #     # Receive data from client
    #     bin_data = client_conn.recv(1024)

    #     # Echo back received data to client
    #     client_conn.sendall(bin_data)

    #     # Print data from client
    #     print ('Server received', bin_data)

        # Close connection to client

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
    except Exception as e:
        print(f"Other exception {e}")

