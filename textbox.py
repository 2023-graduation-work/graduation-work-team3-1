import tkinter as tk
from tkinter.scrolledtext import ScrolledText
class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=200, height=350)
        self.pack()
        master.geometry("900x700")
        master.title("Hello Tkinter")
        self.create_widget()

    def create_widget(self):
        text = ScrolledText(root, font=("", 15), height=10, width=40)
        text.place(relx=1.0, rely=1.0, anchor="se")
        text.pack()
        
if __name__=='__main__':
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()
        