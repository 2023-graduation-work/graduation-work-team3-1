import tkinter as tk
import sqlite3
from tkinter import messagebox

# SQLite3データベースへの接続をここで行う
conn = sqlite3.connect('sample.sqlite3')
cur = conn.cursor()

def check_sqlite_connection():

    try:
        # テーブル "user" が存在しない場合、CREATE TABLE ステートメントで作成
        create_table_sql = "CREATE TABLE IF NOT EXISTS user (id INT, name TEXT, age INT)"
        print('テーブルを作成')
        cur.execute(create_table_sql)
        conn.commit()
        
        print(f'conn:{conn}')   

        # テーブルにデータ\を挿入
        sql_statement = "INSERT INTO sample VALUES (8, 'Nakajima', 30)"
        cur.execute(sql_statement)
        conn.commit()

        messagebox.showinfo("Success", "データが正常に挿入されました。")
    except sqlite3.Error as e:
        messagebox.showerror("Error", "SQLite3への接続中にエラーが発生しました:\n" + str(e))

# Tkinterウィンドウの設定
root = tk.Tk()
root.title("SQLite3接続確認")

# ボタンを作成して関数を実行
check_button = tk.Button(root, text="SQLite3接続を確認", command=check_sqlite_connection)
check_button.pack(pady=20)

root.mainloop()
