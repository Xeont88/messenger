from tkinter import *

name = "Ruslan Sonkin"


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
    text.config(state=NORMAL)
    msg = name + ':\n     ' + entry.get() + '\n\n'
    # text.highlight_pattern(name, "red")
    text.insert(END, msg)
    text.config(state=DISABLED)
    entry.delete(0, END)


root = Tk()
root.geometry('275x400+200+200')
root.title('messenger v0.1')

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

btn1.config(state=DISABLED)
btn2.config(state=DISABLED)
btn3.config(state=DISABLED)

root.mainloop()
