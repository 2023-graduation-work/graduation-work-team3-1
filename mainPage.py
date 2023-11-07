import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkcalendar import Calendar
from tkinter import ttk  # ttkをインポート
from datetime import date
import db
import sqlite3
import tkinter as tk
from tkinter import messagebox

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        master.geometry("700x400")  # ウィンドウのサイズを設定
        master.title("Hello Tkinter")  # ウィンドウのタイトルを設定
        self.create_widgets()


            
    def create_widgets(self):
        def update_selected_date():
            selected_date = cal.get_date()
            selected_date_label.config(text=f"{selected_date}の日記")
            
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        setting_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='操作', menu=setting_menu)
        setting_menu.add_command(label='削除')
        setting_menu.add_command(label='検索')
        
        today = date.today()  # 今日の日付を取得
        selected_date_label = tk.Label(self, text=f"{today}の日記", font=("", 12))  # ラベルを作成
        selected_date_label.grid(row=0, column=0, padx=(350, 0), pady=10, sticky='w')  # グリッド配置
        

        
        weather_options = ["晴れ", "曇り", "雨", "雪"]  # 天気の選択肢リスト

        selected_weather = tk.StringVar()  # 天気を選択するための変数を作成

        # ttk.Comboboxを使用してプルダウンメニューを作成
        weather_combobox = ttk.Combobox(self, textvariable=selected_weather, values=weather_options, width=25)
        weather_combobox.grid(row=1, column=0, padx=(300, 0), pady=10)  # グリッド配置
        weather_combobox.set(weather_options[0])  # 初期選択を設定

        weather_label = tk.Label(self, text="今日の天気:")  # ラベルを作成
        weather_label.grid(row=1, column=0, padx=(0, 0), pady=10)  # グリッド配置
        


        text = tk.Text(self, font=("", 15), height=10, width=40)
        text.grid(row=4, column=0, padx=(250, 0), pady=10, sticky='w')
        
        


        #カレンダーウィジェットを作成
        cal = Calendar(self, selectmode="day", showweeknumbers=False)  
        cal.grid(row=4, column=0, padx=20, pady=10, sticky='w')  # グリッド配置
        cal.bind("<<CalendarSelected>>", lambda event: update_selected_date())  # カレンダーの選択イベントに関数をバインド

        weather_label = tk.Label(self, text="今日の充実度:")  # ラベルを作成
        weather_label.grid(row=2, column=0, padx=(0, 0), pady=0)  # グリッド配置


        self.scale_var = tk.DoubleVar()
        scaleH = tk.Scale(self, variable=self.scale_var, orient=tk.HORIZONTAL, length=180, from_=0, to=100)
        scaleH.grid(row=2, column=0, padx=(300, 0), pady=0)

        
        
        
                # チェック有無変数
        self.var = tk.IntVar()

        rdo1 = ttk.Radiobutton(self, text='出社', variable=self.var, value=0)
        rdo1.grid(row=3, column=0, padx=(0, 50), pady=0)

        rdo2 = ttk.Radiobutton(self, text='テレワーク', variable=self.var, value=1)
        rdo2.grid(row=3, column=0, padx=(70, 0), pady=0)

        rdo3 = ttk.Radiobutton(self, text='外回り', variable=self.var, value=2)
        rdo3.grid(row=3, column=0, padx=(200,0), pady=0)

        rdo4 = ttk.Radiobutton(self, text='出張', variable=self.var, value=3)
        rdo4.grid(row=3, column=0, padx=(300, 0), pady=0)

        rdo5 = ttk.Radiobutton(self, text='休日', variable=self.var, value=4)
        rdo5.grid(row=3, column=0, padx=(400, 0), pady=0)
        
        
        today = cal.get_date()
        weather =  weather_combobox.get()
        erichment = self.scale_var.get()
        ac = self.var.get()
        
        
        if  ac == 0 :
                action="出社"
        elif ac==1:
                action="テレワーク"
        elif ac==2:
                action="外回り"
        elif ac==3:
                action="出張"
        elif ac==4:
                action="休日"
           
           
        
        
        diary_text = text.get("1.0", tk.END)
        
    # You can now call the database function here to save the data
        
