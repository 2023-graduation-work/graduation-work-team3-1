import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkcalendar import Calendar
from tkinter import ttk  # ttkをインポート
from datetime import date

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
        

        save_button = tk.Button(self, text="保存")  # 保存ボタンを作成
        
        
        save_button.grid(row=0, column=0, padx=(0, 100), pady=10, sticky='e')  # グリッド配置
        
        weather_options = ["晴れ", "曇り", "雨", "雪"]  # 天気の選択肢リスト

        selected_weather = tk.StringVar()  # 天気を選択するための変数を作成

        # ttk.Comboboxを使用してプルダウンメニューを作成
        weather_combobox = ttk.Combobox(self, textvariable=selected_weather, values=weather_options, width=25)
        weather_combobox.grid(row=1, column=0, padx=(300, 0), pady=10)  # グリッド配置
        weather_combobox.set(weather_options[0])  # 初期選択を設定

        weather_label = tk.Label(self, text="今日の天気:")  # ラベルを作成
        weather_label.grid(row=1, column=0, padx=(0, 0), pady=10)  # グリッド配置


        text = ScrolledText(self, font=("", 15), height=10, width=40)  # スクロール可能なテキストボックスを作成
        text.grid(row=4, column=0, padx=(250, 0), pady=10, sticky='w')  # グリッド配置

        cal = Calendar(self, selectmode="day", showweeknumbers=False)  # カレンダーウィジェットを作成
        cal.grid(row=4, column=0, padx=20, pady=10, sticky='w')  # グリッド配置
        cal.bind("<<CalendarSelected>>", lambda event: update_selected_date())  # カレンダーの選択イベントに関数をバインド

        weather_label = tk.Label(self, text="今日の充実度:")  # ラベルを作成
        weather_label.grid(row=2, column=0, padx=(0, 0), pady=0)  # グリッド配置

        self.create_slider()  # スライダーを作成

    def create_slider(self):
        self.scale_var = tk.DoubleVar()
        scaleH = tk.Scale(self, variable=self.scale_var, orient=tk.HORIZONTAL, length=180, from_=0, to=100)
        scaleH.grid(row=2, column=0, padx=(300, 0), pady=0)

if __name__ == '__main__':
    root = tk.Tk()  # ルートウィンドウを作成
    app = Application(master=root)  # Applicationクラスのインスタンスを作成
    root.mainloop()  # アプリケーションを実行
