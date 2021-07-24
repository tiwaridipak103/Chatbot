from tkinter import *

from function import  greeting_response , bot_responce
root = Tk()
exit = ['see you later' , 'bye' , 'quiet' , 'next time']
def send():
    send  = "You : " + e.get()
    txt.insert(END , "\n" + send)
    if e.get() in exit:
        txt.insert(END , "\n" + 'Bot : See you later')

    else :
        if   greeting_response(e.get()) != None:
            txt.insert(END , "\n" + 'Bot : '+ greeting_response(e.get()))
        else:
            txt.insert(END , "\n" + 'Bot : Wait a minute.')
            txt.insert(END , "\n" + 'Bot : '+ bot_responce(e.get()))
          
    e.delete(0, END)
txt = Text(root)
txt.grid(row=0 , column = 0 ,columnspan= 2 )
txt.insert(END , "\n" + 'Bot : Hi , How can i help you ? ')
e = Entry(root ,width = 100)
send = Button(root , text = 'send' ,command =send ).grid(row=1 , column = 1)
e.grid(row=1 , column = 0)
root.title('Welcome To Chatbot')
root.mainloop()