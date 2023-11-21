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

        master.geometry("700x400")
        master.title("日記アプリ")
        master.resizable(False,False)

        # master.geometry("600x300")
        # master.title("日記アプリ")
        # master.resizable(False, False)

        self.create_widgets()
        self.create_datebase()


        #データが入った日の色を変更
        if len(self.serect_data()) >= 1:
            for date in self.serect_data():
                d = ",".join(date)
                da = datetime.strptime(d, "%d-%m-%Y")
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
            

            # 初期値を設定
            entry = self.get_entry_by_date(d)
            if entry:
                self.scale_var.set(entry['enrichment'])
                self.var.set(self.actions.index(entry['action']))
            else:
                weather_options = ["晴れ", "曇り", "雨", "雪"]
                self.selected_weather.set(weather_options[0])
            # テキストボックスの初期値を更新
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, "")
                print("初期値を更新")
                # エントリが存在しない場合、初期値を設定
                self.scale_var.set(1)
                self.var.set(0)

            

            # データが存在する時、textboxにデータを表示処理
            day=self.cal.get_date()
            for dayy in self.serect_data():
                d = ",".join(dayy)
                if day == d:
                    self.text.config(state=tk.NORMAL)
                    self.text.delete(1.0, tk.END)
                    textdate=self.search_textbox(day)
                    text = ",".join(textdate)
                    self.text.insert(tk.END, text)
            # データが存在する時、天気の初期値をデータに置き換える処理
                    tenki=self.search_weather(day)
                    wea = ",".join(tenki)
                    if wea == "晴れ":
                        tenki = 0
                    elif wea == "曇り":
                        tenki = 1   
                    elif wea == "雨":
                        tenki = 2
                    elif wea == "雪":
                        tenki = 3
                    
                    weather_options = ["晴れ", "曇り", "雨", "雪"]
                    self.selected_weather.set(weather_options[tenki])
                # データが存在する時、充実度の初期値をデータに置き換える処理
                    zyuzitu=self.search_enrichment(day)
                    self.scale_var.set(zyuzitu[0])
                #データが存在する時、行動の初期値をデータに置き換える処理
                    action=self.search_action(day)
                    action = ",".join(action)
                    if action == "出社":
                        action = 0
                    elif action == "テレワーク":
                        action = 1
                    elif action == "外回り":
                        action = 2
                    elif action == "出張":
                        action = 3
                    elif action == "休日":
                        action = 4
                    
                    self.var.set(action)

                    

                    
                    
                        
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
        self.text = ScrolledText(self, font=("", 15), height=7, width=30,state=tk.NORMAL)
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
        
        self.scale_var.set(0)
        
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
        
    

                
            
        
        
        #サブウィンドウを生成
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
            
            
                
            #テキストボックスの検索処理
            def perform_search():
                    keyword = search_entry.get()
                    search_results = self.keywordsearch_data(keyword)
                    search_result_text.config(state=tk.NORMAL)
                    search_result_text.delete(1.0, tk.END)
                    for result in search_results:
                        search_result_text.insert(tk.END, result)
                        search_result_text.insert(tk.END, "\n")
                    search_result_text.config(state=tk.DISABLED)
            
            search_button = tk.Button(search_window, text="検索",command= lambda : perform_search())
            search_button.pack()
    #削除処理
    def delete_entry(self):
        today = self.cal.get_date()
        self.delete_entry_by_date(today)
    #削除処理のSQL
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
            
            
            #データの日付から行動のデータを取ってくる処理
    def search_action(self, keyword):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        search_results = []
        try:
            sql_statement = "SELECT action FROM diary WHERE date = ?;"
            cur.execute(sql_statement, (keyword,))
            search_results = cur.fetchone()
            conn.commit()
            return  search_results
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))    
            
    
        #データの日付から充実度のデータを取ってくる処理
    def search_enrichment(self, keyword):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        search_results = []
        try:
            sql_statement = "SELECT enrichment FROM diary WHERE date = ?;"
            cur.execute(sql_statement, (keyword,))
            search_results = cur.fetchone()
            conn.commit()
            return  search_results
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))        
    #データの日付から天気のデータを取ってくる処理
    def search_weather(self, keyword):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        search_results = []
        try:
            sql_statement = "SELECT weather FROM diary WHERE date = ?;"
            cur.execute(sql_statement, (keyword,))
            search_results = cur.fetchone()
            conn.commit()
            return  search_results
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))        

    #データの日付からテキストボックスを取ってくる処理
    def search_textbox(self, keyword):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        search_results = []
        try:
            sql_statement = "SELECT textbox FROM diary WHERE date = ?;"
            cur.execute(sql_statement, (keyword,))
            search_results = cur.fetchone()
            conn.commit()
            return  search_results
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))
    
    #エントリーから入力されたキーワードからデータの日付を取ってくる検索処理
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
        dt = datetime.strptime(today, "%d-%m-%Y")
        
        # Convert the date to the desired format "yyyy/mm/dd"

        formatted_date = dt.strftime('%Y/%m/%d')
        
        weather = self.selected_weather.get()
        enrichment = self.scale_var.get()
        action = self.actions[self.var.get()]
        diary_text = self.text.get("1.0", tk.END)
        # Save the entry with the formatted date
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
        

    def delete_data(self, today):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        try:
            sql_statement = "DELETE FROM diary WHERE date = ?;"
            cur.execute(sql_statement, (today,))
            conn.commit()
            messagebox.showinfo("Success", "データが正常に削除されました。")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))
    
    
    def keywordsearch_data(self, keyword):
        conn = sqlite3.connect('diaryapp.sqlite3')
        cur = conn.cursor()
        search_results = []
        try:
            sql_statement = "SELECT date, textbox FROM diary WHERE textbox LIKE ?;"
            cur.execute(sql_statement, (f"%{keyword}%",))
            rows = cur.fetchall()
            for row in rows:
                r=datetime.strptime(row[0], "%d-%m-%Y")
                d = r.strftime('%Y/%m/%d')
                print(d)
                search_results.append(f"{d}:\n{row[1]}")
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))
        return search_results
    


    
if __name__ == '__main__':
    root = tk.Tk()  # ルートウィンドウを作成
    app = Application(master=root)  # Applicationクラスのインスタンスを作成
    root.mainloop()  # アプリケーションを実行




