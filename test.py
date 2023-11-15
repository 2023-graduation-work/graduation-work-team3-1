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
        master.title("日記アプリ")
        master.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        def update_selected_date():
            selected_date = cal.get_date()
            selected_date_label.config(text=f"{selected_date}の日記")
            # 新しい日付が選択されたときにエントリを取得
            selected_entry = self.get_entry_by_date(selected_date)
            if selected_entry:
                # エントリが存在する場合、情報を表示
                selected_weather.set(selected_entry['weather'])
                scale_var.set(selected_entry['enrichment'])
                self.var.set(actions.index(selected_entry['action']))
                text.delete("1.0", tk.END)
                text.insert(tk.END, selected_entry['textbox'])
            else:
                # エントリが存在しない場合、初期値を表示
                selected_weather.set(weather_options[0])
                scale_var.set(0)
                self.var.set(0)
                text.delete("1.0", tk.END)

        def save_entry():
            today = cal.get_date()
            weather = selected_weather.get()
            enrichment = scale_var.get()
            action = actions[self.var.get()]
            diary_text = text.get("1.0", tk.END)
            self.insert_or_update_entry(today, diary_text, weather, enrichment, action)

        def delete_entry():
            today = cal.get_date()
            self.delete_entry_by_date(today)

        def open_search_window():
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

            search_button = tk.Button(search_window, text="検索", command=perform_search)
            search_button.pack()

        menubar = tk.Menu(root)
        root.config(menu=menubar)
        setting_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='操作', menu=setting_menu)
        setting_menu.add_command(label='削除', command=delete_entry)
        setting_menu.add_command(label='検索', command=open_search_window)

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

    def insert_or_update_entry(self, today, textbox, weather, enrichment, action):
        conn = sqlite3.connect('daiaryapp.sqlite3')
        cur = conn.cursor()
        try:
            create_table_sql = "CREATE TABLE IF NOT EXISTS diary (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, textbox TEXT, weather TEXT, enrichment INTEGER, action TEXT);"
            cur.execute(create_table_sql)
            conn.commit()

            # エントリが存在するか確認
            sql_statement = "SELECT id FROM diary WHERE date = ?;"
            cur.execute(sql_statement, (today,))
            existing_entry = cur.fetchone()

            if existing_entry:
                # エントリが存在する場合は更新
                entry_id = existing_entry[0]
                update_sql = "UPDATE diary SET textbox=?, weather=?, enrichment=?, action=? WHERE id=?;"
                cur.execute(update_sql, (textbox, weather, enrichment, action, entry_id))
                conn.commit()
            else:
                # エントリが存在しない場合は挿入
                insert_sql = "INSERT INTO diary (date, textbox, weather, enrichment, action) VALUES (?,?,?,?,?);"
                cur.execute(insert_sql, (today, textbox, weather, enrichment, action))
                conn.commit()

            messagebox.showinfo("Success", "データが正常に挿入または更新されました。")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))

    def delete_entry_by_date(self, today):
        conn = sqlite3.connect('daiaryapp.sqlite3')
        cur = conn.cursor()
        try:
            sql_statement = "DELETE FROM diary WHERE date = ?;"
            cur.execute(sql_statement, (today,))
            conn.commit()
            messagebox.showinfo("Success", "データが正常に削除されました。")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))

    def search_data(self, keyword):
        conn = sqlite3.connect('daiaryapp.sqlite3')
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
        return search_results

    def get_entry_by_date(self, selected_date):
        conn = sqlite3.connect('daiaryapp.sqlite3')
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


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()