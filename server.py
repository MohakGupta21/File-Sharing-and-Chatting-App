import socket
from threading import Thread
from tkinter import messagebox
from threading import Thread
from tqdm import tqdm
from os import path
from time import sleep
from random import uniform
from tkinter import*

class main_window():
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096
    SERVER_PORT = 33000

    def sethost(self, str):
        self.SERVER_HOST = str

    def gethost(self):
        return self.SERVER_HOST

    def connect(self):
        self.r=Tk()
        astr=StringVar()
        astr=""
        bstr=IntVar()
        bstr='33000'
        l=Label(self.r,text="This is Server,Port Number =33000")
        l.grid(row=0,column=0,columnspan=2)
        l2=Label(self.r,text="Enter Host Name:")
        l2.grid(row=1,column=0)
        self.e2=Entry(self.r,textvariable=astr)
        self.e2.grid(row=1,column=1)

        okButton=Button(self.r,text="OK",command=self.s_connect)
        okButton.grid(row=3,column=1)
        self.r.mainloop()

    def s_connect(self):
        self.sethost(self.e2.get())
        s = socket.socket()
        s.bind((self.gethost(), self.SERVER_PORT))
        s.listen(5)

        self.client_socket, address = s.accept()
        messagebox.showinfo(f"{address}" + "is connected")
        self.msg_list.insert(END, "Welcome to the Chatting and File Sharing app!")
        receive_thread = Thread(target=self.receive)
        receive_thread.start()


    def send_file(self,filename):
        host = self.gethost()
        port = 5001
        s2 = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        s2.connect((host, port))
        print("[+] Connected.")

        filesize = path.getsize(filename)

        s2.send(f"{filename}{SEPARATOR}{filesize}".encode())
        f = open(filename, "rb")
        while 1:
            bytes_read = f.read(self.BUFFER_SIZE)
            if not bytes_read:
                break

            s2.sendall(bytes_read)
        messagebox.showinfo("File Sent!")
        s2.close()

    def ok(self):
        a = Tk()
        str = StringVar()
        l = Label(a, text="Enter File name:")
        l.grid(row=0, column=0)
        filename = str.get()
        e = Entry(a, textvariable=filename)
        e.grid(row=0, column=1)
        b = Button(a, text="OK",command=lambda :self.send_file(e.get()))
        b.grid(row=0, column=2)
        a.mainloop()

    def receive_file(self):
        host = self.gethost()
        port = 5001
        s3 = socket.socket()
        s3.bind((host, port))
        s3.listen(5)
        print(f"[*] Listening as {host}:{port}")
        client_socket, address = s3.accept()
        print(f"[+] {address} is connected.")

        received = client_socket.recv(self.BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)

        filename = path.basename(filename)
        filesize = int(filesize)

        f = open(filename, "wb")
        while 1:
            bytes_read = client_socket.recv(self.BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)

        messagebox.showinfo("File Received!")
        client_socket.close()
        s3.close()

    def receive(self):
        while True:
               try:
                  msg = self.client_socket.recv(1024).decode("utf8")
                  self.msg_list.insert(END,"Client: "+ msg)
               except OSError:  # Possibly client has left the chat.
                    break

    def send(self):
        display_mess = self.my_msg.get()
        self.my_msg.set("")
        mess = bytes(display_mess, "utf-8")
        self.client_socket.send(mess)
        self.msg_list.insert(END, "You: "+display_mess)

    def Exit(self):
        self.root.quit()
        exit(1)

    def init(self):
        self.root=Tk()
        self.root.title("Server")
        self.root.geometry('400x420')
        self.messages_frame = Frame(self.root,padx=10,pady=10)
        self.my_msg = StringVar()  # For the messages to be sent.
        self.my_msg.set("Type your messages here.")
        scrollbar = Scrollbar(self.messages_frame)
        self.msg_list = Listbox(self.messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.msg_list.pack(side=LEFT, fill=BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()

        entry_field = Entry(self.root, textvariable=self.my_msg)
        entry_field.bind("<Return>", self.send)
        entry_field.pack()

        send_button = Button(self.root, text="Send", command=self.send)
        send_button.pack()

        mybutton=Button(self.root,text="Connect",command=self.connect)
        mybutton.pack(side='bottom')

        button2=Button(self.root,text="Choose File",command=self.ok)
        button2.pack()
        button3=Button(self.root,text="Receive File",command=self.receive_file)
        button3.pack()
        button4=Button(self.root,text="Exit",command=self.Exit)
        button4.pack(side='bottom')

        self.root.mainloop()

if __name__ == "__main__":
    app=main_window()
    app.init()
