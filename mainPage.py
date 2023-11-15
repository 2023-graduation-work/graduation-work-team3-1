import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkcalendar import Calendar
from tkinter import ttk
from tkinter import messagebox
from datetime import date
import datetime
import sqlite3
from tkinter import *
from datetime import datetime

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        master.geometry("600x300")
        master.title("日記アプリ")
        master.resizable(False, False)
        self.create_widgets()
        self.create_datebase()


        #データが入った日の色を変更
        if len(self.serect_data()) >= 1:
            for date in self.serect_data():
                d = ",".join(date)
                da=datetime.strptime(d, "%d-%m-%Y")
                self.cal.calevent_create(da,"Hello World",tags="Message")
                self.cal.tag_config("Message",background="red",foreground="white")
        else:
                messagebox.showerror("Error", "データがありません.")
            
            
    def create_widgets(self):
        #選択した日付ラベルの変更
        def update_selected_date():
            selected_date_str = self.cal.get_date()
            selected_date = datetime.strptime(selected_date_str, "%d-%m-%Y")
            d = selected_date.strftime('%Y/%m/%d')
            selected_date_label.config(text=f"{d}の日記")
        self.today = date.today()
        selected_date_label = tk.Label(self, text=f"{self.today}の日記", font=("", 12))
        selected_date_label.grid(row=0, column=0, padx=(350, 0), pady=5, sticky='w')

        #天気のコンボボックス
        weather_options = ["晴れ", "曇り", "雨", "雪"]
        self.selected_weather = tk.StringVar()
        weather_combobox = ttk.Combobox(self, textvariable=self.selected_weather, values=weather_options, width=25)
        weather_combobox.grid(row=1, column=0, padx=(300, 0), pady=5)
        weather_combobox.set(weather_options[0])

        weather_label = tk.Label(self, text="今日の天気:")
        weather_label.grid(row=1, column=0, padx=(0, 0), pady=5)

        #テキストボックス
        self.text = ScrolledText(self, font=("", 15), height=7, width=30)
        self.text.grid(row=4, column=0, padx=(250, 0), pady=10, sticky='w')

        #カレンダー生成処理
        self.cal = Calendar(self, selectmode="day", showweeknumbers=False,date_pattern="dd-mm-y")
        self.cal.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.cal.bind("<<CalendarSelected>>", lambda event: update_selected_date())

        #充実度スライダー
        weather_label = tk.Label(self, text="今日の充実度:")
        weather_label.grid(row=2, column=0, padx=(0, 0), pady=0)

        self.scale_var = tk.DoubleVar()
        scaleH = tk.Scale(self, variable=self.scale_var, orient=tk.HORIZONTAL, length=180, from_=1, to=100)
        scaleH.grid(row=2, column=0, padx=(300, 0), pady=0)
        
        #行動ラジオボタン
        self.actions = ["出社", "テレワーク", "外回り", "出張", "休日"]
        self.var = tk.IntVar()
        action_frame = ttk.Frame(self)
        action_frame.grid(row=3, column=0, padx=(250, 0), pady=0)
        for i, action in enumerate(self.actions):
            rdo = ttk.Radiobutton(action_frame, text=action, variable=self.var, value=i)
            rdo.grid(row=0, column=i, padx=5, pady=0)
            
        #メニューバー
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        setting_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='操作', menu=setting_menu)
        setting_menu.add_command(label='削除', command=self.delete_entry)
        setting_menu.add_command(label='検索', command=lambda : open_search_window())

            
        #保存ボタン
        save_button = tk.Button(self, text="保存", command=self.save_entry)
        save_button.grid(row=0, column=0, padx=(0, 40), pady=5, sticky='e')
        
        
        
        def open_search_window():
            #  command=self.perform_search
            search_window = tk.Toplevel(root)
            search_window.title("検索")
            

            search_label = tk.Label(search_window, text="キーワードを入力:")
            search_label.pack()

            search_entry = tk.Entry(search_window)
            search_entry.pack()

            search_result_text = ScrolledText(search_window, font=("", 12), height=10, width=40, state=tk.DISABLED)
            search_result_text.pack()
            
            
                
            
            def perform_search():
                    keyword = search_entry.get()
                    search_results = self.search_data(keyword)
                    search_result_text.config(state=tk.NORMAL)
                    search_result_text.delete(1.0, tk.END)
                    for result in search_results:
                        search_result_text.insert(tk.END, result)
                        search_result_text.insert(tk.END, "\n")
                    search_result_text.config(state=tk.DISABLED)
            
            search_button = tk.Button(search_window, text="検索",command= lambda : perform_search())
            search_button.pack()

    def delete_entry(self):
        today = self.cal.get_date()
        self.delete_entry_by_date(today)
        
    def delete_entry_by_date(self, today):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        try:
            sql_statement = "DELETE FROM diary WHERE date = ?;"
            cur.execute(sql_statement, (today,))
            conn.commit()
            messagebox.showinfo("Success", "データが正常に削除されました。")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))
    
    


    def get_entry_by_date(self, selected_date):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        try:
            sql_statement = "SELECT textbox, weather, enrichment, action FROM diary WHERE date = ?;"
            cur.execute(sql_statement, (selected_date,))
            row = cur.fetchone()
            conn.commit()
            if row:
                entry = {
                    'textbox': row[0],
                    'weather': row[1],
                    'enrichment': row[2],
                    'action': row[3]
                }
                return entry
            else:
                return None
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))
            
    
    
    def search_data(self, keyword):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        search_results = []
        try:
            sql_statement = "SELECT date, textbox FROM diary WHERE textbox LIKE ?;"
            cur.execute(sql_statement, (f"%{keyword}%",))
            rows = cur.fetchall()
            for row in rows:
                search_results.append(f"{row[0]}:\n{row[1]}")
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))
        return  search_results
    
        #保存した値を取ってくる
    def save_entry(self):
        today = self.cal.get_date()
        print("取ってきた値today"+today)
        dt = datetime.strptime(today, "%d-%m-%Y")
        weather = self.selected_weather.get()
        enrichment = self.scale_var.get()
        action = self.actions[self.var.get()]
        diary_text = self.text.get("1.0", tk.END)
        self.insert_up_data(today, diary_text, weather, enrichment, action)
        
        self.cal.calevent_create(dt,"Hello World",tags="Message")
        self.cal.tag_config("Message",background="red",foreground="white")
        
    def create_datebase(self):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        try:
            create_table_sql = "CREATE TABLE IF NOT EXISTS diary (date TEXT INTEGER PRIMARY KEY , textbox TEXT, weather TEXT, enrichment INTEGER, action TEXT)"
            cur.execute(create_table_sql)
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))

        #INSERT処理
    def insert_up_data(self, today, textbox, weather, enrichment, action):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        try:
            
                       # エントリが存在するか確認
            sql_statement = "SELECT date FROM diary WHERE date = ?;"
            cur.execute(sql_statement, (today,))
            existing_entry = cur.fetchone()
            if existing_entry:
                # エントリが存在する場合は更新
                entry_id = existing_entry[0]
                update_sql = "UPDATE diary SET textbox=?, weather=?, enrichment=?, action=? WHERE date=?;"
                cur.execute(update_sql, (textbox, weather, enrichment, action, today))
                conn.commit()
            else:
                sql_statement = "INSERT INTO diary (date, textbox, weather, enrichment, action) VALUES (?,?,?,?,?)"
                cur.execute(sql_statement, (today, textbox, weather, enrichment, action))
                conn.commit()
            messagebox.showinfo("Success", "データが正常に挿入されました.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))
    #すべてのデータを取ってくる
    def serect_data(self):
        rows = []
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        
        try:
            sql_statement = "SELECT date FROM diary"
            cur.execute(sql_statement)
            rows = cur.fetchall()
            print(rows)
            return rows
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))
    #データの件数を取ってくる
    # 取得件数
    def line_data(self):
         rows = []
         conn = sqlite3.connect('diaryapp.sqlite3')
         cur = conn.cursor()
        
         try:
            sql_statement = "SELECT date FROM diary"
            cur.execute(sql_statement)
            rows = cur.fetchall()
            count = cur.rowcount
            return count
         except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))
        

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()

