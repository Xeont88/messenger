from socket import *


myHost = ''
myPort = 5400

#  creating object of socket class
sockObj = socket(AF_INET, SOCK_STREAM)
#  listening of the Net
sockObj.bind((myHost, myPort))
#  no more than 5 messages in the queue
sockObj.listen(5)


while True:
    print('ready')
    connection, address = sockObj.accept()
    print('connected by', address)
    bin_data = connection.recv(1024)
    str_data = bin_data.decode('utf-8')
    print(str_data)

    # making answer
    str_answer = 'I\'ve got ' + str(len(bin_data)) + ' bytes'
    # sending answer to client
    connection.send(str_answer.encode('utf-8'))
    # close connection
    connection.close()

    # ...and wait for next one
