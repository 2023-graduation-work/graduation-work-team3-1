import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkcalendar import Calendar
from datetime import date
from tkinter import messagebox
import sqlite3

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        master.geometry("700x400")
        master.title("Hello Tkinter")
        self.create_widgets()

    def create_widgets(self):
        def update_selected_date():
            selected_date = cal.get_date()
            selected_date_label.config(text=f"{selected_date}の日記")

        
        #保存する値を取ってくる
        def save_entry():
            today = cal.get_date()
            weather = selected_weather.get()
            enrichment = scale_var.get()
            action = actions[self.var.get()]
            diary_text = text.get("1.0", tk.END)
            self.insert_data(today, diary_text, weather, enrichment, action)
        #メニューバー
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        setting_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='操作', menu=setting_menu)
        setting_menu.add_command(label='削除')
        setting_menu.add_command(label='検索')

        
        
        today = date.today()
        selected_date_label = tk.Label(self, text=f"{today}の日記", font=("", 12))
        selected_date_label.grid(row=0, column=0, padx=(350, 0), pady=10, sticky='w')
        #天気の処理
        weather_options = ["晴れ", "曇り", "雨", "雪"]
        selected_weather = tk.StringVar()
        weather_combobox = ttk.Combobox(self, textvariable=selected_weather, values=weather_options, width=25)
        weather_combobox.grid(row=1, column=0, padx=(300, 0), pady=10)
        weather_combobox.set(weather_options[0])

        weather_label = tk.Label(self, text="今日の天気:")
        weather_label.grid(row=1, column=0, padx=(0, 0), pady=10)
        #テキストボックス
        text = ScrolledText(self, font=("", 15), height=10, width=40)
        text.grid(row=4, column=0, padx=(250, 0), pady=10, sticky='w')

        #カレンダー
        cal = Calendar(self, selectmode="day", showweeknumbers=False)
        cal.grid(row=4, column=0, padx=20, pady=10, sticky='w')
        cal.bind("<<CalendarSelected>>", lambda event: update_selected_date())

        #充実度slider
        weather_label = tk.Label(self, text="今日の充実度:")
        weather_label.grid(row=2, column=0, padx=(0, 0), pady=0)

        scale_var = tk.DoubleVar()
        scaleH = tk.Scale(self, variable=scale_var, orient=tk.HORIZONTAL, length=180, from_=0, to=100)
        scaleH.grid(row=2, column=0, padx=(300, 0), pady=0)

        #行動ラジオボタン
        actions = ["出社", "テレワーク", "外回り", "出張", "休日"]
        self.var = tk.IntVar()
        action_frame = ttk.Frame(self)
        action_frame.grid(row=3, column=0, padx=(0, 0), pady=0)
        for i, action in enumerate(actions):
            rdo = ttk.Radiobutton(action_frame, text=action, variable=self.var, value=i)
            rdo.grid(row=0, column=i, padx=5, pady=0)

        
        #保存ボタン
        save_button = tk.Button(self, text="保存", command=save_entry)
        save_button.grid(row=0, column=0, padx=(0, 100), pady=10, sticky='e')


    #INSERT処理
    def insert_data(self, today, textbox, weather, enrichment, action):
        conn = sqlite3.connect('daiaryapp.sqlite3')
        cur = conn.cursor()
        try:
            create_table_sql = "CREATE TABLE IF NOT EXISTS diary (id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,textbox TEXT,weather TEXT,enrichment INTEGER,action TEXT)"
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
   