# 
# Create the "Save" button with the clic method as a command
        save_button = tk.Button(self, text="保存", command=lambda : self.click_insert(today,diary_text,weather,erichment,action))
        save_button.grid(row=0, column=0, padx=(0, 100), pady=10, sticky='e')
            
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

        def save_entry():
            today = cal.get_date()
            weather = selected_weather.get()
            enrichment = scale_var.get()
            action = actions[self.var.get()]
            diary_text = text.get("1.0", tk.END)
            self.insert_data(today, diary_text, weather, enrichment, action)

        menubar = tk.Menu(root)
        root.config(menu=menubar)
        setting_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='操作', menu=setting_menu)
        setting_menu.add_command(label='削除')
        setting_menu.add_command(label='検索')

        today = date.today()
        selected_date_label = tk.Label(self, text=f"{today}の日記", font=("", 12))
        selected_date_label.grid(row=0, column=0, padx=(350, 0), pady=10, sticky='w')

        weather_options = ["晴れ", "曇り", "雨", "雪"]
        selected_weather = tk.StringVar()
        weather_combobox = ttk.Combobox(self, textvariable=selected_weather, values=weather_options, width=25)
        weather_combobox.grid(row=1, column=0, padx=(300, 0), pady=10)
        weather_combobox.set(weather_options[0])

        weather_label = tk.Label(self, text="今日の天気:")
        weather_label.grid(row=1, column=0, padx=(0, 0), pady=10)

        text = ScrolledText(self, font=("", 15), height=10, width=40)
        text.grid(row=4, column=0, padx=(250, 0), pady=10, sticky='w')

        cal = Calendar(self, selectmode="day", showweeknumbers=False)
        cal.grid(row=4, column=0, padx=20, pady=10, sticky='w')
        cal.bind("<<CalendarSelected>>", lambda event: update_selected_date())

        weather_label = tk.Label(self, text="今日の充実度:")
        weather_label.grid(row=2, column=0, padx=(0, 0), pady=0)

        scale_var = tk.DoubleVar()
        scaleH = tk.Scale(self, variable=scale_var, orient=tk.HORIZONTAL, length=180, from_=0, to=100)
        scaleH.grid(row=2, column=0, padx=(300, 0), pady=0)

        actions = ["出社", "テレワーク", "外回り", "出張", "休日"]
        self.var = tk.IntVar()
        action_frame = ttk.Frame(self)
        action_frame.grid(row=3, column=0, padx=(0, 0), pady=0)
        for i, action in enumerate(actions):
            rdo = ttk.Radiobutton(action_frame, text=action, variable=self.var, value=i)
            rdo.grid(row=0, column=i, padx=5, pady=0)

        save_button = tk.Button(self, text="保存", command=save_entry)
        save_button.grid(row=0, column=0, padx=(0, 100), pady=10, sticky='e')



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
    def click_insert(self,today,textbox, weather,erichment,action):

            # SQLite3データベースへの接続をここで行う
            conn = sqlite3.connect('daiaryapp.splite3')
            cur = conn.cursor()
    
            try:
                    # テーブル "user" が存在しない場合、CREATE TABLE ステートメントで作成
                create_table_sql = "CREATE TABLE IF NOT EXISTS diary (id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,textbox TEXT,weather TEXT,enrichment INTEGER,action TEXT)"
                print('テーブルを作成')
                cur.execute(create_table_sql)
                conn.commit()
        
                print(f'conn:{conn}')   

                # テーブルにデータ\を挿入
                sql_statement = "INSERT INTO diary (date,textbox,weather,enrichment,action) VALUES (?,?,?,?,?)"
                cur.execute(sql_statement,(today,textbox,weather,erichment,action))
                conn.commit()
        

                messagebox.showinfo("Success", "データが正常に挿入されました。")
            except sqlite3.Error as e:
                messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))
if __name__ == '__main__':
    root = tk.Tk()  # ルートウィンドウを作成
    app = Application(master=root)  # Applicationクラスのインスタンスを作成
    root.mainloop()  # アプリケーションを実行
