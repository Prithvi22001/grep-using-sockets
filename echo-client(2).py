from socket import *

serverName = 'localhost'
serverPort = 50008
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

sentence = input("Input lowercase sentence:")
clientSocket.sendall(sentence.encode())
finish=True

while finish:    
  data = clientSocket.recv(1024).decode()
  if not data: 
    print("in while")
    break
  print ("From Server:", data)
  if data.find('END!!') !=-1:
    finish=False

print("out")
clientSocket.close()
