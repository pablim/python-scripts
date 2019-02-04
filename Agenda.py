from tkinter import *

def show_entry_fields():
    print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))


master = Tk()
Label(master, text="Login").grid(row=0)
Label(master, text="Senha").grid(row=2)

e1 = Entry(master)
e2 = Entry(master)

e1.grid(row=1)
e2.grid(row=3)


Button(master, text='Entrar', command=show_entry_fields).grid(
        row=4, sticky=W, pady=4
    )


mainloop( )
