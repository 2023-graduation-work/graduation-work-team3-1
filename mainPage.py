import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkcalendar import Calendar

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        master.geometry("700x500")
        master.title("Hello Tkinter")
        self.create_widgets()

    def create_widgets(self):
        # テキストボックスを作成
        text = ScrolledText(self, font=("", 15), height=10, width=40)
        text.grid(row=1, column=1, padx=20, pady=100)

        # カレンダーウィジェットを作成
        cal = Calendar(self, selectmode="day")
        cal.grid(row=1, column=0, padx=20, pady=100)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()

