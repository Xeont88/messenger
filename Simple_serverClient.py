from socket import *

# server address, first connection with server on this comp (localhost)
server_address = ('localhost', 5400)

while True:
    #  waiting for message
    msg = input(': ')
    bin_msg = bytes(msg, 'utf-8')

    client = socket(AF_INET, SOCK_STREAM)

    try:
        client.connect(server_address)
        client.sendall(bin_msg)
        # waiting for answer
        data = client.recv(1024)
        print('Server answer:', data.decode('utf-8'))
    except:
        print('not connected')

    finally:
        client.close()





