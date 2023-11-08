import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkcalendar import Calendar
from tkinter import ttk
from tkinter import messagebox
from datetime import date
import sqlite3

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        master.geometry("600x300")
        master.title("日記アプリ")
        master.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        def update_selected_date():
            selected_date = self.cal.get_date()
            selected_date_label.config(text=f"{selected_date}の日記")

        self.today = date.today()
        selected_date_label = tk.Label(self, text=f"{self.today}の日記", font=("", 12))
        selected_date_label.grid(row=0, column=0, padx=(350, 0), pady=5, sticky='w')

        weather_options = ["晴れ", "曇り", "雨", "雪"]
        self.selected_weather = tk.StringVar()
        weather_combobox = ttk.Combobox(self, textvariable=self.selected_weather, values=weather_options, width=25)
        weather_combobox.grid(row=1, column=0, padx=(300, 0), pady=5)
        weather_combobox.set(weather_options[0])

        weather_label = tk.Label(self, text="今日の天気:")
        weather_label.grid(row=1, column=0, padx=(0, 0), pady=5)

        self.text = ScrolledText(self, font=("", 15), height=7, width=30)
        self.text.grid(row=4, column=0, padx=(250, 0), pady=10, sticky='w')

        self.cal = Calendar(self, selectmode="day", showweeknumbers=False)
        self.cal.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.cal.bind("<<CalendarSelected>>", lambda event: update_selected_date())

        weather_label = tk.Label(self, text="今日の充実度:")
        weather_label.grid(row=2, column=0, padx=(0, 0), pady=0)

        self.scale_var = tk.DoubleVar()
        scaleH = tk.Scale(self, variable=self.scale_var, orient=tk.HORIZONTAL, length=180, from_=1, to=100)
        scaleH.grid(row=2, column=0, padx=(300, 0), pady=0)

        self.actions = ["出社", "テレワーク", "外回り", "出張", "休日"]
        self.var = tk.IntVar()
        action_frame = ttk.Frame(self)
        action_frame.grid(row=3, column=0, padx=(250, 0), pady=0)
        for i, action in enumerate(self.actions):
            rdo = ttk.Radiobutton(action_frame, text=action, variable=self.var, value=i)
            rdo.grid(row=0, column=i, padx=5, pady=0)

        save_button = tk.Button(self, text="保存", command=self.save_entry)
        save_button.grid(row=0, column=0, padx=(0, 40), pady=5, sticky='e')

    def save_entry(self):
        today = self.cal.get_date()
        weather = self.selected_weather.get()
        enrichment = self.scale_var.get()
        action = self.actions[self.var.get()]
        diary_text = self.text.get("1.0", tk.END)
        self.insert_data(today, diary_text, weather, enrichment, action)

    def insert_data(self, today, textbox, weather, enrichment, action):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        try:
            create_table_sql = "CREATE TABLE IF NOT EXISTS diary (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, textbox TEXT, weather TEXT, enrichment INTEGER, action TEXT)"
            cur.execute(create_table_sql)
            conn.commit()

            sql_statement = "INSERT INTO diary (date, textbox, weather, enrichment, action) VALUES (?,?,?,?,?)"
            cur.execute(sql_statement, (today, textbox, weather, enrichment, action))
            conn.commit()
            messagebox.showinfo("Success", "データが正常に挿入されました.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()
