from socket import *

play_table = []             # users list [name, ip, ch]


def send_to_all(msg):
    for el in play_table:
        ip_el = el[1]
        res = send_answ(ip_el, msg)
    pass


def send_answ(ip, msg):
    client = socket(AF_INET, SOCK_STREAM)
    bin_msg = bytes(msg, 'utf-8')

    try:
        client.connect((ip, 5401))
        client.send(bin_msg)
        res = 'OK'
    except:
        res = 'not connected'
    finally:
        client.close()
    return res


# TODO: сохранение сообщений в тхт док.


myHost = ''
myPort = 5400       # servers port

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

    # making answer
    str_answer = 'I\'ve got ' + str(len(bin_data)) + ' bytes'
    # sending answer to client
    connection.send(str_answer.encode('utf-8'))
    # close connection
    connection.close()

    ip_client = address[0]

    lst_data = str_data.split('|')
    command = lst_data[0]
    # print('command =', command)
    try:
        param = lst_data[1]
    except:
        param = ''
    print('command =', command + ', param =', param)

    send_to_all(command + param)


