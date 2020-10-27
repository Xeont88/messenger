#  messenger.py     R.R.Sonkin 22.10.2020
#  клиент для сетевого варианта приложения для быстрого обмена сообщениями
#  часть 0.1 - интерфейс
#  часть 0.2 - + история сообщений
#  часть 0.3 - server

from tkinter import *
import time

import threading
from socket import *

ver = '0.3 (server)'
name = "Ruslan Sonkin"
last_date = 0
server_address = ('localhost', 5400)
main_tau = 20  # время цикла главной программы в мс
# server_address = ('192.168.0.1', 5400)
locserv_addr = ('', 5401)
mode = 'disconnect'
lst_in = []
busy_in = 0  # queue business


def tools_window_f():
    tools_window = Toplevel()
    tools_window.title('tools')


def options_window_f():
    options_window = Toplevel()
    options_window.title('options')


def clear_history():
    text.config(state=NORMAL)
    text.delete(0.0, END)
    text.config(state=DISABLED)


# def highlight_pattern(self, pattern, tag, start="1.0", end="end",
#                          regexp=False):
#        '''Apply the given tag to all text that matches the given pattern
#
#        If 'regexp' is set to True, pattern will be treated as a regular
#        expression according to Tcl's regular expression syntax.
#        '''
#
#        start = index(start)
#        end = index(end)
#        mark_set("matchStart", start)
#        mark_set("matchEnd", start)
#        mark_set("searchLimit", end)
#
#        count = IntVar()
#        while True:
#            index = self.search(pattern, "matchEnd","searchLimit",
#                                count=count, regexp=regexp)
#            if index == "": break
#            if count.get() == 0: break # degenerate pattern which matches zero-length strings
#            self.mark_set("matchStart", index)
#            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
#            self.tag_add(tag, "matchStart", "matchEnd")


def send_msg(event):
    msg = entry.get()

    client = socket(AF_INET, SOCK_STREAM)
    bin_msg = bytes(msg, 'utf-8')

    try:
        client.connect(server_address)
        client.sendall(bin_msg)
        print('sending', bin_msg)
        res = ''
    except:
        res = 'Сервер выключен'
        pass
    finally:
        client.close()
    return res


def put_msg(msg):
    global lst_in
    global busy_in
    while busy_in:
        time.sleep(0.001)
    busy_in = 1
    lst_in.append(msg)
    busy_in = 0


def work_in():
    global lst_in
    global busy_in
    lock_sock = socket(AF_INET, SOCK_STREAM)
    lock_sock.bind(locserv_addr)
    lock_sock.listen(5)

    while True:
        # waiting for message from server
        connection, address = lock_sock.accept()
        bin_data = connection.recv(1024)
        str_data = bin_data.decode('utf-8')
        connection.close()

        put_msg(str_data)

        time.sleep(0.001)


# message receive flow
tr_in = threading.Thread(target=work_in)
tr_in.daemon = True
tr_in.start()


def disp_msg(msg):
    global last_date
    text.config(state=NORMAL)
    # print(time.ctime())

    date = time.strftime('%d.%m.%y', time.localtime())
    t = time.strftime('%X', time.localtime())
    print(msg)
    if msg:
        msg = name + '\n'
        if last_date != date:
            msg += date + ' '
            last_date = date
        msg += t + ':\n' + entry.get() + '\n\n'
        # text.highlight_pattern(name, "red")
        text.insert(END, msg)
        text.config(state=DISABLED)
        entry.delete(0, END)

        save_history()


def save_history():
    t = open('history.txt', 'w')
    data = text.get(0.0, END)
    t.write(data)


def load_saved_msgs():
    t = open('history.txt', 'r')
    data = t.read()
    text.config(state=NORMAL)
    text.insert(END, data)
    text.config(state=DISABLED)


root = Tk()
root.geometry('275x400+200+200')
root.title('messenger ' + ver)

menu = Menu(root)
root.config(menu=menu)

fileMenu = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=fileMenu)

fileMenu.add_command(label='Очистка истории сообщений', command=clear_history)
fileMenu.add_command(label='Выход', command=exit)
menu.add_command(label='Tools', command=tools_window_f)
menu.add_command(label='Options', command=options_window_f)

frame_text = Frame(root, )
frame_text.place(x=5, y=5, relwidth=1, relheight=1, width=-5, height=-30)
text = Text(frame_text)
text.place(x=0, y=0, relwidth=1, relheight=1, width=-55, height=0)

btn1 = Button(frame_text, text=1, width=7, height=3)
btn1.pack(anchor=NE, pady=5)
btn2 = Button(frame_text, text=2, width=7, height=3)
btn2.pack(anchor=NE, pady=5)
btn3 = Button(frame_text, text=3, width=7, height=3)
btn3.pack(anchor=NE, pady=5)

frame_entry = Frame(root, )
frame_entry.pack(side=BOTTOM, fill=X)

entry = Entry(frame_entry)
entry.pack(side=LEFT, fill=X, expand=1)

btn = Button(frame_entry, text='send', command=lambda: send_msg(0))
btn.pack(side=RIGHT, padx=5)

entry.bind('<Return>', send_msg)

load_saved_msgs()

btn1.config(state=DISABLED)
btn2.config(state=DISABLED)
btn3.config(state=DISABLED)


def main():
    global lst_in
    global busy_in
    global mode

    if len(lst_in) > 0:
        while busy_in:
            time.sleep(0.001)
        busy_in = 1
        str_in = lst_in.pop(0)
        busy_in = 0
        disp_msg(str_in)

    root.after(main_tau, main)


main()

root.mainloop()
