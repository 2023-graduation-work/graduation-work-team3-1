import tkinter as tk
from tkcalendar import Calendar

def update_selected_date():
    # 選択した日付を取得
    selected_date = cal.get_date()
    
    # グレーにする日付を設定
    gray_dates = ["2023-10-15", "2023-10-20", "2023-10-25"]  # グレーにしたい日付のリスト
    
    print(selected_date)
    
    
root = tk.Tk()

# カレンダーウィジェットを作成
cal = Calendar(root, selectmode="day", showweeknumbers=False,selectbackground='red')  
cal.grid(row=4, column=0, padx=20, pady=10, sticky='w')  # グリッド配置
cal.bind("<<CalendarSelected>>", lambda event: update_selected_date())  # カレンダーの選択イベントに関数をバインド

root.mainloop()