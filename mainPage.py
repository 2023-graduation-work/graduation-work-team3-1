import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=200, height=350)
        self.pack()
        master.geometry("900x700")
        master.title("日記アプリ")
        self.create_widget()

    def create_widget(self):
        self.label1 = tk.Label(self, text='Sample', relief="raised", borderwidth=4)
        self.label1.pack()
        
if __name__=='__main__':
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()
        